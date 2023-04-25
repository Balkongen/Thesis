import random
import matplotlib.pyplot as plt
import math
import heapq

# edge l = 2m

# Network environment settings

CONSTANT_ENERGY_DRAIN = 0.0005
MINIMUM_START_ENERGY = 0.7
ENERGY = 1
COLUMNS = 10
ROWS = 10
NUMBER_OF_NODES = COLUMNS * ROWS
PROBABILITY_OF_PACKET_LOST = 0.2

RADIO_DIST = 1
EPISODES = 1000

graph_delivery_rate = []
graph_energy_consumption = []
total_consumption = []

package_dropped = 0
lifetime_count = 0

#-----SIMULATION SET UP-------

nodes = [] # [(x-coordinate, y-coordinate), ...]

edges = [] # [(from_node, to_node, distance), ...]
# node = (x-coordinate, y-coordinate)

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node

node_to_maximum_path = {} # key = node (x-coordinate, y-coordinate). Value = maximum path to sink node

malicious_nodes = {} # comment out nodes for different tests
malicious_nodes[(1, 5)] = 0
malicious_nodes[(2, 1)] = 0
malicious_nodes[(3, 2)] = 0
malicious_nodes[(4, 3)] = 0
malicious_nodes[(5, 4)] = 0
malicious_nodes[(6, 5)] = 0
malicious_nodes[(7, 8)] = 0
malicious_nodes[(8, 3)] = 0


def create_network():
    
    for y in range(0, 10):
        for x in range(0,10):
            nodes.append((x, y))
            node_to_energy[(x, y)] = random.uniform(MINIMUM_START_ENERGY, ENERGY)
            
create_network()


def create_edges(edges, nodes, max_radio_distance):
    for node_one in nodes:
        for node_two in nodes:
            
            if node_one != node_two:
                x_dist = (node_two[0] - node_one[0])**2
                y_dist = (node_two[1] - node_one[1])**2
                x_y_diff = x_dist + y_dist
                distance = math.sqrt(x_y_diff)
    
                if distance <= max_radio_distance:
                    edges.append((node_one, node_two, distance))
    
    
create_edges(edges=edges, nodes=nodes, max_radio_distance=RADIO_DIST)

#-----SIMULATION SET UP END-------

#constants used in energy calculation
TRANSMISSION_COST = 0.007
# TRANSMISSION_COST = 45

def transmission_cost():
    return TRANSMISSION_COST

def reception_cost():
    return 0 # No cost of reception

#constants used in fuzzy lifetime membership function
ALPHA = 0.2
GAMMA = 0.9
BETA = 0.2
SIGMA = ENERGY 
THETA = [0.2, 0.8]

# Equation 6, Fuzzy lifetime membership function
def lifetime_membership_eq6(residual_energy):
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
        return 1 # Sink node 
    
    
# Equation 7, fuzzy membership minimun delay
def minimum_delay_eq7(node):
    return 1 + (((THETA[0] - 1) * node_to_maximum_path[node]) / max(node_to_maximum_path.values())) # THETA can change based on test runs


# The network is at risk of not proiritizing lifetime that shortest path sometimes
# Equation 10, mulitobjective membership function
def multi_objective_membership_eq10(umd, ulf):
    return (BETA * min(umd, ulf)) + ((1 - BETA) * ((umd + ulf) / 2)) 


# Equation 11, returns new value of weight of edge
def weight_assign_eq11(edge):
    residual_energy = node_to_energy[edge[1]] 
    return 1 - multi_objective_membership_eq10(lifetime_membership_eq6(residual_energy), minimum_delay_eq7(edge[1]))


def create_routes(routes):
    for _ in range(0, EPISODES):

        index = random.randint(0, len(nodes) - 1)
        routes.append(nodes[index])
        

def get_shortest_path(edge_list, start_node, end_node):
   
    #dictionairy where key = a node and value is the previous node when calc dijkstras
    path_nodes = {}
    path_nodes[end_node] = None

    distances = {node: float('inf') for node,_,_ in edge_list}
    distances[start_node] = 0
    
    unvisited_known_nodes = [(0, start_node)]
    heapq.heapify(unvisited_known_nodes)
    
    while unvisited_known_nodes: # change name
       
        (curr_dist, curr_node) = heapq.heappop(unvisited_known_nodes)
        
        #stop if visiting end_node
        if curr_node == end_node:
            break

        for (from_node, to_node, w) in edge_list:
            if from_node == curr_node:
                new_dist = curr_dist + edge_list[(from_node, to_node, w)]

                if new_dist < distances[to_node]:
                    
                    distances[to_node] = new_dist
           
                    path_nodes[to_node] = from_node
                    heapq.heappush(unvisited_known_nodes, (new_dist, to_node))

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


def send_data_and_compute_new_energy(path):
    global package_dropped
    
    for node in node_to_energy: # Remove energy from all nodes.
        node_to_energy[node] = node_to_energy[node] - CONSTANT_ENERGY_DRAIN

    for index, node in enumerate(path):
        
        if index == len(path) - 1:
            return

        if node in malicious_nodes:
            # 20% chance of losing package if it's a malicious node
            if random.random() < PROBABILITY_OF_PACKET_LOST:
                package_dropped = package_dropped + 1
                return

        current_energy = node_to_energy[node]

        if index == 0:
            # Do Only transmission on first node
            node_to_energy[node] = current_energy - transmission_cost()
            continue
        
        # Send data
        node_to_energy[node] = current_energy - transmission_cost() - reception_cost()


def shortest_distance_to_sink(edge_list, start_node, end_node):
    distances = {node: float('inf') for node,_,_ in edge_list}
    distances[start_node] = 0
    
    unvisited_known_nodes = [(0, start_node)]
    heapq.heapify(unvisited_known_nodes)
    
    while unvisited_known_nodes: # change name
  
        (curr_dist, curr_node) = heapq.heappop(unvisited_known_nodes)
        
        #stop if visiting end_node
        if curr_node == end_node:
            break

        for (from_node, to_node, w) in edge_list:
            if from_node == curr_node:
                new_dist = curr_dist + w

                if new_dist < distances[to_node]:
                    
                    distances[to_node] = new_dist
                    heapq.heappush(unvisited_known_nodes, (new_dist, to_node))

    return distances[end_node]


def calculate_distances_to_sink(end_node_input):
    for node in nodes:
        node_to_maximum_path[node] = shortest_distance_to_sink(edge_list=edges, start_node=node, end_node=end_node_input)


def generate_sink_node():
    ix = random.randint(0, NUMBER_OF_NODES - 1)
    return nodes[ix]

def calculate_energy_consumption():
    energy_left = sum(node_to_energy.values())
    return (ENERGY * NUMBER_OF_NODES) - energy_left


def main():
    #dict with edge - weight in this context
    edge_weight = {} # Key = edge, value = weight

    # Initialize routing requests
    routing_request = []
    create_routes(routing_request)
   
    global lifetime_count
    
    ix = 0 # Counter for terminal window
    
    for request in routing_request:
        lifetime_count = lifetime_count + 1
        
        if ix % 10 == 0:
            print(ix) 
        ix = ix + 1

        sink_node = generate_sink_node()
        
        calculate_distances_to_sink(sink_node)

        for _, edge in enumerate(edges):
            
            #assign weight to edges and add to dict
            edge_weight[edge] = weight_assign_eq11(edge)
            
        minimum_weight_path = get_shortest_path(edge_weight, request, sink_node)    

        if len(minimum_weight_path) == 1:
            graph_delivery_rate.append((lifetime_count - package_dropped) / lifetime_count)
            graph_energy_consumption.append(calculate_energy_consumption())
            continue
        else:
            send_data_and_compute_new_energy(minimum_weight_path)
            
        graph_delivery_rate.append((lifetime_count - package_dropped) / lifetime_count)
        graph_energy_consumption.append(calculate_energy_consumption())

        for node in node_to_energy:
            if node_to_energy[node] <= 0:
                return lifetime_count
            
    return lifetime_count


if __name__ == '__main__':
    print("Packages sent: ", main())
    print("Packages delivered: ", lifetime_count - package_dropped)
    print("Dropped packages: ", package_dropped)
    print("Energy consumption: ", calculate_energy_consumption())
    print("Energy efficiency: ", (lifetime_count - package_dropped) / calculate_energy_consumption())
    
    print("NODES")
    for i, node in enumerate(node_to_energy):
        print(node, node_to_energy[node])

    life = []
    for x in range(0, lifetime_count):
        life.append(x)

    # Uncomment to see plots

    # DELIVERY RATE
    # plt.plot(life, GRAPH_DELIVERY_RATE)
    # plt.show()

    # ENERGY CONSUMPTION
    # plt.plot(life, GRAPH_ENERGY_CONSUMPTION)
    # plt.show()
