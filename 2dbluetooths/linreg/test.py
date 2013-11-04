#!/usr/bin/env python

import featurebuilder
import pickle
import mdp
import math
import numpy


def load_data(filename):
	src = open(filename, "r")
	X, Y = eval(src.readline())
	src.close()
	return X, Y

def load_node(filename):
	f = open(filename, "rb")
	node = pickle.load(f)
	f.close()
	return node


def main():
	print "Loading data..."
	X, Y = load_data("test_set.py")
	node = load_node("node.p")
	print "len(X):", len(X), "len(X[0]):", len(X[0]), "len(Y):", len(Y)
	print "Building features..."
	X = featurebuilder.build_nth_x_from_set(X)
	print "Size of X:", X.shape
	Y = featurebuilder.build_y(Y)
	print "Size of Y:", Y.shape
	dsum = 0
	rights = 0
	for i in xrange(X.shape[0]):
		x = X[i]
		x = x.reshape(1, x.size)
		y_est = node.execute(x)
		y_true = Y[i]
		d = y_true - y_est[0]
		dist = math.sqrt(numpy.dot(d, d))
		dsum += dist
		y_est_r = numpy.round(y_est)
		if numpy.array_equal(y_true, y_est_r[0]):
			rights += 1
		print "true:", y_true, "estimate:", y_est, "dist:", dist, "rounded estimate:", y_est_r, "they're equal:", numpy.array_equal(y_true, y_est_r[0])
	print "Average distance:", dsum/Y.shape[0]
	print "Success rate:", rights/Y.shape[0]

if __name__ == "__main__":
	main()
