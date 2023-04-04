import random
import matplotlib.pyplot as plt
import math

ENERGY = 1
COLUMNS = 25
ROWS = 25
NUMBER_OF_NODES = 10

#NEW
RADIO_DIST = 3

def print_network():
    for inner in network:
        print(inner)   


random_list = []

#NEW
edge_list = []
node_energy = {}

# Change to None or -1
network = [[0 for x in range(ROWS)] for y in range(COLUMNS)]

for n in range(NUMBER_OF_NODES - 1):
    
    while True:
        x = random.randint(0, COLUMNS - 1)
        y = random.randint(0, ROWS - 1)

        if (x, y) not in random_list:
            random_list.append((x, y))
            node_energy[(x, y)] = 1
            break
    
    network[x][y] = ENERGY
    #riskerar att dubbla koordinater i network

#Node energy init


sink_node = float('inf')

network[0][0] = sink_node

node_energy[(0, 0)] = float('inf')
random_list.append((0,0))

for nodeX in random_list:
    for nodeY in random_list:
        
        if nodeX == nodeY:
            continue

        distance = math.sqrt((nodeY[0] - nodeX[0])**2 + (nodeY[1] - nodeX[1])**2)
        if  distance > RADIO_DIST:
            continue

        if not (nodeX, nodeY, distance) in edge_list:
            edge_list.append((nodeX, nodeY, distance))

print(random_list)
# print_network()
print("--------")
for x in edge_list:
    print(x)

# ALL ABOVE SET UP

print("----------")
print(node_energy)

#constants used in energy calculation
A = 1.0e-9
B = 5.0e-11
m = 4

# Equation 3, Energy transmission cost
def transsmon_eq3(distance, k):
    return (A + B * distance**m) * k

# Equation 4, Energy reseption cost
def reception_eq4(k):
    return A * k

#constants used in fuzzy lifetime membership function

ALPHA = 0.2
GAMMA = 0.9
BETA = 0.2
SIGMA = 1

# Equation 6, Fuzzy lifetime membership function
def lifetime_membership_eq6(residual_energy, distance, k):
    MAXIMUM_LIFETIME = 0
    
    current_energy = residual_energy - transsmon_eq3(distance, k)

    if ALPHA * SIGMA < current_energy and current_energy <= SIGMA:
        #lollolo
        return 1 - ((1 - GAMMA) / (1 - ALPHA)) * (1 - current_energy / SIGMA)
        
    elif transsmon_eq3(distance, k) < current_energy and current_energy <= ALPHA * SIGMA:
        condition_1 = (GAMMA) / (ALPHA * (SIGMA - transsmon_eq3(distance, k))) 
        condition_2 = current_energy - transsmon_eq3(distance, k)
        return condition_1 * condition_2

    elif current_energy <= transsmon_eq3(distance, k):
        return 0


THETA = [0.2, 0.8]

