#!/usr/bin/env python

import numpy
import gauss_pdf
import pickle

class NaiveGaussNode(object):
	def __init__(self, load_from_file = None):
		if load_from_file:
			f = open(load_from_file, "rb")
			_self = pickle.load(f)
			f.close()
			self = _self
		else:
			self.training_set = None
			self.covariances = None

def main():
	ng = NaiveGaussNode(load_from_file = "../../../../../git/smartspacedatan/v3/2_order_knode.p")

if __name__ == "__main__":
	main()
