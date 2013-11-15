#!/usr/bin/env python

import coordmap

import glob
import random

#data_path = "../data/"
data_path =  "../data_1_foot_grid/"
test_ratio = 0.5

def read_by_locid(locid):
	print "Reading locid:", locid
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
	global data_path
	X = []
	Y = []
	if data_path == "../data/":
		for loc in coordmap.locids:
			data = read_by_locid(loc)
			X += data
			Y += [list(coordmap._1to2[loc]) for _ in xrange(len(data))]
	elif data_path == "../data_1_foot_grid/":
		for _x in xrange(0, 8+1):
			for _y in xrange(0, 4+1):
				if _x == 0 and _y == 0:
					loc = "0"
				elif _x == 0:
					loc = str(_y)
				else:
					loc = str(_x) + str(_y)
				data = read_by_locid(loc)
				X += data
				Y += [[_x, _y] for _ in xrange(len(data))]
	return X, Y

def build_sets(X, Y):
	training = [[], []]
	test = [[], []]
	for i in xrange(len(X)):
		feats = X[i]
		_x, _y = Y[i]
		if (_x%2 == 0 and _y%2 == 1) or (_x%2 == 1 and _y%2 ==0):
			training[0].append(feats)
			training[1].append([_x, _y])
		else:
			test[0].append(feats)
			test[1].append([_x, _y])
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
