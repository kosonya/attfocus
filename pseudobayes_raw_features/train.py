#!/usr/bin/env python

import features

def load_data(filename):
	f = open(filename, "r")
	X, Y = eval(f.readline())
	f.close()
	return X, Y

def write_thetas(thetas):
	f = open("thetas.py", "w")
	f.write(str(thetas))
	f.close()

def main():
	print "Loading data..."
	X, Y = load_data("../training_set.py")
	print "len(X):", len(X), "len(X[0]):", len(X[0]), "len(Y):", len(Y)
	ftrs = features.Features(X, Y)
	ftrs.build_aprx()
	thetas = ftrs.get_thetas()
	for theta in thetas:
		print thetas
	write_thetas(thetas)

if __name__ == "__main__":
	main()
