import random
import matplotlib.pyplot as plt

ENERGY = 1
COLUMNS = 10
ROWS = 10
NUMBER_OF_NODES = 100

#NEW
RADIO_DIST = 3

#-----SiMULATION SET UP-------

nodes = [] # [(x-coordinate, y-coordinate), ...]
#NEW

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node

def create_network():
    
    for y in range(0, 10):
        for x in range(0,10):
            nodes.append((x, y))
            # node_to_energy[(x, y)] = random.uniform(initial_node_energy, ENERGY)
            node_to_energy[(x, y)] = ENERGY
            
create_network()

nodes_x = []
nodes_y = []

for node in nodes:
    nodes_x.append(node[0])
    nodes_y.append(node[1])

sink_x, sink_y = nodes[len(nodes) - 1]

plt.scatter(nodes_x, nodes_y, c='black')
plt.scatter([sink_x], [sink_y], c='red')

plt.xlim(-1, 10)
plt.ylim(-1, 10)
plt.title("Network Topology")
plt.show()

