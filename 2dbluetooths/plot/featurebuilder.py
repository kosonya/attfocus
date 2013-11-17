import numpy
import math
import itertools



def nth_arr_from_sample(sample, n=4):
	res = map(lambda x: reduce(lambda a, b: a*b, x, 1), itertools.combinations_with_replacement(sample, n))
	return res

def build_nth_x_from_set(arr_X, n = 5):
	l = len(arr_X)
	order = len(nth_arr_from_sample(arr_X[0], n))
	print "Original features:", len(arr_X[0])
	print "Built features:", order
	X = numpy.empty([l, order], dtype="float64")
	for i in xrange(len(arr_X)):
		sample = arr_X[i]
		nth_sample = nth_arr_from_sample(sample, n)
		X[i] = nth_sample
	return X	

def build_y(arr_Y):
	res = numpy.array(arr_Y, dtype="float64")
	return res
