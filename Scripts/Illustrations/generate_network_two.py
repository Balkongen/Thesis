import matplotlib.pyplot as plt

ENERGY = 1
COLUMNS = 10
ROWS = 10
NUMBER_OF_NODES = 100

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

# Malicious nodes
plt.scatter([1], [5], c='yellow')
plt.scatter([1], [3], c='yellow')
plt.scatter([2], [1], c='yellow')
plt.scatter([2], [6], c='yellow')
plt.scatter([3], [2], c='yellow')
plt.scatter([3], [5], c='yellow')
plt.scatter([4], [3], c='yellow')
plt.scatter([4], [6], c='yellow')
plt.scatter([5], [2], c='yellow')
plt.scatter([6], [5], c='yellow')
plt.scatter([6], [7], c='yellow')
plt.scatter([7], [8], c='yellow')
plt.scatter([7], [7], c='yellow')
plt.scatter([8], [3], c='yellow')
plt.scatter([8], [1], c='yellow')



plt.xlim(-1, 10)
plt.ylim(-1, 10)
plt.title("Network Topology")
plt.show()