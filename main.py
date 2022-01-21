from world import *
from cylinder import Cylinder
from RRT_3D import *

# size of cube.
x_min = 0
x_max = 1

y_min = 0
y_max = 1

z_min = 0
z_max = 1

N = 5

no_of_iterations = 7000

plt3d = plt.figure().gca(projection='3d')

env = Environment(plt3d, x_min, x_max, y_min, y_max, z_min, z_max, N)
env.make_world()

cylinder = Cylinder(plt3d)
cylinder.update_pose((0.2, 0.5, 0.026), 90, 0, 0)
cylinder.make_cylinder()

rrt = RRT(0.05, cylinder, env)
rrt.start(no_of_iterations, plt3d, cylinder, env)

plt.show()