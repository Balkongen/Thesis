import random
import matplotlib.pyplot as plt
import math

ENERGY = 1
COLUMNS = 25
ROWS = 25
NUMBER_OF_NODES = 10

#NEW
RADIO_DIST = 3

random_list = []
#NEW
edge_list = []
node_energy = {}

# Change to None or -1

def create_network(rows, columns, num_of_nodes, random_list, node_energy):
    for _ in range(num_of_nodes - 1):
        
        while True:
            x = random.randint(0, rows - 1)
            y = random.randint(0, columns - 1)

            if (x, y) not in random_list:
                random_list.append((x, y))
                node_energy[(x, y)] = 1
                break
        
    sink_node = float('inf')

    node_energy[(0, 0)] = sink_node
    random_list.append((0,0))
        #riskerar att dubbla koordinater i network
    
create_network(rows=ROWS, columns=COLUMNS, num_of_nodes=NUMBER_OF_NODES, random_list=random_list, node_energy=node_energy)
#Node energy init

def create_edges(edges, nodes, max_radio_distance):
    for nodeX in nodes:
        for nodeY in nodes:
            
            if nodeX == nodeY:
                continue

            distance = math.sqrt((nodeY[0] - nodeX[0])**2 + (nodeY[1] - nodeX[1])**2)
            if  distance > max_radio_distance:
                continue

            if not (nodeX, nodeY, distance) in edges:
                edges.append((nodeX, nodeY, distance))

create_edges(edges=edge_list, nodes=random_list, max_radio_distance=RADIO_DIST)



# print(random_list)
# print_network()
# print("--------")
# for x in edge_list:
#     print(x)

# ALL ABOVE SET UP

# print("----------")
# print(node_energy)

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



