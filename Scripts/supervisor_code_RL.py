"""
Algorithm based on work done by Bouzid et al. (2020). Implemented by our supervisor: Shubham Vaishnav.

Bouzid, S. E., Serrestou, Y., Raoof, K., & Omri, M. N. (2020). Efficient routing protocol for wireless sensor network based on reinforcement learning. In 2020 5th International Conference on Advanced Technologies for Signal and Image Processing (ATSIP) (pp. 1-5). IEEE. 10.1109/ATSIP49331.2020.9231883

"""

#INITIALIZATION AND ENVIRONMENT SETUP
#import libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams['figure.dpi'] = 90
plt.rcParams.update({'font.size': 12})

#define the shape of the environment (i.e., its states)
environment_rows = 10
environment_columns = 10

number_of_episodes = 1000
transmission_energy_cost = 0.007    # the amount of energy(mJ) consumed by a node to receive and forward a packet to 1 hop distance
active_mode_energy_cost = 0.0005    #the amount of energy(mj) cosumed by a node for being in active mode
initial_node_energy = 0.7

num_malicious_rows = 8

#define actions
#numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

#Define the environment and its functions
class WSN():
  def __init__(self, Q = None):
    self.Q = Q
  
  #define a function that simulate the function of SDN and control the behaviour of nodes
  def get_reward(self,row, column):
    #Create a 2D numpy array to hold the rewards for each state. 
    #The array contains 10 rows and 10 columns (to match the shape of the environment), and each value is initialized to -1.
    rewards = np.full((environment_rows, environment_columns), -1.)
    rewards[9, 9] = 1. #set the reward for the destination node (i.e., the goal) to 1

    #define malicious node(8 nodes) locations for rows 0 through 9
    malicious = {} #store locations in a dictionary
    # malicious[1] = [5, 4, 8]
    # malicious[2] = [1, 5, 3]
    # malicious[3] = [2, 6]
    # malicious[4] = [3, 1]
    # malicious[5] = [4, 8]
    # malicious[6] = [5, 3]
    # malicious[7] = [8, 2]
    # malicious[8] = [3, 6]

    malicious[1] = [3,5]
    malicious[2] = [1,6]
    malicious[3] = [2,5]
    malicious[4] = [3,6]
    malicious[5] = [2]
    malicious[6] = [5,7]
    malicious[7] = [7,8]
    malicious[8] = [1,3]
    

    #set the rewards for all malicious node
    for row_index in range(1, num_malicious_rows+1):
      for column_index in malicious[row_index]: 
        rewards[row_index, column_index] = -2.
    
    return rewards[row, column]
  
  #define a function that determines if the specified location is a terminal state(either a malicious node or the destination node)
  def is_terminal_state(self, current_row_index, current_column_index):
    #if the reward for this location is -1, then it is not a terminal state
    if self.get_reward(current_row_index, current_column_index) == -1.:
      return False
    else:
      return True

  #define a function that will choose a random, non-terminal starting location
  def get_starting_location(self):
    #get a random row and column index
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
    #continue choosing random row and column indexes until a non-terminal state is identified
    #(i.e., until the chosen state is a 'normal node').
    while self.is_terminal_state(current_row_index, current_column_index):
      current_row_index = np.random.randint(environment_rows)
      current_column_index = np.random.randint(environment_columns)
    return current_row_index, current_column_index

  #define an epsilon greedy algorithm that will choose which action to take next
  def get_next_action(self, current_row_index, current_column_index, epsilon):
    if np.random.random() > epsilon:
      return np.argmax(self.Q[current_row_index, current_column_index])
    else: #choose a random action
      return np.random.randint(4)
  
  #define a function that will get the next location based on the chosen action
  def get_next_location(self, current_row_index, current_column_index, action_index):
    new_row_index = current_row_index
    new_column_index = current_column_index
    if actions[action_index] == 'up' and current_row_index > 0:
      new_row_index -= 1
    elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
      new_column_index += 1
    elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
      new_row_index += 1
    elif actions[action_index] == 'left' and current_column_index > 0:
      new_column_index -= 1
    return new_row_index, new_column_index


def R2LTO(epsilone = 0, discount_factor = 0.2, learning_rate = 0.9):
    
    q_values3 = np.zeros((environment_rows, environment_columns, 4))
    env = WSN(Q= q_values3)
    
    packet_delivery = []
    t_energy = []
    alive = []
    lifetime = []
    total_network_lifetime = 0
    

    path_lenght = 0        
    nb_success = 0
    total_energy = 0 
    #hop = 0
    alive_node = 100

    initial_energy = np.full((environment_rows, environment_columns),initial_node_energy)

    #run through 1000 training episodes
    for episode in range(number_of_episodes):
        #get the starting location for this episode
      row_index, column_index = env.get_starting_location()
      

      #initialize the consumed energy to zero for the curretn episode
      energy = 0
      path_lenght = 0

      #continue taking actions (i.e., moving) until we reach a terminal state
      #(i.e., until we reach the item packaging area or crash into an item storage location)
      while not env.is_terminal_state(row_index, column_index):
          #choose which action to take (i.e., where to move next)
          action_index = env.get_next_action(row_index, column_index, epsilone)

          #perform the chosen action, and transition to the next state (i.e., move to the next location)
          old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
          row_index, column_index = env.get_next_location(row_index, column_index, action_index)
    
          #calculate the reward for moving to the new state
          reward = env.get_reward(row_index, column_index)
          hop = 18-row_index-column_index
          R = initial_energy[row_index, column_index]/(hop+1)

    
          old_q_value = q_values3[old_row_index, old_column_index, action_index]
          temporal_difference = R + (discount_factor * np.max(q_values3[row_index, column_index])) - old_q_value

          #update the Q-value for the previous state and action pair
          new_q_value = old_q_value + (learning_rate * temporal_difference)
          q_values3[old_row_index, old_column_index, action_index] = new_q_value

          initial_energy -= active_mode_energy_cost
    
          initial_energy[old_row_index, old_column_index] -= transmission_energy_cost

           # add one step to path lenght
          path_lenght += 1
          total_network_lifetime += 1

          # if the energy level of any node is zero or less, it means that the node is died
          for row in range(environment_rows):
            for column in range(environment_columns):
              if initial_energy[row, column] <= 0:
                lifetime.append(total_network_lifetime) 

          # If we have a reward, it means that our outcome is a success
          if reward == 1:
              nb_success += 1
          
      alive.append(alive_node)
      packet_delivery.append(nb_success/(episode+1))
      energy = path_lenght*transmission_energy_cost + 100*path_lenght*active_mode_energy_cost

      total_energy += energy
      t_energy.append(total_energy)

    if len(lifetime) == 0:
      lifetime.append(1000)


    life = []
    for x in range(number_of_episodes):
      life.append(x)
      
    print('R2LTO Training complete!')
    print('number of packet delivered:', nb_success)
    print("delivery rate: ", nb_success/episode)
    print("Energy : ", total_energy)
    print("Energy efficiency: ", nb_success / total_energy)
    print("Lifetime: ", lifetime[0])

    plt.plot(life, t_energy)
    plt.show()
   
    plt.plot(life, packet_delivery)
    plt.show()
   
    return(packet_delivery, t_energy, alive)

R2LTO()