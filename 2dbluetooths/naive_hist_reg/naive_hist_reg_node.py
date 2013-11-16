#!/usr/bin/env python

import numpy
import pickle
import mdp
import itertools

def mul(seq):
	res = seq[0]
	if len(seq) == 1:
		return res
	for x in seq[1:]:
		res *= x
	return res

def build_feats(in_arr, order, debug = False):
	res = None
	i = 1
	in_arr = numpy.hstack( (numpy.ones([in_arr.shape[0], 1]), in_arr) )
	for feat in itertools.combinations_with_replacement(in_arr.T, r = order):
		if debug:
			print "Processing feature", i
		i += 1
		arr = mul(feat)
		arr = arr.reshape([arr.size, 1])
		if res == None:
			res = arr
		else:
			res = numpy.hstack( (res, arr) )
	res = res[:,1:]
	return res

def posts_to_fence(posts):
	return reduce(lambda (lst, prev), cur: (numpy.hstack( (lst, float(cur+prev)/2.0) ), cur), posts[1:], (numpy.array([]), posts[0]))[0]

class NaiveHistRegNode(object):
	def __init__(self, dtype = "float64", debug = False, order = 2):
		self.training_set = None
		self.lnodes = []
		self.dtype = dtype
		self.debug = debug
		self.order = order


	def train(self, inp, out):
		in_arr = numpy.array(inp, dtype = self.dtype)
		out_arr = numpy.array(out, dtype = self.dtype)
		if in_arr.shape[0] != out_arr.shape[0]:
			raise Exception("Inconsistent array shape. In: {}. Out: {}".format(in_arr.shape, out_arr.shape))
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		out_feats = out_arr.shape[1]
		self.out_feats = out_feats
		for example in xrange(examples):
			tmp_res = []
			if self.debug:
				print "in_arr[{}] = {}".format(example, in_arr[example])
				print "out_arr[{}] = {}".format(example, out_arr[example])
			for in_feat in xrange(in_feats):
				arr = numpy.hstack( (in_arr[example][in_feat], out_arr[example]) )
				if self.training_set != None:
					self.training_set[in_feat] = numpy.vstack( (self.training_set[in_feat], arr) )
				else:
					tmp_res.append(arr)
			if self.training_set == None:
				self.training_set = tmp_res


	def stop_training(self, destroy_training_set = True):
		l = len(self.training_set)
		self.lnodes = [mdp.nodes.LinearRegressionNode(use_pinv = True) for _ in xrange(l)]
		for i in xrange(l):
			feat = self.training_set[i]
			if self.debug:
				print "Calculating histogram {} of {}".format(i, l)
			H, edges = numpy.histogramdd(feat, bins = (5, 8, 4), normed = False)
			centers = map(posts_to_fence, edges)
			grid = numpy.ix_(*centers)
			if self.debug:
				print "H", H.shape
				print H
			lnode_X = None
			lnode_Y = None
			for y in xrange(H.shape[1]):
				tmp_y = None
				for z in xrange(H.shape[2]):
					for x in xrange(H.shape[0]):
						_x = centers[0][x]
						_y = centers[1][y]
						_z = centers[2][z]
						if self.debug:
							print "y:", _y, "z:", _z, "x:", _x, "f:", H[x, y, z]
						arr = numpy.array([_y, _z, _x], dtype = self.dtype)
						arr = arr.reshape([1, 3])
						if lnode_X == None:
							lnode_X = arr
						else:
							lnode_X = numpy.vstack( (lnode_X, arr) )
						arr = numpy.array([H[x, y, z]], dtype = self.dtype).reshape([1, 1])
						if tmp_y == None:
							tmp_y = arr
						else:
							tmp_y = numpy.vstack( (tmp_y, arr) )

					if self.debug:
						print ""
				tmp_y = tmp_y / numpy.max(tmp_y)
				if self.debug:
					print tmp_y
				if lnode_Y == None:
					lnode_Y = tmp_y
				else:
					lnode_Y = numpy.vstack( (lnode_Y, tmp_y) )

			if self.debug:
				print "X"
				print lnode_X
				print "Y"
				print lnode_Y

			if self.debug:
				print "Building polynomial features"
			lnode_X = build_feats(lnode_X, self.order, self.debug)

			if self.debug:
				print "Training node", i
			self.lnodes[i].train(lnode_X, lnode_Y)
			self.lnodes[i].stop_training()
			if self.debug:
				print "Done"

		if destroy_training_set:
			self.training_set = None

	#Currently only supports 2D output. I'll think of the general case later.
	def execute(self, inp, minx, maxx, miny, maxy, step = 0.5):
		in_arr = numpy.array(inp, dtype=self.dtype)
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		res = None
		current_res = None
		for example in xrange(examples):
			max_pdf = 0.0
			x = minx
			while x <= maxx:
				y = miny
				while y <= maxy:
					current_total_pdf = 1.0
					for in_feat in xrange(in_feats):
						feat_x_y = numpy.array([x, y, in_arr[example][in_feat]], dtype=self.dtype)
						feat_x_y = feat_x_y.reshape([1, 3])
						feat_x_y = build_feats(feat_x_y, self.order, False)
						pdf = self.lnodes[in_feat].execute(feat_x_y)[0][0]
						current_total_pdf *= pdf

					if current_total_pdf > max_pdf:
						current_res = [x, y]
						max_pdf = current_total_pdf
					if self.debug:
						print "x:", x, "y:", y, "pdf:", current_total_pdf, "max_pdf:", max_pdf, "res:", current_res
					y += step
				x += step
			if res == None:
				res = numpy.array(current_res, dtype = self.dtype)
				res = res.reshape([1, res.size])
			else:
				res = numpy.vstack( (res, numpy.array(current_res, dtype = self.dtype)) )
		return res

	def save(self, filename, destroy_training_set = True):
		if destroy_training_set:
			self.training_set = None
		else:
			self.training_set = list(self.training_set)
		f = open(filename, "wb")

		pickle.dump(self, f)
		f.close()
				

def main():
	ng = NaiveGaussNode(load_from_file = "../../../../../git/smartspacedatan/v3/2_order_knode.p")

if __name__ == "__main__":
	main()
