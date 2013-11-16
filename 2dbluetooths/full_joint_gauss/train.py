#!/usr/bin/env python

import pickle
import gauss_node
import numpy



def load_data(filename):
	src = open(filename, "r")
	X, Y = eval(src.readline())
	src.close()
	return X, Y


def main():
	print "Loading data..."
	X, Y = load_data("training_set.py")
	print "len(X):", len(X), "len(X[0]):", len(X[0]), "len(Y):", len(Y)
	gnode = gauss_node.NaiveGaussNode(debug = True)
	for i in xrange(len(X)):
		x = numpy.array(X[i])
		x = x.reshape([1, x.size])
		y = numpy.array(Y[i])
		y = y.reshape([1, y.size])
	#	print "x:", x, "y:", y
		gnode.train(x, y)
	#for row in xrange(gnode.training_set[0].shape[0]):
	#	s = ""
	#	for column in xrange(len(gnode.training_set)):
	#		s += str(gnode.training_set[column][row]) + " "
	#	print s
	gnode.stop_training()
	print "Means:", gnode.mean.shape
	print gnode.mean, "\n"
	print "Covariance:", gnode.covariance.shape
	print gnode.covariance
	print "Det of cov:", numpy.linalg.det(gnode.covariance)
	print "XY Means:", gnode.xymean.shape
	print gnode.xymean.shape
	print "XY Covariance:", gnode.xycovariance.shape
	print gnode.xycovariance
	print "Det of XYcov:", numpy.linalg.det(gnode.xycovariance)
	gnode.save(filename = "gnode.p")

if __name__ == "__main__":
	main()
