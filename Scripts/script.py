import random
import matplotlib.pyplot as plt

ENERGY = 1
COLUMNS = 25
ROWS = 25
NUMBER_OF_NODES = 50


def print_network():
    for inner in network:
        print(inner)   


random_list = []

# Change to None or -1
network = [[0 for x in range(ROWS)] for y in range(COLUMNS)]

for n in range(NUMBER_OF_NODES):
    
    while True:
        x = random.randint(0, COLUMNS - 1)
        y = random.randint(0, ROWS - 1)

        if (x, y) not in random_list:
            random_list.append((x, y))
            break

    #while x och y ! finns i list  
    random_list.append((x, y))
    
    network[x][y] = ENERGY
    #riskerar att dubbla koordinater i network
    
sink_node = float('inf')

network[0][0] = sink_node

print_network()

# plt.plot(network)

# plt.show()

