#!/usr/bin/env python

import pickle
import naive_hist_reg_node
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
	hnode = naive_hist_reg_node.NaiveHistRegNode(debug = True, order = 3)
	for i in xrange(len(X)):
		x = numpy.array(X[i])
		x = x.reshape([1, x.size])
		y = numpy.array(Y[i])
		y = y.reshape([1, y.size])
	#	print "x:", x, "y:", y
		hnode.train(x, y)
	#for row in xrange(gnode.training_set[0].shape[0]):
	#	s = ""
	#	for column in xrange(len(gnode.training_set)):
	#		s += str(gnode.training_set[column][row]) + " "
	#	print s
	hnode.stop_training()

	hnode.save(filename = "hnode.p")

if __name__ == "__main__":
	main()
