#!/usr/bin/env python

import pickle
import regbay_node
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
	rnode = regbay_node.RegressionBayesNode(debug = True, order = 3, use_pinv = True)
	rnode.train(numpy.array(X, dtype = "float64"), numpy.array(Y, dtype="float64"))
	rnode.stop_training()
	rnode.save(filename = "rnode.p")

if __name__ == "__main__":
	main()
