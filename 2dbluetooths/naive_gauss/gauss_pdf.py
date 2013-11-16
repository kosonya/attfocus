#!/usr/bin/env python

import numpy


def multi_pdf(x, mean, covariance):
	k = x.size
	res = 1.0 / numpy.sqrt( ( (2.0 * numpy.pi) ** k ) * numpy.linalg.det(covariance) )
	res *= numpy.exp( -0.5 * numpy.dot(numpy.dot(numpy.transpose(x - mean), numpy.linalg.pinv(covariance)), (x - mean)) )
	return res
