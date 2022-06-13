# Importing libraries
import numpy as np  # To deal with data in form of matrices
import tkinter as tk  # To build GUI
import time  # Time is needed to slow down the agent and to see how he runs
from PIL import Image, ImageTk  # For adding images into the canvas widget
import sys
sys.path.append("../")
# from linear_test import *

import requests
def send_to_flask(step, episode, m, action):
    data = {'step':step, 'ep':episode, 'map':m, 'action':action}
    r = requests.post("http://localhost:8000", data = data)
    

# Setting the sizes for the environment
pixels = 40   # pixels
env_height = 3  # grid height
env_width = 3 # grid width

# Global variable for dictionary with coordinates for the final route
a = {}


obs_coord = []
obs_pos = {(2,1):2, (0,1):2}
flag_pos = [2,2]
flag_coord = flag_pos * pixels

for (x,y) in obs_pos.keys():
    obs_coord.append([x * pixels, y * pixels])

obs_visited = []
actions = ['up', 'down', 'right', 'left']
action_angle = [0, 180, 90, 270] # up, down, right, left

def move_one_f():
    print("Moved one forward")

def turn_required(action, current_facing):
    reqd_facing = action_angle[action]
    i = (current_facing - reqd_facing) / 90    
    if i == 0:
        pass
    elif i>0:
        while i>0:
            left_mpu(gyro_offsets)
            i -= 1
            current_facing = reqd_facing
    else:
        while i<0:
            right_mpu(gyro_offsets)      
            i += 1
            current_facing = reqd_facing
    return current_facing


def is_obstacle():
    global threshold
    global current_depth

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= 0,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)

    is_obj = check_if_object(depth)

def create_obs(self,next_state):
    pos = obs_pos[next_state[0] / pixels, next_state[1] / pixels] - 1
    img = self.obstacle_object[pos]
    self.obstacle.append(self.canvas_widget.create_image(next_state[0], next_state[1], anchor='nw', image=img))


# Creating class for the environment
class Environment(tk.Tk, object):
    def __init__(self):
        super(Environment, self).__init__()
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)
        self.title('RL Path Planning')
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

        img_obstacle2 = Image.open("../images/tree1.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle2))
        # Obstacle type 3 - tree2
        img_obstacle3 = Image.open("../images/tree2.png")
        self.obstacle_object.append(ImageTk.PhotoImage(img_obstacle3))
        
        self.obstacle = []

        # Final Point
        img_flag = Image.open("../images/flag.png")
        self.flag_object = ImageTk.PhotoImage(img_flag)
        self.flag = self.canvas_widget.create_image(pixels * flag_coord[0], pixels * flag_coord[1], anchor='nw', image=self.flag_object)

        # Agent
        img_robot = Image.open("../images/agent1.png")
        self.robot = ImageTk.PhotoImage(img_robot)
        self.agent = self.canvas_widget.create_image(0, 0, anchor='nw', image=self.robot)

        # Packing everything
        self.canvas_widget.pack()

    # Function to reset the environment and start new Episode
    def reset(self):
        self.update()
        #time.sleep(0.1)
        input("Reset bot and press enter... ")
        # Updating agent
        self.canvas_widget.delete(self.agent)
        self.agent = self.canvas_widget.create_image(0, 0, anchor='nw', image=self.robot)

        # # Clearing the dictionary and the i
        self.d = {}
        self.i = 0

        # Return observation
        return self.canvas_widget.coords(self.agent)
        
    def step(self, action, current_facing):
        # Current state of the agent
        state = self.canvas_widget.coords(self.agent)
        base_action = np.array([0, 0])
        
        ## obs = is_obstacle()
        
        # Action 'up'
        if action == 0:
            if state[1] >= pixels:
                base_action[1] -= pixels
                # current_facing = turn_required(action, current_facing)
                print("Turned " + actions[action])
        # Action 'down'
        elif action == 1:
            if state[1] < (env_height - 1) * pixels:
                base_action[1] += pixels
                # current_facing = turn_required(action, current_facing)
                print("Turned " + actions[action])
        # Action right
        elif action == 2:
            if state[0] < (env_width - 1) * pixels:
                base_action[0] += pixels
                # current_facing = turn_required(action, current_facing)
                print("Turned " + actions[action])
        # Action left
        elif action == 3:
            if state[0] >= pixels:
                base_action[0] -= pixels
                # current_facing = turn_required(action, current_facing)
                print("Turned " + actions[action])
                
        # Moving the agent according to the action
        self.canvas_widget.move(self.agent, base_action[0], base_action[1])
	
        next_posn = self.canvas_widget.coords(self.agent)

        # Calculating the reward for the agent
        ## if not obs and next_posn == self.canvas_widget.coords(self.flag):
        if next_posn == self.canvas_widget.coords(self.flag):
            reward = 1
            done = True
            next_state = 'goal'

            print("Goal Reached")

            # move and update dict
            move_one_f()
            self.d[self.i] = self.canvas_widget.coords(self.agent)
        
            # Updating next state
            #next_state = self.d[self.i]

            # Updating key for the dictionary
            self.i += 1
           
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

        ## elif obs:
        elif next_posn in obs_coord:
            
            self.canvas_widget.move(self.agent, -base_action[0], -base_action[1])

            if next_posn not in obs_visited:
                create_obs(self, next_posn)
                obs_visited.append(next_posn)
            
            print("Obstacle detected")
            
            reward = -1
            done = True
            next_state = 'obstacle'

            # Clearing the dictionary and the i
            self.d = {}
            self.i = 0

        else:
            if state != next_posn:
                # move and update dict
                move_one_f()
                self.d[self.i] = self.canvas_widget.coords(self.agent)
                self.i += 1
            next_state = next_posn
            reward = 0
            done = False

        return next_state, reward, done, current_facing

    # Function to get the next observation and reward by doing next step
    def step_old(self, action):
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

            # create_flag(self, next_state)

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



