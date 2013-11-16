#!/usr/bin/env python

import numpy
import gauss_pdf
import pickle

class NaiveGaussNode(object):
	def __init__(self, load_from_file = None, dtype = "float64", debug = False):
		self.training_set = None
		self.covariances = []
		self.means = []
		self.xy_covariance = []
		self.xy_mean = []
		self.xys = None
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
			if self.xys == None:
				self.xys = out_arr[example]
			else:
				self.xys = numpy.vstack( (self.xys, out_arr[example]) )

	def stop_training(self, destroy_training_set = True):
		l = len(self.training_set)
		for i in xrange(l):
			feat = self.training_set[i]
			if self.debug:
				print "Calculating covariance and mean {} of {}".format(i, l)
			self.covariances.append(numpy.cov(feat.T))
			self.means.append(numpy.mean(feat, axis=0))
		self.xy_covariance = numpy.cov(self.xys.T)
		self.xy_mean = numpy.mean(self.xys, axis = 0)
		self.training_set = None

	#Currently only supports 2D output. I'll think of the general case later.
	def execute(self, inp, minx, maxx, miny, maxy, step = 0.5):
		in_arr = numpy.array(inp, dtype=self.dtype)
		examples = in_arr.shape[0]
		in_feats = in_arr.shape[1]
		res = None
		covdets = map(numpy.linalg.det, self.covariances)
		covpinvs = map(numpy.linalg.pinv, self.covariances)
		factor =  (2.0 * numpy.pi) ** (in_feats+2)

		xycovdet = numpy.linalg.det(self.xy_covariance)
		xycovpinv = numpy.linalg.pinv(self.xy_covariance)
		xyfactor = (2.0*numpy.pi) ** 2
		for example in xrange(examples):
			max_pdf = 0.0
			x = minx
			while x <= maxx:
				y = miny
				while y <= maxy:
					current_total_pdf = 1.0
					for in_feat in xrange(in_feats):
						arr = numpy.hstack( (in_arr[example][in_feat], numpy.array([x, y], dtype=self.dtype) ) )
						xmm = arr - self.means[in_feat]
						pdf = numpy.exp(-0.5 * numpy.dot(numpy.dot(xmm.T, covpinvs[in_feat]), xmm))/numpy.sqrt(factor*covdets[in_feat])
						current_total_pdf *= pdf


					xyarr = numpy.array([x, y], dtype=self.dtype)
					xyxmm = xyarr - self.xy_mean
					xypdf = numpy.exp(-0.5 * numpy.dot(numpy.dot(xyxmm.T, xycovpinv), xyxmm))/numpy.sqrt(xyfactor * xycovdet)

					current_total_pdf /= xypdf**(in_feats+2)

					if self.debug:
						print "x:", x, "y:", y, "pdf:", current_total_pdf, "max_pdf:", max_pdf, "xypdf:", xypdf

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
		self.dtype = str(self.dtype)
		self.means = list(self.means)
		self.covariances = list(self.covariances)
		pickle.dump(self, f)
		f.close()
				

def main():
	ng = NaiveGaussNode(load_from_file = "../../../../../git/smartspacedatan/v3/2_order_knode.p")

if __name__ == "__main__":
	main()
