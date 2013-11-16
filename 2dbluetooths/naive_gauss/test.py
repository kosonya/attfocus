#!/usr/bin/env python

import featurebuilder
import pickle
import numpy
import gauss_node

def load_data(filename):
	src = open(filename, "r")
	X, Y = eval(src.readline())
	src.close()
	return X, Y



def main():
	print "Loading data..."
	X, Y = load_data("test_set.py")
	f = open("gnode.p", "rb")
	gnode = pickle.load(f)
	f.close()
	gnode.debug = False
	print "len(X):", len(X), "len(X[0]):", len(X[0]), "len(Y):", len(Y)
	Y = numpy.array(Y, dtype="float64")
	print "Shape of Y:", Y.shape
	X = numpy.array(X, dtype="float64")
	print "Shape of X:", X.shape
	dsum = 0
	rights = 0
	for i in xrange(X.shape[0]):
		x = X[i]
		x = x.reshape(1, x.size)
		y_est = gnode.execute(x, minx = -1.0, maxx = 10.0, miny = -1.0, maxy = 10.0, step = 0.5)
		y_true = Y[i]
		d = y_true - y_est[0]
		dist = numpy.sqrt(numpy.dot(d, d))
		dsum += dist
		y_est_r = numpy.round(y_est)
		got_it_right = numpy.array_equal(y_true, y_est_r[0])
		if got_it_right:
			rights += 1
		print "true:", y_true, "estimate:", y_est, "dist:", dist, "rounded estimate:", y_est_r, "they're equal:", got_it_right
	print "Average distance:", dsum/Y.shape[0]
	print "Success rate:", float(rights)/Y.shape[0]

if __name__ == "__main__":
	main()
