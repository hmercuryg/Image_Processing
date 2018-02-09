# hexagonal plot
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import pandas as pd

argv = sys.argv
argc = len(argv)

if argc != 2:
	print 'Usage: $python %s arg1(datafile)' %argv[0]
	sys.exit()

with open(argv[1],'rb') as f:
	input_array = pickle.load(f)

X_Y = np.array(input_array)
time = np.arange(len(input_array))

df = pd.DataFrame(X_Y, columns = ['x','y'])

df.plot(kind='hexbin',x='x',y='y',gridsize=25)

#fig = plt.figure(1)
#ax = fig.add_subplot(111,projection='3d')

#ax.plot_wireframe(X_Y[:,0],X_Y[:,1],time,rstride=10,cstride=10)
plt.show()
