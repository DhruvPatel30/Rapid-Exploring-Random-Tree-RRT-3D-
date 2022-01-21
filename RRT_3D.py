from matplotlib import pyplot as plt
from world import Environment as env
import math
import random
from scipy.spatial import cKDTree


class RRT:
    def __init__(self, maxStepSize, cyl, env):

        self.maxStepSize = maxStepSize
        self.factor = math.sqrt(cyl.radius**2 + (cyl.height/2)**2)
        print(self.factor)
        # Defines the range of x,y and z for generatinf the random point, which will be the center of the cylinder
        self.x_min = env.x_min + self.factor
        self.x_max = env.x_max + 0.7 

        self.y_min = env.y_min + self.factor
        self.y_max = env.y_max - self.factor

        self.z_min = env.z_min + self.factor
        self.z_max = env.z_max - self.factor

        self.position = []

        self.orientation = []

        self.parent = []

        self.position.append([cyl.center[0], cyl.center[1], cyl.center[2]])
    
        self.orientation.append([cyl.roll, cyl.pitch, cyl.yaw])

        self.parent.append(0)   # the parent of the first node is the node itself

        self.path = []

        self.x_goal = 1.5
        self.y_goal = 0.5
        self.z_goal = 0.2
        self.tolerance = 0.1

        # giving some tolerance window
        self.xgmin = self.x_goal - self.tolerance
        self.xgmax = self.x_goal + self.tolerance

        self.ygmin = self.y_goal - self.tolerance
        self.ygmax = self.y_goal + self.tolerance

        self.zgmin = self.z_goal - self.tolerance
        self.zgmax = self.z_goal + self.tolerance
    
    def atgoal(self):
        n= self.get_number_of_nodes()-1
        (x,y,z)= (self.position[n][0], self.position[n][1], self.position[n][2]) 
        if (x>=self.xgmin) and (x<=self.xgmax) and (y>=self.ygmin) and (y<=self.ygmax) and (z>=self.zgmin) and (z<=self.zgmax):
            return 1
        else:
            return 0

    def get_number_of_nodes(self):
        return (len(self.position))

    def add_node(self, n, position, orientation):
        self.position.insert(n, position)
        self.orientation.insert(n, orientation)
    
    def add_edge(self, parent, child):
        self.parent.insert(child, parent)

    def remove_node(self, n):
        self.position.pop(n)
        self.orientation.pop(n)
    
    def metric(self, node1, node2):     # arguments are the index of nodes
        x1, y1, z1 = self.position[node1]
        x2, y2, z2 = self.position[node2]
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y2 = float(y2)
        z1 = float(z1)
        z2 = float(z2)
        return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)       # euclidean distance

    def get_random_node(self):
        x = random.uniform(self.x_min, self.x_max)
        y = random.uniform(self.y_min, self.y_max)
        z = random.uniform(self.z_min, self.z_max)
        roll = random.uniform(0, 180)
        pitch = random.uniform(0, 180)
        yaw = random.uniform(0, 180)
        position = [x,y,z]
        orientation = [roll, pitch, yaw]
        return position, orientation

    def valid_points(self, x, y, z):
        val = 0.025
        if x>=self.factor and x<(0.75-self.factor):
            if y<self.factor or y>1-self.factor or z<self.factor or x>1-self.factor:
                return False
        
        elif x>(0.75+self.factor) and x<(1-self.factor):
            if y<self.factor or y>1-self.factor or z<self.factor or x>1-self.factor:
                return False

        elif (0.75-self.factor)< x <(0.75+self.factor):
            if y<0.425+val  or y>0.575-val or z<0.725+val or z>0.875-val:            # some padding can be added.
                return False

        elif (1-self.factor)< x <(1+self.factor):
            if y<0.425+val or y>0.575-val  or z<0.125+val or z>0.275-val:
                return False

        return True

    def check_step(self, near_n, n, dist, pos, orientation):
        if dist < self.maxStepSize:
            if self.valid_points(pos[0], pos[1], pos[2]) == False:
                self.remove_node(n)
            
        elif dist > self.maxStepSize:
            x_rand, y_rand, z_rand = self.position[n][0], self.position[n][1], self.position[n][2]
            x_near, y_near, z_near = self.position[near_n][0], self.position[near_n][1], self.position[near_n][2]
            px, py, pz = (x_rand-x_near, y_rand-y_near, z_rand-z_near)
            magnitude = math.sqrt((x_rand-x_near)**2 + (y_rand-y_near)**2 + (z_rand-z_near)**2)
            unit_px, unit_py, unit_pz = px/magnitude, py/magnitude, pz/magnitude
            x_, y_, z_ = self.maxStepSize*unit_px, self.maxStepSize*unit_py, self.maxStepSize*unit_pz 
            x, y, z = x_near+x_, y_near+y_, z_near+z_
            self.remove_node(n)
            if (self.valid_points(x, y, z)):
                position = [x,y,z]
                self.add_node(n, position, orientation)

    def connect(self, node1, node2):
        self.add_edge(node1, node2)

    def expand(self):
        kd_tree = cKDTree(self.position)
        position , orienatation = self.get_random_node()
        dist, near_n = kd_tree.query(position, k = 1)
        n = self.get_number_of_nodes()
        self.add_node(n, position, orienatation)
        self.check_step(near_n, n, dist,position,  orienatation)    # Check if the distance between nearest neighbor and random node is less than maxStepSize. If not, decrease the length of the edge.
        self.connect(near_n, n)

    def path_to_goal(self):
		#find goal state
        i = self.get_number_of_nodes() - 1       # the last node inserted in the list will be the goal node.
        self.path.append(i)
        newpos=self.parent[i]
        #keep adding parents	
        while (newpos!=0):
            self.path.append(newpos)
            newpos = self.parent[newpos]	
        #add start state
        self.path.append(0)

    #draw tree
    def showtree(self,k, ax):
        for i in range (0,self.get_number_of_nodes()):
            par=self.parent[i]
            # plt.plot([self.x[i],self.x[par]],[self.y[i],self.y[par]],k,lw=0.5)
            # ax.scatter([self.position[i][0],self.position[par][0]], [self.position[i][1],self.position[par][1]], [self.position[i][2],self.position[par][2]], c= "blue", s=5)
            ax.plot([self.position[i][0],self.position[par][0]], [self.position[i][1],self.position[par][1]], [self.position[i][2],self.position[par][2]], color = "black")
            
    #draw path 
    def showpath(self,k, plt3d):
        for i in range (len(self.path)-1):
                n1=self.path[i]
                n2=self.path[i+1]
                # plt.plot([self.x[n1],self.x[n2]],[self.y[n1],self.y[n2]],k,lw=1,markersize=3)
                plt3d.plot([self.position[n1][0],self.position[n2][0]], [self.position[n1][1],self.position[n2][1]], [self.position[n1][2],self.position[n2][2]], color = "red")

    def draw (self, plt3d):
	    # draw tree
        # self.showtree('0.45', plt3d)
		 
	    #draw path
        self.showpath('ro-', plt3d)
	
        # plt.show()

    def visualize_cylinder(self, plt3d, cyl, env):
        n = len(self.path)
        for i in range(n-1, -1, -1):
            plt.cla()
            n1=self.path[i]
            center = (self.position[n1][0], self.position[n1][1], self.position[n1][2])
            roll = self.orientation[n1][0]
            pitch = self.orientation[n1][1]
            yaw = self.orientation[n1][2]
            if i==0:
                roll =0
                pitch =0
                yaw = 0
            cyl.update_pose(center, roll, pitch, yaw)
            cyl.make_cylinder()
            env.make_world()
            plt.pause(0.1)
         


    def start(self, nmax, plt3d, cyl, env):
        flag = False
        for i in range(0,nmax):
            self.expand()
            if self.atgoal()==1:
                flag = True
                break
        if flag:     
            print("Reached the goal node using RRT")
            self.path_to_goal()
            self.visualize_cylinder(plt3d, cyl,env)
            # # print("Got path")
            self.draw(plt3d)
        else:
            self.draw(plt3d)
            print("Path not found")
