# File: run_agent.py
# Description: Running algorithm
# Environment: PyCharm and Anaconda environment
#
# MIT License
# Copyright (c) 2018 Valentyn N Sichkar
# github.com/sichkar-valentyn
#
# Reference to:
# Valentyn N Sichkar. Reinforcement Learning Algorithms for global path planning // GitHub platform. DOI: 10.5281/zenodo.1317899



# Importing classes
from env_rl import Environment
from rl_agent_brain import QLearningTable 
from calibrated_movement import *
import warnings
warnings.filterwarnings("ignore")
n_episodes = 10

action_angle = [0, 180, 90, 270] # up, down, right, left
actions = ['up', 'down', 'right', 'left']
gyro_offsets = mpu_initialize()

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
    
def update():
    # Resulted list for the plotting Episodes via Steps
    steps = []

    # Summed costs for all episodes in resulted list
    all_costs = []

    for episode in range(n_episodes):
        # Initial Observation
        observation = env.reset()

        # Updating number of Steps for each Episode
        i = 0

        # Updating the cost for each episode
        cost = 0
        
        current_facing = 180
        
        while True:
            # Refreshing environment
            env.render()

            # RL chooses action based on observation
            action = RL.choose_action(str(observation))
            
                                    
            # RL takes an action and get the next observation and reward
            observation_, reward, done, current_facing = env.step(action, current_facing, gyro_offsets)

            # RL learns from this transition and calculating the cost
            cost += RL.learn(str(observation), action, reward, str(observation_))

            # Swapping the observations - current and next
            observation = observation_

            # Calculating number of Steps in the current Episode
            i += 1

            # Break while loop when it is the end of current Episode
            # When agent reached the goal or obstacle
            if done:
                steps += [i]
                all_costs += [cost]
                break

    # Showing the final route
    env.final()

    # Showing the Q-table with values for each action
    RL.print_q_table()

    # Plotting the results
    RL.plot_results(steps, all_costs)


# Commands to be implemented after running this file
if __name__ == "__main__":
    # Calling for the environment
    env = Environment()
    # Calling for the main algorithm
    RL = QLearningTable(actions=list(range(env.n_actions)))
    # Running the main loop with Episodes by calling the function update()
    env.after(100, update)  # Or just update()
    env.mainloop()
