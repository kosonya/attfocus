#!/usr/bin/env python

class PerformFeature(object):
	def __init__(self, theta):
		self.order = len(theta)
		self.theta = [t for [t] in theta]


	def value(self, x):
		res = 0
		for i in xrange(0, self.order):
			res += self.theta[i] * x**i
		return res


	def pseudop(self, x, y):
		return 1.0/(1.0+(self.value(x)-float(y))**2)



class PerformFeatures(object):
	def __init__(self, thetas):
		self.thetas = thetas

	def build_features(self):
		self.features = []
		for theta in self.thetas:
			f = PerformFeature(theta)
			self.features.append(f)

	def total_pseudop(self, x, ys):
		res = 1.0
		for i in xrange(len(self.features)):
			res *= self.features[i].pseudop(x, ys[i])
		return res

	def max_pseudop(self, xs, ys):
		max_x = xs[0]
		max_p = self.total_pseudop(xs[0], ys)
		for i in xrange(1, len(xs)):
			p_i = self.total_pseudop(xs[i], ys)
			if p_i > max_p:
				max_p = p_i
				max_x = xs[i]
		return max_x
