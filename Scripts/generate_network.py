import random
import matplotlib.pyplot as plt

ENERGY = 1
COLUMNS = 25
ROWS = 25
NUMBER_OF_NODES = 40

#NEW
RADIO_DIST = 3

#-----SiMULATION SET UP-------

nodes = [] # [(x-coordinate, y-coordinate), ...]
#NEW

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node

# Change to None or -1

def create_network(rows, columns, num_of_nodes, nodes, node_energy):
    for _ in range(num_of_nodes - 1):
        
        while True:
            x = random.randint(0, rows - 1)
            y = random.randint(0, columns - 1)

            if (x, y) not in nodes:
                nodes.append((x, y))
                node_energy[(x, y)] = 1
                break
        
    sink_node = float('inf')

    # node_to_energy[(0, 0)] = sink_node
    # nodes.append((0,0))
        #riskerar att dubbla koordinater i network
    
create_network(rows=ROWS, columns=COLUMNS, num_of_nodes=NUMBER_OF_NODES, nodes=nodes, node_energy=node_to_energy)
#Node energy init

nodes_x = []
nodes_y = []

for x in nodes:
    nodes_x.append(x[0])
    nodes_y.append(x[1])

plt.scatter(nodes_x, nodes_y, c='black')

plt.scatter([0],[0], c='red')
plt.xlim(-1, 25)
plt.ylim(-1, 25)
plt.title("Network Topology")

plt.show()
