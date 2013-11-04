import numpy
import math
import itertools


def quad_arr_from_sample(sample):
	res = []
	for n in xrange(len(sample)):
		for m in xrange(n, len(sample)):
			res.append(sample[n]*sample[m])
	return [1] + res

def cube_arr_from_sample(sample):
	res = []
	for n in xrange(len(sample)):
		for m in xrange(n, len(sample)):
			for k in xrange(m, len(sample)):
				res.append(sample[n]*sample[m]*sample[k])
	return [1] + res

def fourth_arr_from_sample(sample):
	res = []
	for n in xrange(len(sample)):
		for m in xrange(n, len(sample)):
			for k in xrange(m, len(sample)):
				for l in xrange(k, len(sample)):
					res.append(sample[n]*sample[m]*sample[k]*sample[l])
	return [1] + res

def fifth_arr_from_sample(sample):
	res = []
	for n in xrange(len(sample)):
		for m in xrange(n, len(sample)):
			for k in xrange(m, len(sample)):
				for l in xrange(k, len(sample)):
					for o in xrange(l, len(sample)):
						res.append(sample[n]*sample[m]*sample[k]*sample[l]*sample[o])
	return [1] + res


def sixth_arr_from_sample(sample):
	res = []
	sample = [1] + sample
	for n in xrange(len(sample)):
		for m in xrange(n, len(sample)):
			for k in xrange(m, len(sample)):
				for l in xrange(k, len(sample)):
					for o in xrange(l, len(sample)):
						for p in xrange(o, len(sample)):
							res.append(sample[n]*sample[m]*sample[k]*sample[l]*sample[o]*sample[p])
	return [1] + res

def seventh_arr_from_sample(sample):
	res = []
	sample = [1] + sample
	for n in xrange(len(sample)):
		for m in xrange(n, len(sample)):
			for k in xrange(m, len(sample)):
				for l in xrange(k, len(sample)):
					for o in xrange(l, len(sample)):
						for p in xrange(o, len(sample)):
							for q in xrange(p, len(sample)):
								res.append(sample[n]*sample[m]*sample[k]*sample[l]*sample[o]*sample[p]*sample[q])
	return [1] + res

def build_quad_x_from_set(arr_X):
	order = sum(xrange( (len(arr_X[0]))+1)) + 1
	l = len(arr_X)
	X = numpy.empty([l, order])
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		quad_sample = quad_arr_from_sample(sample)
		X[i] = quad_sample
	return X

def build_cube_x_from_set(arr_X):
	l = len(arr_X)
	n = len(arr_X[0]) + 3
	order = n*(n**2-6*n+11)/6 
	print len(arr_X[0])
	print order
	X = numpy.empty([l, order])
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		cube_sample = cube_arr_from_sample(sample)
		X[i] = cube_sample
	return X

def build_fourth_x_from_set(arr_X):
	l = len(arr_X)
	n = len(arr_X[0]) 
	order = 1 + (6 + (11 + (6 + n)*n)*n)*n/24 
	print len(arr_X[0])
	print order
	X = numpy.empty([l, order])
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		fourth_sample = fourth_arr_from_sample(sample)
		X[i] = fourth_sample
	return X

def build_fifth_x_from_set(arr_X):
	l = len(arr_X)
	n = len(arr_X[0]) 
	order = len(fifth_arr_from_sample(arr_X[0]))
	print len(arr_X[0])
	print order
	X = numpy.empty([l, order])
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		fifth_sample = fifth_arr_from_sample(sample)
		X[i] = fifth_sample
	return X

def build_sixth_x_from_set(arr_X):
	l = len(arr_X)
	n = len(arr_X[0]) 
	order = len(sixth_arr_from_sample(arr_X[0]))
	print len(arr_X[0])
	print order
	X = numpy.empty([l, order])
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		sixth_sample = sixth_arr_from_sample(sample)
		X[i] = sixth_sample
	return X

def build_seventh_x_from_set(arr_X):
	l = len(arr_X)
	n = len(arr_X[0]) 
	order = len(seventh_arr_from_sample(arr_X[0]))
	print len(arr_X[0])
	print order
	X = numpy.empty([l, order])
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		seventh_sample = seventh_arr_from_sample(sample)
		X[i] = seventh_sample
	return X


def nth_arr_from_sample(sample, n=4):
	combs = itertools.combinations_with_replacement([1] + sample, n)

	return map(lambda x: reduce(lambda a, b: a*b, x, 1), itertools.combinations_with_replacement([1] + sample, n))

def build_nth_x_from_set(arr_X, n = 7):
	l = len(arr_X)
	order = len(nth_arr_from_sample(arr_X[0], n))
	print "Original features:", len(arr_X[0])
	print "Built features:", order
	X = numpy.empty([l, order])
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		nth_sample = nth_arr_from_sample(sample, n)
		X[i] = nth_sample
	return X	

def build_y(arr_Y):
	return numpy.array(map(lambda x: [x], arr_Y))
