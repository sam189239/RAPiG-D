# File: env.py
# Description: Building the environment-1 for the Mobile Robot to explore
# Agent - Mobile Robot
# Obstacles - 'road closed', 'trees', 'traffic lights', 'buildings'
# Environment: PyCharm and Anaconda environment
#
# MIT License
# Copyright (c) 2018 Valentyn N Sichkar
# github.com/sichkar-valentyn
#
# Reference to:
# Valentyn N Sichkar. Reinforcement Learning Algorithms for global path planning // GitHub platform. DOI: 10.5281/zenodo.1317899

 

# Importing libraries
import numpy as np  # To deal with data in form of matrices
import tkinter as tk  # To build GUI
import time  # Time is needed to slow down the agent and to see how he runs
from PIL import Image, ImageTk  # For adding images into the canvas widget

# Setting the sizes for the environment
pixels = 40   # pixels
env_height = 3  # grid height
env_width = 3  # grid width

# Global variable for dictionary with coordinates for the final route
a = {}

obs_coord = []
#obs_pos = { (3,4):2, (0,2):6, (1,0):5, (3,2):2, (4,0):12, (5,3):7, (7,3):9, (6,1):10, (5,5):4, (6,5):4, 
#            (5,6):4, (5,7):4, (0,8):3, (3,7):8, (0,4):1, (8,0):3, (7,7):4, (1,6):11, (8,3):8, (7,6):4, (7,5):4, (2,3):2
#        }
obs_pos = { (1,1):2, (0,2):2}
flag_pos = [2,2]
flag_coord = flag_pos * pixels

obs_visited = []

for (x,y) in obs_pos.keys():
    obs_coord.append([x * pixels, y * pixels])


def create_obs(self,next_state):
    pos = obs_pos[next_state[0] / pixels, next_state[1] / pixels] - 1
    img = self.obstacle_object[pos]
    self.obstacle.append(self.canvas_widget.create_image(next_state[0], next_state[1], anchor='nw', image=img))

def create_flag(self):
    self.flag = self.canvas_widget.create_image(flag_coord[0], flag_coord[1], anchor='nw', image=self.flag_object)

# Creating class for the environment
class Environment(tk.Tk, object):
    def __init__(self):
        super(Environment, self).__init__()
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)
        self.title('RL Q-learning. Sichkar Valentyn')
        self.geometry('{0}x{1}'.format(env_width * pixels, env_height * pixels))
        self.build_environment()

        # Dictionaries to draw the final route
        self.d = {}
        self.f = {}

        # Key for the dictionaries
        self.i = 0

        # Writing the final dictionary first time
        self.c = True

        # Showing the steps for longest found route
        self.longest = 0

        # Showing the steps for the shortest route
        self.shortest = 0

    # Function to build the environment
    def build_environment(self):
        self.canvas_widget = tk.Canvas(self,  bg='white',
                                       height=env_height * pixels,
                                       width=env_width * pixels)

        # Creating grid lines
        for column in range(0, env_width * pixels, pixels):
            x0, y0, x1, y1 = column, 0, column, env_height * pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, env_height * pixels, pixels):
            x0, y0, x1, y1 = 0, row, env_height * pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')

        # Creating objects of  Obstacles
        # Obstacle type 1 - road closed1

        self.obstacle_object = []

        img_obstacle1 = Image.open("images/road_closed1.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle1))
        # Obstacle type 2 - tree1
        img_obstacle2 = Image.open("images/tree1.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle2))
        # Obstacle type 3 - tree2
        img_obstacle3 = Image.open("images/tree2.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle3))
        # Obstacle type 4 - building1
        img_obstacle4 = Image.open("images/building1.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle4))
        # Obstacle type 5 - building2
        img_obstacle5 = Image.open("images/building2.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle5))
        # Obstacle type 6 - road closed2
        img_obstacle6 = Image.open("images/road_closed2.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle6))
        # Obstacle type 7 - road closed3
        img_obstacle7 = Image.open("images/road_closed3.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle7))
        # Obstacle type 8 - traffic lights
        img_obstacle8 = Image.open("images/traffic_lights.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle8))
        # Obstacle type 9 - pedestrian
        img_obstacle9 = Image.open("images/pedestrian.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle9))
        # Obstacle type 10 - shop
        img_obstacle10 = Image.open("images/shop.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle10))
        # Obstacle type 11 - bank1
        img_obstacle11 = Image.open("images/bank1.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle11))
        # Obstacle type 12 - bank2
        img_obstacle12 = Image.open("images/bank2.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle12))

        # Creating obstacles themselves
        # Obstacles from 1 to 22

        self.obstacle = []

        # Final Point
        img_flag = Image.open("images/flag.png")
        self.flag_object = ImageTk.PhotoImage(img_flag)
        self.flag = self.canvas_widget.create_image(pixels * flag_coord[0], pixels * flag_coord[1], anchor='nw', image=self.flag_object)

        # Uploading the image of Mobile Robot
        img_robot = Image.open("images/agent1.png")
        self.robot = ImageTk.PhotoImage(img_robot)

        # Creating an agent with photo of Mobile Robot
        self.agent = self.canvas_widget.create_image(0, 0, anchor='nw', image=self.robot)
#        self.flag = self.canvas_widget.create_image(flag_coord[0], flag_coord[1], anchor='nw', image=self.flag_object)
        # Packing everything
        self.canvas_widget.pack()

    # Function to reset the environment and start new Episode
    def reset(self):
        self.update()
        #time.sleep(0.1)

        # Updating agent
        self.canvas_widget.delete(self.agent)
        self.agent = self.canvas_widget.create_image(0, 0, anchor='nw', image=self.robot)

        # # Clearing the dictionary and the i
        self.d = {}
        self.i = 0

        # Return observation
        return self.canvas_widget.coords(self.agent)

    # Function to get the next observation and reward by doing next step
    def step(self, action):
        # Current state of the agent
        state = self.canvas_widget.coords(self.agent)
        base_action = np.array([0, 0])

        # Updating next state according to the action
        # Action 'up'
        if action == 0:
            if state[1] >= pixels:
                base_action[1] -= pixels
        # Action 'down'
        elif action == 1:
            if state[1] < (env_height - 1) * pixels:
                base_action[1] += pixels
        # Action right
        elif action == 2:
            if state[0] < (env_width - 1) * pixels:
                base_action[0] += pixels
        # Action left
        elif action == 3:
            if state[0] >= pixels:
                base_action[0] -= pixels

        # Moving the agent according to the action
        self.canvas_widget.move(self.agent, base_action[0], base_action[1])

        # Writing in the dictionary coordinates of found route
        self.d[self.i] = self.canvas_widget.coords(self.agent)

        # Updating next state
        next_state = self.d[self.i]

        # Updating key for the dictionary
        self.i += 1

        # Calculating the reward for the agent
        if next_state == self.canvas_widget.coords(self.flag):
            reward = 1
            done = True
            next_state = 'goal'

            # create_flag(self)

            # Filling the dictionary first time
            if self.c == True:
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]
                self.c = False
                self.longest = len(self.d)
                self.shortest = len(self.d)

            # Checking if the currently found route is shorter
            if len(self.d) < len(self.f):
                # Saving the number of steps for the shortest route
                self.shortest = len(self.d)
                # Clearing the dictionary for the final route
                self.f = {}
                # Reassigning the dictionary
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]

            # Saving the number of steps for the longest route
            if len(self.d) > self.longest:
                self.longest = len(self.d)

        elif next_state in obs_coord:
            if next_state not in obs_visited:
                create_obs(self, next_state)
                obs_visited.append(next_state)

            reward = -1
            done = True
            next_state = 'obstacle'

            # Clearing the dictionary and the i
            self.d = {}
            self.i = 0

        else:
            reward = 0
            done = False

        return next_state, reward, done

    # Function to refresh the environment
    def render(self):
        #time.sleep(0.03)
        self.update()

    # Function to show the found route
    def final(self):
        # Deleting the agent at the end
        self.canvas_widget.delete(self.agent)

        # Showing the number of steps
        print('The shortest route:', self.shortest)
        print('The longest route:', self.longest)

        # Creating initial point
        origin = np.array([20, 20])
        self.initial_point = self.canvas_widget.create_oval(
            origin[0] - 5, origin[1] - 5,
            origin[0] + 5, origin[1] + 5,
            fill='blue', outline='blue')

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            print(self.f[j])
            self.track = self.canvas_widget.create_oval(
                self.f[j][0] + origin[0] - 5, self.f[j][1] + origin[0] - 5,
                self.f[j][0] + origin[0] + 5, self.f[j][1] + origin[0] + 5,
                fill='blue', outline='blue')
            # Writing the final route in the global variable a
            a[j] = self.f[j]


# Returning the final dictionary with route coordinates
# Then it will be used in agent_brain.py
def final_states():
    return a


# This we need to debug the environment
# If we want to run and see the environment without running full algorithm
if __name__ == '__main__':
    env = Environment()
    env.mainloop()
