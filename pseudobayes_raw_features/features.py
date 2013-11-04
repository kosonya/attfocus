#!/usr/bin/env python

import feature

class Features(object):
	def __init__(self, X, Y):
		self.X = X
		self.Y = Y

	def build_aprx(self):
		self.features = []
		for feature_n in xrange(len(self.X[0])):
			data = []
			for i in xrange(len(self.X)):
				data.append([self.X[i][feature_n], self.Y[i]])
			ftr = feature.Feature()
			ftr.create_vars(data)
			ftr.solve_theta()
			self.features.append(ftr)

	def get_thetas(self):
		res = []
		for ftr in self.features:
			res.append(ftr.theta.tolist())
		return res
