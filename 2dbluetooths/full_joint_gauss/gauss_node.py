#!/usr/bin/env python

import numpy
import gauss_pdf
import pickle

class NaiveGaussNode(object):
	def __init__(self, load_from_file = None, dtype = "float64", debug = False):
		self.training_set = None
		self.covariance = None
		self.mean = None
		self.dtype = dtype
		self.out_feats = 2
		self.debug = debug
		if load_from_file:
			f = open(load_from_file, "rb")
			self = pickle.load(f)
			f.close()
			self = _self


	def train(self, inp, out):
		in_arr = numpy.array(inp, dtype = self.dtype)
		out_arr = numpy.array(out, dtype = self.dtype)
		if self.debug:
			print "in:", in_arr
			print "out:", out_arr
		if in_arr.shape[0] != out_arr.shape[0]:
			raise Exception("Inconsistent array shape. In: {}. Out: {}".format(in_arr.shape, out_arr.shape))
		arr = numpy.hstack( (in_arr, out_arr) )
		if self.training_set == None:
			self.training_set = arr
		else:
			self.training_set = numpy.vstack( (self.training_set, arr) )

	def stop_training(self, destroy_training_set = True):
		self.covariance = numpy.cov(self.training_set.T)
		self.mean = numpy.mean(self.training_set, axis=0)
		xy = self.training_set[:,-2:]
		self.xycovariance = numpy.cov(xy.T)
		self.xymean = numpy.mean(xy, axis=0)
		self.training_set = None

	#Currently only supports 2D output. I'll think of the general case later.
	def execute(self, inp, minx, maxx, miny, maxy, step = 0.5):
		in_arr = numpy.array(inp, dtype=self.dtype)
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		res = None
		covdet = numpy.linalg.det(self.covariance)
		if self.debug:
			print "Det of cov:", covdet
		covpinv = numpy.linalg.pinv(self.covariance)
		factor = (2.0 * numpy.pi) ** (in_feats+2)

		xycovdet = numpy.linalg.det(self.xycovariance)
		xycovpinv = numpy.linalg.pinv(self.xycovariance)
		xyfactor = (2.0 * numpy.pi) ** 2

		for example in xrange(examples):
			max_pdf = 0.0
			x = minx
			while x <= maxx:
				y = miny
				while y <= maxy:
					arr = numpy.hstack( (in_arr[example], numpy.array([x, y], dtype=self.dtype) ) )
					xmm = arr - self.mean
					current_total_pdf = numpy.exp(-0.5 * numpy.dot(numpy.dot(xmm.T, covpinv), xmm))/numpy.sqrt(factor*covdet)

					xyarr = numpy.array([x, y], dtype=self.dtype)
					xyxmm = xyarr - self.xymean
					xypdf = numpy.exp(-0.5 * numpy.dot(numpy.dot(xyxmm.T, xycovpinv), xyxmm))/numpy.sqrt(xyfactor*xycovdet)
					current_total_pdf /= xypdf
					if self.debug:
						print "x:", x, "y:", y, "pdf:", current_total_pdf, "max_pdf:", max_pdf
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
