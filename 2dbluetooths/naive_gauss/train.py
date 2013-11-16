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
	gnode = gauss_node.NaiveGaussNode(debug = False)
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
	for i in xrange(len(gnode.covariances)):
		print i, ":"
		print "mean:", gnode.means[i]
		print "covariance:"
		print gnode.covariances[i]
		print "cov det:", numpy.linalg.det(gnode.covariances[i])
		print "\n"
	print "xy mean:", gnode.xy_mean
	print "xy cov:", gnode.xy_covariance
	gnode.save(filename = "gnode.p")

if __name__ == "__main__":
	main()
