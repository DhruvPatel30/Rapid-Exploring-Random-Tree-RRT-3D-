# Importing Libraries
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy.lib.function_base import select


class Environment:
    def __init__(self, plt3d, x_min=0, x_max=1, y_min=0, y_max=1, z_min=0, z_max=1, N =10):
        self.plt3d = plt3d
        self.N = N

        self.x_min = 0
        self.x_max = 1

        self.y_min = 0
        self.y_max = 1

        self.z_min = 0
        self.z_max = 1

        # 1st face of cube. X=0 and Y and Z changes from 0 to 1 (left face)
        self.Y1 = np.linspace(y_min,y_max,self.N)
        self.Z1 = np.linspace(z_min,z_max,self.N)
        self.yy1, self.zz1 = np.meshgrid(self.Y1, self.Z1) 
        self.xx1 = 0

        # 2nd face of cube. X=1 and Y and Z changes from 0 to 1 (right face) 
        self.Y2 = np.linspace(y_min,y_max,self.N)
        self.Z2 = np.linspace(z_min,z_max,self.N)
        self.yy2, self.zz2 = np.meshgrid(self.Y2, self.Z2) 
        self.xx2 = 1

        # 3rd face of cube. Y=0 and X and Z changes from 0 to 1 (front face) 
        self.X3 = np.linspace(x_min,x_max,self.N)
        self.Z3 = np.linspace(z_min,z_max,self.N)
        self.xx3, self.zz3 = np.meshgrid(self.X3, self.Z3) 
        self.yy3 = 0

        # 4th face of cube. Y=1 and X and Z changes from 0 to 1 (rear face) 
        self.X4 = np.linspace(x_min,x_max,self.N)
        self.Z4 = np.linspace(z_min,z_max,self.N)
        self.xx4, self.zz4 = np.meshgrid(self.X4, self.Z4) 
        self.yy4 = 1

        # 5th face of cube. Z =0 and X and Y changes from 0 to 1 (bottom face) 
        self.X5 = np.linspace(x_min,x_max,self.N)
        self.Y5 = np.linspace(y_min,y_max,self.N)
        self.xx5, self.yy5 = np.meshgrid(self.X5, self.Y5) 
        self.zz5 = 0*self.xx5
        # print(self.zz5.shape)

        # 6th face of cube. Z = 1 and X and Y changes from 0 to 1 (bottom face) 
        self.X6 = np.linspace(x_min,x_max,self.N)
        self.Y6 = np.linspace(y_min,y_max,self.N)
        self.xx6, self.yy6 = np.meshgrid(self.X6, self.Y6) 
        self.zz6 = np.ones((self.N,self.N))
        # print(self.zz6.shape)

        # inner face of cube. X=0.75 and Y and Z changes from 0 to 1 (right face) 
        self.Y2 = np.linspace(y_min,y_max,self.N)
        self.Z2 = np.linspace(z_min,z_max,self.N)
        self.yy2, self.zz2 = np.meshgrid(self.Y2, self.Z2) 
        self.xx2 = 0.75
        
        # barrier free  patch 1
        self.b_Y1 = 0
        self.b_Z1 = 0
        self.b_xx1 = 0
        self.b_yy1 = 0
        self.b_zz1 = 0

        # barrier free patch 2
        self.b_Y2 = 0
        self.b_Z2 = 0
        self.b_xx2 = 0
        self.b_yy2 = 0
        self.b_zz2 = 0

        self.make_cube()
        self.make_barrier_free()
        # self.make_cylinder()


    def make_cube(self):
        self.plt3d.set_xlim(0, 2)
        self.plt3d.plot_surface(self.xx1, self.yy1, self.zz1, alpha=0.3)
        self.plt3d.plot_surface(self.xx2, self.yy2, self.zz2, alpha=0.3)
        self.plt3d.plot_surface(self.xx3, self.yy3, self.zz3, alpha=0.3)
        self.plt3d.plot_surface(self.xx4, self.yy4, self.zz4, alpha=0.3)
        self.plt3d.plot_surface(self.xx5, self.yy5, self.zz5, alpha=0.3)
        self.plt3d.plot_surface(self.xx6, self.yy6, self.zz6, alpha=0.3)
        self.plt3d.set(xlabel='X axis', ylabel='Y axis', zlabel='Z axis')
    
    def make_barrier_free(self):
        # barrier free window on the right most face.
        self.b_Y2 = np.linspace(0.425,0.575,self.N)
        self.b_Z2 = np.linspace(0.125,0.275,self.N)
        self.b_yy2, self.b_zz2 = np.meshgrid(self.b_Y2, self.b_Z2)
        self.b_xx2 = 1

        # barrier free window on the inner face.
        self.b_Y1 = np.linspace(0.425,0.575,self.N)
        self.b_Z1 = np.linspace(0.875,0.725,self.N)
        self.b_yy1, self.b_zz1 = np.meshgrid(self.b_Y1, self.b_Z1)
        self.b_xx1 = 0.75
        
        self.plt3d.plot_surface(self.b_xx2, self.b_yy2, self.b_zz2, alpha=0.8)
        self.plt3d.plot_surface(self.b_xx1, self.b_yy1, self.b_zz1, alpha=0.8)

    def make_world(self):
        self.make_cube()
        self.make_barrier_free()
        # self.draw()



