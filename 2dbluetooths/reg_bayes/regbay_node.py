#!/usr/bin/env python

import numpy
import mdp
import itertools
import pickle

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

def pseudo_pdf(estimated_x, true_x):
	return 1.0 / (1.0 + (estimated_x - true_x)**2)

class RegressionBayesNode(object):
	def __init__(self, dtype = "float64", debug = False, order = 2, use_pinv = True):
		self.training_set = None
		self.lnodes = []
		self.order = order
		self.use_pinv = use_pinv
		self.debug = debug
		self.dtype = dtype


	def train(self, inp, out):
		in_arr = numpy.array(inp, dtype = self.dtype)
		out_arr = numpy.array(out, dtype = self.dtype)
		if in_arr.shape[0] != out_arr.shape[0]:
			raise Exception("Inconsistent array shape. In: {}. Out: {}".format(in_arr.shape, out_arr.shape))
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		out_feats = out_arr.shape[1]
		if self.debug:
			print "Building out features"
		out_pol_arr = build_feats(in_arr = out_arr, order = self.order, debug = self.debug)

		if self.lnodes == []:
			self.lnodes = [mdp.nodes.LinearRegressionNode(use_pinv = self.use_pinv, dtype=self.dtype) for _ in xrange(in_feats)]
		for feat in xrange(in_feats):
			in_feat = in_arr[:,feat]
			in_feat = in_feat.reshape([in_feat.size, 1])
			if self.debug:
				print "Processing feature {} of {}".format(feat, in_feats)
			self.lnodes[feat].train(out_pol_arr, in_feat)
			

	def stop_training(self):
		l = len(self.lnodes)
		for i in xrange(l):
			if self.debug:
				print "Stopping training node {}".format(i)
			self.lnodes[i].stop_training()

	#Currently only supports 2D output. I'll think of the general case later.
	def execute(self, inp, minx, maxx, miny, maxy, step = 0.5):
		in_arr = numpy.array(inp, dtype=self.dtype)
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		res = None

		for example in xrange(examples):
			max_pdf = 0.0
			x = minx
			while x <= maxx:
				y = miny
				while y <= maxy:
					xy = numpy.array([x, y], dtype = self.dtype)
					xy = xy.reshape([1, xy.size])
					xy = build_feats(xy, order = self.order, debug = self.debug)
					current_total_pdf = 1.0
					for in_feat in xrange(in_feats):
						true_x = in_arr[example][in_feat]
						estimated_x = self.lnodes[in_feat].execute(xy)
						pp = pseudo_pdf(estimated_x, true_x)
						current_total_pdf *= pp

					if current_total_pdf > max_pdf:
						current_res = [x, y]
						max_pdf = current_total_pdf
					y += step
				x += step
			if res == None:
				res = numpy.array(current_res, dtype = self.dtype)
				res = res.reshape([1, res.size])
			else:
				res = numpy.vstack( (res, numpy.array(current_res, dtype = self.dtype)) )
		return res

	def save(self, filename):
		f = open(filename, "wb")
		pickle.dump(self, f)
		f.close()
				
def main():
	ng = NaiveGaussNode(load_from_file = "../../../../../git/smartspacedatan/v3/2_order_knode.p")

if __name__ == "__main__":
	main()
