import numpy as np
import math
from world import Environment as env
from RRT_3D import *

class Cylinder:
    def __init__(self, plt3d, center = (0,0,0), radius= 0.026, height = 0.122, roll =0, pitch=0, yaw=0, N=10):
        self.plt3d = plt3d
        self.N = N

        self.center = center
        self.radius = radius
        self.height = height

        self.roll = math.radians(roll)
        self.pitch = math.radians(pitch)
        self.yaw = math.radians(yaw)

        self.cylinder_z = 0
        self.theta = 0
        self.theta_grid = 0
        self.x_grid = 0
        self.y_grid = 0
        self.z_grid = 0

        # list to store the values of a,b,c and d of planes
        # left, middle, right, bottom, top, front, rear. (sequence of the planes stored below)
        self.const_for_plane = [[1,0,0,0], [1,0,0,-0.75], [1,0,0,-1], [0,0,1,0], [0,0,1,-1], [0,1,0,0], [0,1,0,-1]]


        self.cylinder_lower_plane_x = []
        self.cylinder_lower_plane_y = []
        self.cylinder_lower_plane_z = []
        self.lower_plane_flag = 0

        self.cylinder_upper_plane_x = []
        self.cylinder_upper_plane_y = []
        self.cylinder_upper_plane_z = []
        self.upper_plane_flag = 0


    def make_cylinder(self):
        self.cylinder_z = np.linspace(-self.height/2, self.height/2, self.N)
        self.theta = np.linspace(0, 2*np.pi, self.N)
        theta_grid, temp_z_grid = np.meshgrid(self.theta, self.cylinder_z)
        temp_x_grid = self.radius*np.cos(theta_grid) 
        temp_y_grid = self.radius*np.sin(theta_grid) 

        # Rotation around Z axis.
        x = np.array(temp_x_grid)
        y = np.array(temp_y_grid)
        z = np.array(temp_z_grid)
        for i in range(temp_x_grid.shape[0]):
            for j in range(temp_x_grid.shape[1]):
                x[i][j]= math.cos(self.yaw)*temp_x_grid[i][j]-math.sin(self.yaw)*temp_y_grid[i][j]
                y[i][j]= math.sin(self.yaw)*temp_x_grid[i][j]+math.cos(self.yaw)*temp_y_grid[i][j]

        # Rotation around Y axis
        x_temp = np.array(x)
        z_temp = np.array(z)
        for i in range(x_temp.shape[0]):
            for j in range(x_temp.shape[1]):
                x[i][j]= math.cos(self.pitch)*x_temp[i][j]+math.sin(self.pitch)*z_temp[i][j]
                z[i][j]= -math.sin(self.pitch)*x_temp[i][j]+math.cos(self.pitch)*z_temp[i][j]

        #Rotate wrt X axis
        y_temp = np.array(y)
        z_temp = np.array(z)
        for i in range(y_temp.shape[0]):
            for j in range(y_temp.shape[1]):
                y[i][j]= math.cos(self.roll)*y_temp[i][j]-math.sin(self.roll)*z_temp[i][j]
                z[i][j]= math.sin(self.roll)*y_temp[i][j]+math.cos(self.roll)*z_temp[i][j]

        x += self.center[0]
        y += self.center[1]
        z += self.center[2]

        self.x_grid = np.array(x)
        self.y_grid = np.array(y)
        self.z_grid = np.array(z)

        self.plt3d.plot_surface(self.x_grid, self.y_grid, self.z_grid, alpha=0.8)


    def update_pose(self, center, roll, pitch, yaw):
        self.center = center
        self.roll = math.radians(roll)
        self.pitch = math.radians(pitch)
        self.yaw = math.radians(yaw)

    # def intersection_with_plane(self, x, y, z, a, b, c, d):
    #     if ((a*x + b*y + c*z + d) >= 0):
    #         return True, 1 
    #     return False, -1

    # def check__lower_cylinder_plane(self):
    #     for j in range(len(self.const_for_plane)):
    #         flag = True
    #         for i in range(len(self.cylinder_lower_plane_x)):
    #             if i==0:
    #                 flag, self.lower_plane_flag = self.intersection_with_plane(self.cylinder_lower_plane_x[i], self.cylinder_lower_plane_y[i], self.cylinder_lower_plane_z[i], self.const_for_plane[j][0], self.const_for_plane[j][1],self.const_for_plane[j][2],self.const_for_plane[j][3]) 
    #             else:
    #                 if self.intersection_with_plane(self.cylinder_lower_plane_x[i], self.cylinder_lower_plane_y[i], self.cylinder_lower_plane_z[i], self.const_for_plane[j][0], self.const_for_plane[j][1],self.const_for_plane[j][2],self.const_for_plane[j][3]) != flag:
    #                     return True
    #     return False
    
    # def check_upper_cylinder_plane(self):
    #     for j in range(len(self.const_for_plane)):
    #         flag = True
    #         for i in range(len(self.cylinder_upper_plane_x)):
    #             if i==0:
    #                 flag, self.upper_plane_flag = self.intersection_with_plane(self.cylinder_upper_plane_x[i], self.cylinder_upper_plane_y[i], self.cylinder_upper_plane_z[i], self.const_for_plane[j][0], self.const_for_plane[j][1],self.const_for_plane[j][2],self.const_for_plane[j][3]) 
    #             else:
    #                 if self.intersection_with_plane(self.cylinder_upper_plane_x[i], self.cylinder_upper_plane_y[i], self.cylinder_upper_plane_z[i], self.const_for_plane[j][0], self.const_for_plane[j][1],self.const_for_plane[j][2],self.const_for_plane[j][3]) != flag:
    #                     return True
    #     return False

    # def check_perp_dist_bet_axis_bound(self, var):
    #     if var == 'l':
    #         x_min = min(self.cylinder_lower_plane_x)
    #         x_max = max(self.cylinder_lower_plane_x)

    #         y_min = min(self.cylinder_lower_plane_y)
    #         y_max = max(self.cylinder_lower_plane_y)

    #         z_min = min(self.cylinder_lower_plane_z)
    #         z_max = max(self.cylinder_lower_plane_z)

    #         x, y, z = (x_min+x_max)/2, (y_min+y_max)/2, (z_min+z_max)/2   # center of the lower plane

    # def collison_check(self):

    #     self.cylinder_lower_plane_x = self.x_grid[0]
    #     self.cylinder_lower_plane_y = self.y_grid[0]
    #     self.cylinder_lower_plane_z = self.z_grid[0]

    #     self.cylinder_upper_plane_x = self.x_grid[self.N-1]
    #     self.cylinder_upper_plane_y = self.y_grid[self.N-1]
    #     self.cylinder_upper_plane_z = self.z_grid[self.N-1]

    #     lower_plane = self.check__lower_cylinder_plane()            # if lower plane will be intersecting "lower_plane" will be true. 
    #     upper_plane = self.check_upper_cylinder_plane()             # if upper plane will be intersecting "upper_plane" will be true.

    #     if lower_plane == False and upper_plane == False and (self.upper_plane_flag == self.lower_plane_flag):   # if self.upper_plane_flag and self.lower_plane_flag are same, that means both the pane are on one side of any face of cube.
    #         return False                                                                                         # This condition is taken into consideration because while passing through the window, this circumstance will come.
    #     return True

        # if lower_plane == True:
        #     y_min = min(self.cylinder_lower_plane_y)
        #     y_max = max(self.cylinder_lower_plane_y)

        #     z_min = min(self.cylinder_lower_plane_z)
        #     z_max = max(self.cylinder_lower_plane_z)

            

        #     self.check_perp_dist_bet_axis_bound('l')

        # print(lower_plane)


        
        