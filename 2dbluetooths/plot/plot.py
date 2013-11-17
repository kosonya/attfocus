#!/usr/bin/env python


import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt



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
	X = numpy.array(X)
	Y = numpy.array(Y)
	zs = X[:,-4:].T
	x, y = Y.T
	fig = plt.figure()
	for i in xrange(4):
		ax = fig.add_subplot(2,2,i, projection='3d')
		#ax.plot3D(x, y, z1, color="b")
		z = zs[i]
		xpos = x.flatten()
		ypos = y.flatten()
		zpos = numpy.zeros(x.size * y.size)
		dx = 0.5 * numpy.ones_like(zpos)
		dy = dx.copy()
		dz = z.flatten() + 80
		ax.set_xlabel("x")
		ax.set_ylabel("y")
		ax.set_zlabel("signal level")
		ax.set_title("Bluetooth beacon {}".format(i+1))
		ax.bar3d(xpos, ypos, zpos, dx, dy, -dz, color='b', zsort='average')
	plt.tight_layout()
	plt.show()

if __name__ == "__main__":
	main()
