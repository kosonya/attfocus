#!/usr/bin/env python

import featurebuilder
import pickle
import mdp


def load_data(filename):
	src = open(filename, "r")
	X, Y = eval(src.readline())
	src.close()
	return X, Y

def teach(X, Y):
	node = mdp.nodes.LinearRegressionNode(use_pinv = True)
	print "training"
	node.train(X, Y)
	print "stopping training"
	node.stop_training()
	return node

def main():
	print "Loading data..."
	X, Y = load_data("training_set.py")
	print "len(X):", len(X), "len(X[0]):", len(X[0]), "len(Y):", len(Y)
	print "Building features..."
	X = featurebuilder.build_nth_x_from_set(X)
	print "Size of X:", X.shape
	Y = featurebuilder.build_y(Y)
	print "Size of Y:", Y.shape
	print "Teaching node.."
	node = teach(X, Y)
	print "Writing node..."
	f = open("node.p", "wb")
	pickle.dump(node, f)
	f.close()

if __name__ == "__main__":
	main()
