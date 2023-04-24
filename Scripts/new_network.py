import random
import matplotlib.pyplot as plt
import math
import heapq

# 10 x 10 nodes.
# edge l = 2m
# continuously consume 0.0005 J
# Transmission cost 0.007 J
# init energ = 500 J
# 1000 episodes and each episode terminates when the packet is dropped
# Measure: Number of packets delivered, lost. Total energy consumed
# in whole process. Network lifetime. Number of dying nodes?


CONSTANT_ENERGY_DRAIN = 0.0005
ENERGY = 500
COLUMNS = 10
ROWS = 10
NUMBER_OF_NODES = COLUMNS * ROWS
PROBABILITY_OF_PACKET_LOST = 0.2

GRAPH_DELIVERY_RATE = []
GRAPH_ENERGY_CONSUMPTION = []
TOTAL_CONSUMPTION = []

PACKAGE_DROPPED = 0

RADIO_DIST = 1

EPISODES = 200

LIFETIME_COUNT = 0

#-----SIMULATION SET UP-------

nodes = [] # [(x-coordinate, y-coordinate), ...]

edges = [] # [(from_node, to_node, distance), ...]
# node = (x-coordinate, y-coordinate)

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node

node_to_maximum_path = {} # key = node (x-coordinate, y-coordinate). Value = maximum path to sink node

malicious_nodes = {}
malicious_nodes[(1, 5)] = 0
malicious_nodes[(2, 1)] = 0
malicious_nodes[(3, 2)] = 0
malicious_nodes[(4, 3)] = 0
malicious_nodes[(6, 5)] = 0
malicious_nodes[(7, 8)] = 0
malicious_nodes[(8, 3)] = 0

def create_network():
    
    for y in range(0, 10):
        for x in range(0,10):
            nodes.append((x, y))
            node_to_energy[(x, y)] = ENERGY
            
create_network()

def create_edges(edges, nodes, max_radio_distance):
    for node_one in nodes:
        for node_two in nodes:
            
            if node_one != node_two:
                x_dist = (node_two[0] - node_one[0])**2
                y_dist = (node_two[1] - node_one[1])**2
                c_sum = x_dist + y_dist
                dist = math.sqrt(c_sum)

                if dist <= max_radio_distance:
                    edges.append((node_one, node_two, dist))
    
    
    # for nodeX in nodes:
    #     for nodeY in nodes:
            

        


    #         if nodeX == nodeY:
    #             continue

    #         distance = math.sqrt((nodeY[0] - nodeX[0])**2 + (nodeY[1] - nodeX[1])**2)
    #         if  distance > max_radio_distance:
    #             continue

    #         if not (nodeX, nodeY, distance) in edges:
    #             edges.append((nodeX, nodeY, distance))

create_edges(edges=edges, nodes=nodes, max_radio_distance=RADIO_DIST)

#-----SIMULATION SET UP END-------

#constants used in energy calculation
TRANSMISSION_COST = 0.007
# TRANSMISSION_COST = 45

# Equation 3, Energy transmission cost
def transmission_cost():
    return TRANSMISSION_COST

def reception_cost():
    return 0 # No cost of reception

#constants used in fuzzy lifetime membership function
ALPHA = 0.2
GAMMA = 0.9
BETA = 0.2
SIGMA = ENERGY 

# Equation 6, Fuzzy lifetime membership function
def lifetime_membership_eq6(residual_energy):
    MAXIMUM_LIFETIME = 0
    
    current_energy = residual_energy - transmission_cost()

    if (ALPHA * SIGMA) < current_energy and current_energy <= SIGMA:
        return 1 - ((1 - GAMMA) / (1 - ALPHA)) * (1 - current_energy / SIGMA)
        
    elif transmission_cost() < current_energy and current_energy <= (ALPHA * SIGMA):
        condition_1 = (GAMMA) / (ALPHA * (SIGMA - transmission_cost())) 
        condition_2 = current_energy - transmission_cost()
        return condition_1 * condition_2

    elif current_energy <= transmission_cost():
        return 0
    else:
        return 1 # Sink node # TODO Är denna rätt?
    
    
THETA = [0.2, 0.8]

# Equation 7, fuzzy membership minimun delay
def minimum_delay_eq7(node):
    return 1 + (((THETA[0] - 1) * node_to_maximum_path[node]) / max(node_to_maximum_path.values())) # THETA can change based on test runs

# Här riskerar nätverkat att dö istället för o byta till väg som är längre
# Equation 10, mulitobjective membership function
def multi_objective_membership_eq10(umd, ulf):
    return (BETA * min(umd, ulf)) + ((1 - BETA) * ((umd + ulf) / 2)) 

# Equation 11, returns new value of weight of edge
def weight_assign_eq11(edge):
    residual_energy = node_to_energy[edge[1]] 
    return 1 - multi_objective_membership_eq10(lifetime_membership_eq6(residual_energy), minimum_delay_eq7(edge[1]))


# TODO ÄNDRA alternativt att fråga handledaren
# Se till att generera startnoder på så sätt att de inte startar hos en malicious node.
# Med probability
def create_routes(routes):

    for _ in range(0, EPISODES):
        index = random.randint(0, len(nodes) - 1)
        package_size = 1000 # Ask supervisor for correct reasonable size
        routes.append((nodes[index], package_size))
        

def get_shortest_path(edge_list, start_node, end_node):
   
    # print("start and end node")
    # print(start_node, end_node)
    #dictionairy where key = a node and value is the previous node when calc dijkstras
    path_nodes = {}
    path_nodes[end_node] = None
    #add source node
    #path_nodes[start_node] = None
    distances = {node: float('inf') for node,_,_ in edge_list}
    distances[start_node] = 0
    
    visited = [(0, start_node)]
    heapq.heapify(visited)
    
    while visited: # change name
       
        (curr_dist, curr_node) = heapq.heappop(visited)
        
        #stop if visiting end_node
        if curr_node == end_node:
            break

        for (from_node, to_node, w) in edge_list:
            if from_node == curr_node:
                new_dist = curr_dist + edge_list[(from_node, to_node, w)]
                # print("Distances", distances)
                # print("No node", no_node)
                # print("W", w)
                if new_dist < distances[to_node]:
                    
                    distances[to_node] = new_dist
                    #här lägger vi in föregående nod
                    path_nodes[to_node] = from_node
                    heapq.heappush(visited, (new_dist, to_node))

    # print("distances: ")
    # for i, node in enumerate(distances):
        # print(node, distances[node])
    # Creates a list of the nodes between start_node and end_node
    path = []
    
    node = end_node
    while node != start_node:
        path.append(node)
        #just in case there is no path between nodes the loop stops if the previous value is None

        if path_nodes[node] is not None:
            node = path_nodes[node]
        else:
            break

    path.append(start_node)
    path.reverse()

    return path


def send_data_and_compute_new_energy(path, k):
    global PACKAGE_DROPPED
    for node in node_to_energy: # Remove energy from all nodes.
        node_to_energy[node] = node_to_energy[node] - CONSTANT_ENERGY_DRAIN

    for index, node in enumerate(path):
        
        if index == len(path) - 1:
            return

        if node in malicious_nodes:
            # 20% chance of losing package if it's a malicious node
            if random.random() < PROBABILITY_OF_PACKET_LOST:
                # Räkna variabel
                PACKAGE_DROPPED = PACKAGE_DROPPED + 1
                return

        
        next_node = path[index + 1]
        #tmp_distance = None
        current_energy = node_to_energy[node]


        if index == 0:
            # Do Only transmission on first node
            node_to_energy[node] = current_energy - transmission_cost()
            continue
        
        #sending data
        node_to_energy[node] = current_energy - transmission_cost() - reception_cost()


def disco_disk(edge_list, start_node, end_node):
    distances = {node: float('inf') for node,_,_ in edge_list}
    distances[start_node] = 0
    
    visited = [(0, start_node)]
    heapq.heapify(visited)
    
    while visited: # change name
  
        (curr_dist, curr_node) = heapq.heappop(visited)
        
        #stop if visiting end_node
        if curr_node == end_node:
            break

    
        for (from_node, to_node, w) in edge_list:
            if from_node == curr_node:
                new_dist = curr_dist + w

                if new_dist < distances[to_node]:
                    
                    distances[to_node] = new_dist
                    #här lägger vi in föregående nod
                    heapq.heappush(visited, (new_dist, to_node))


    return distances[end_node]


def driver(end_node_input):
    for node in nodes:
        node_to_maximum_path[node] = disco_disk(edge_list=edges, start_node=node, end_node=end_node_input)
    return



def generate_sink_node():
    ix = random.randint(0, NUMBER_OF_NODES - 1)
    return nodes[ix]

def calculate_energy_consumption():
    energy_left = sum(node_to_energy.values())
    return (ENERGY * NUMBER_OF_NODES) - energy_left


def generate_same_route(routes):
    for x in range(0, 100):
        routes.append(((3,0), 0))


def main():
    #dict with edge - weight in this context
    edge_weight = {}

    # Initialize routing requests
    routing_request = []
    create_routes(routing_request)
    # generate_same_route(routing_request)

    global LIFETIME_COUNT
    
    ix = 0
    # for all routing requests
    for request in routing_request:
        LIFETIME_COUNT = LIFETIME_COUNT + 1
        # for each edge in network
        print(ix) # Counter for terminal 
        ix = ix + 1

        sink_node = generate_sink_node()
        
        driver(sink_node)

        for i, edge in enumerate(edges):
            
            #assign weight to edges and add to dict
            edge_weight[edge] = weight_assign_eq11(edge)
            
        # for i, edge in enumerate(edge_weight):
        #     print(edge , edge_weight[edge])
        
    
        # print("start node:")
        # print(request)
        
        minimum_weight_path = get_shortest_path(edge_weight, request[0], sink_node)

        #print("Start node:", request[0])
        #print("Sink node:", sink_node)
        #print("MiNI", minimum_weight_path)
    

        if len(minimum_weight_path) == 1:
            GRAPH_DELIVERY_RATE.append((LIFETIME_COUNT - PACKAGE_DROPPED) / LIFETIME_COUNT)
            GRAPH_ENERGY_CONSUMPTION.append(calculate_energy_consumption())
            continue
        else:
            send_data_and_compute_new_energy(minimum_weight_path, 1000)
            
        GRAPH_DELIVERY_RATE.append((LIFETIME_COUNT - PACKAGE_DROPPED) / LIFETIME_COUNT)
        GRAPH_ENERGY_CONSUMPTION.append(calculate_energy_consumption())

        for node in node_to_energy:
            if node_to_energy[node] <= 0:
                return LIFETIME_COUNT
            
    return LIFETIME_COUNT



if __name__ == '__main__':
    print("Packages sent: ", main())
    print("Packages delivered: ", LIFETIME_COUNT - PACKAGE_DROPPED)
    print("Dropped packages: ", PACKAGE_DROPPED)
    print("Energy consumption: ", calculate_energy_consumption())
    
    print("NODES")
    for i, node in enumerate(node_to_energy):
        print(node, node_to_energy[node])

    life = []
    for x in range(0, EPISODES):
        life.append(x)

    # DELIVERY RATE
    # plt.scatter(life, GRAPH_DELIVERY_RATE, s=[1.2])
    # plt.show()

    # ENERGY CONSUMPTION

    #plt.scatter(life, GRAPH_ENERGY_CONSUMPTION, s=[1.2])
    #plt.show()
