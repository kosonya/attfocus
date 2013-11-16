#!/usr/bin/env python

import numpy
import gauss_pdf
import pickle

class NaiveGaussNode(object):
	def __init__(self, load_from_file = None, dtype = "float64", debug = False):
		if load_from_file:
			f = open(load_from_file, "rb")
			_self = pickle.load(f)
			f.close()
			self = _self
		else:
			self.training_set = None
			self.covariances = None
			self.means = None
			self.dtype = dtype
			self.out_feats = 2
		self.debug = debug

	def train(self, inp, out):
		in_arr = numpy.array(inp, dtype = self.dtype)
		out_arr = numpy.array(inp, dtype = self.dtype)
		if in_arr.shape[0] ! = out_arr.shape[0]:
			raise Exception("Inconsistent array shape. In: {}. Out: {}".format(in_arr.shape, out_arr.shape))
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		out_feats = out_arr.shape[1]
		self.out_feats = out_feats
		for example in xrange(examples):
			for in_feat in xrange(in_feats):
				arr = numpy.hstack( (in_feats[example][in_feat], out_feats[example]) )
				if self.training_set != None:
					self.training_set[in_feat] = numpy.vstack( (self.training_set[in_feat], arr) )
				else:
					self.training_set.append(arr)

	def stop_training(self, destroy_training_set = True):
		l = len(self.training_set):
		for i in xrange(l):
			if debug:
				print "Calculating covariance and mean {} of {}".format(i, l)
			self.covariances.append(numpy.cov(self.training_set[i]))
			self.means.append(numpy.mean(self.training_set[i], axis=0))
		self.training_set = None

	#Currently only supports 2D output. I'll think of the general case later.
	def execute(self, inp, minx, maxx, miny, maxy, step = 0.5):
		in_arr = numpy.array(inp, dtype="float64")
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		res = None
		for example in xrange(examples):
			max_pdf = 0.0
			x = minx
			while x <= maxx:
				y = miny
				while y <= maxy:
					current_total_pdf = 1.0
					for in_feat in xrange(in_feats):
						arr = numpy.hstack( (in_arr[example][in_feat]
						pdf = gauss_pdf.multi_pdf(arr, self.means[in_feat], self.covariances[in_feat])
						current_total_pdf *= pdf
					if current_total_pdf > max_pdf:
						current_res = [x, y]
						max_pdf = current_total_pdf
			if res == None:
				res = numpy.array(current_res, dtype = self.dtype)
				res = res.reshape([1, res.size])
			else:
				res = numpy.vstack( (res, numpy.array(current_res, dtype = self.dtype)) )
		return res

	def save(self, filename, destroy_training_set = True):
		if destroy_training_set:
			self.training_set = None
		f = open(filename, "wb")
		pickle.dump(self, f)
		f.close()
				

def main():
	ng = NaiveGaussNode(load_from_file = "../../../../../git/smartspacedatan/v3/2_order_knode.p")

if __name__ == "__main__":
	main()
