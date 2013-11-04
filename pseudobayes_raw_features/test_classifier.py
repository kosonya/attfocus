#!/usr/bin/env python

import performfeature

door_range = range(0, 28+1)

def load_data():
	f = open("../test_set.py", "r")
	X, Y = eval(f.readline())
	f.close()
	return X, Y

def load_thetas():
	f = open("thetas.py", "r")
	thetas = eval(f.readline())
	f.close()
	return thetas

def main():
	X, Y = load_data()
	thetas = load_thetas()
	ftrs = performfeature.PerformFeatures(thetas)
	ftrs.build_features()
	errors = 0
	for i in xrange(len(X)):
		sample = X[i]
		ans = ftrs.max_pseudop(door_range, sample)
		print "Estimate:", ans, "real:", Y[i]
		if ans != Y[i]:
			errors += 1
	print "Errors:", errors
	print "Error percentage:", 100*float(errors)/len(X)

if __name__ == "__main__":
	main()
