#!/usr/bin/env python

import coordmap

import glob
import random

data_path = "../data/"
test_ratio = 0.2

def read_by_locid(locid):
	filename = glob.glob(data_path + str(locid) + "-*.csv")[0]
	f = open(filename, "r")
	res = read_one_file(f)
	f.close()
	return res

def read_one_file(f):
	res = []
	for line in f.readlines()[1:]:
		if not line:
			break
		d = map(float, line.split(','))
		res.append(d)
	return res

def build_x_y():
	X = []
	Y = []
	for loc in coordmap.locids:
		data = read_by_locid(loc)
		X += data
		Y += [list(coordmap._1to2[loc]) for _ in xrange(len(data))]
	return X, Y

def build_sets(X, Y):
	training = [[], []]
	test = [[], []]
	for i in xrange(len(X)):
		dst_set = training if random.uniform(0, 1) > test_ratio else test
		dst_set[0].append(X[i])
		dst_set[1].append(Y[i])
	return training, test


def write_sets(training, test):
	f = open("training_set.py", "w")
	f.write(str(training))
	f.close()
	f = open("test_set.py", "w")
	f.write(str(test))
	f.close()

def main():
	X, Y = build_x_y()
	training, test = build_sets(X, Y)
	write_sets(training, test)

	
if __name__ == "__main__":
	main()	
