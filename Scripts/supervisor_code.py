# Fuzzy logic based algorithm implementation
import random
import matplotlib.pyplot as plt
import math
import heapq

# edge l = 2m

# Network environment settings
#constants used in energy calculation
# transmission_energy_cost = 45
number_of_episodes = 1000
EPISODES = number_of_episodes
PROBABILITY_OF_PACKET_LOST = 1.0 # Blackhole attack

#define the shape of the environment (i.e., its states)
environment_rows = 10
environment_columns = 10

transmission_energy_cost = 0.007    # the amount of energy(mJ) consumed by a node to receive and forward a packet to 1 hop distance
active_mode_energy_cost = 0.0005    #the amount of energy(mj) cosumed by a node for being in active mode
initial_node_energy = 0.7

num_malicious_rows = 8
fuzzyMaliciousNodes = {} # comment out nodes for different tests
fuzzyMaliciousNodes[(1, 5)] = 0
fuzzyMaliciousNodes[(1, 3)] = 0
fuzzyMaliciousNodes[(2, 1)] = 0
fuzzyMaliciousNodes[(2, 6)] = 0
fuzzyMaliciousNodes[(3, 2)] = 0
fuzzyMaliciousNodes[(3, 5)] = 0
fuzzyMaliciousNodes[(4, 3)] = 0
fuzzyMaliciousNodes[(4, 6)] = 0
fuzzyMaliciousNodes[(5, 2)] = 0
fuzzyMaliciousNodes[(6, 5)] = 0
fuzzyMaliciousNodes[(6, 7)] = 0
fuzzyMaliciousNodes[(7, 8)] = 0
fuzzyMaliciousNodes[(7, 7)] = 0
fuzzyMaliciousNodes[(8, 3)] = 0
fuzzyMaliciousNodes[(8, 1)] = 0




maliciousNodesKeys = fuzzyMaliciousNodes.keys()

####### No need to change #######################

COLUMNS = 10
ROWS = 10
NUMBER_OF_NODES = COLUMNS * ROWS
RADIO_DIST = 1


graph_delivery_rate = []
graph_energy_consumption = []
total_consumption = []

package_dropped = 0
sent_packet_count = 0
lifetime = []
path_lenght = 0

#-----SIMULATION SET UP-------

nodes = [] # [(x-coordinate, y-coordinate), ...]

edges = [] # [(from_node, to_node, distance), ...]
# node = (x-coordinate, y-coordinate)

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node

node_to_maximum_path = {} # key = node (x-coordinate, y-coordinate). Value = maximum path to sink node


def create_network():
    
    for y in range(0, 10):
        for x in range(0,10):
            nodes.append((x, y))
            # node_to_energy[(x, y)] = random.uniform(initial_node_energy, ENERGY)
            node_to_energy[(x, y)] = initial_node_energy
            
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


def reception_cost():
    return 0 # No cost of reception

#constants used in fuzzy lifetime membership function
ALPHA = 0.2
GAMMA = 0.9
BETA = 0.2
SIGMA = initial_node_energy 
THETA = [0.2, 0.8]

# Equation 6, Fuzzy lifetime membership function
def lifetime_membership_eq6(residual_energy):
    current_energy = residual_energy - transmission_energy_cost

    if (ALPHA * SIGMA) < current_energy and current_energy <= SIGMA:
        return 1 - ((1 - GAMMA) / (1 - ALPHA)) * (1 - current_energy / SIGMA)
        
    elif transmission_energy_cost < current_energy and current_energy <= (ALPHA * SIGMA):
        
        condition_1 = (GAMMA) / (ALPHA * (SIGMA - transmission_energy_cost)) 
        condition_2 = current_energy - transmission_energy_cost
        return condition_1 * condition_2

    elif current_energy <= transmission_energy_cost:
        return 0
    else:
        return 1 # Sink node 
    
    
# Equation 7, fuzzy membership minimun delay
def minimum_delay_eq7(node):
    return 1 + (((THETA[1] - 1) * node_to_maximum_path[node]) / max(node_to_maximum_path.values())) # THETA can change based on test runs


# The network is at risk of not proiritizing lifetime that shortest path sometimes
# Equation 10, mulitobjective membership function
def multi_objective_membership_eq10(umd, ulf):
    return (BETA * min(umd, ulf)) + ((1 - BETA) * ((umd + ulf) / 2)) 


# Equation 11, returns new value of weight of edge
def weight_assign_eq11(edge):
    residual_energy = node_to_energy[edge[1]] 
    return 1 - multi_objective_membership_eq10(lifetime_membership_eq6(residual_energy), minimum_delay_eq7(edge[1]))


def create_source_nodes_list(routes):
    for _ in range(0, EPISODES):

        index = random.randint(0, len(nodes) - 2)
        routes.append(nodes[index])
        

def get_shortest_path(edge_list, start_node, end_node):
   
    #dictionairy where key = a node and value is the previous node when calc dijkstras
    path_nodes = {}
    path_nodes[end_node] = None

    distances = {node: float('inf') for node,_,_ in edge_list}
    distances[start_node] = 0
    
    unvisited_known_nodes = [(0, start_node)]
    heapq.heapify(unvisited_known_nodes)
    
    while unvisited_known_nodes: 
       
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


def send_data_and_compute_new_energy(path, fuzzy_total_network_lifetime):
    global package_dropped
    path_lenght = 0

    for index, current_node in enumerate(path):
        # add one step to path lenght
        
        path_lenght += 1
        fuzzy_total_network_lifetime += 1

        # if the energy level of any node is zero or less, it means that the node is died
        for node in node_to_energy:
            if node_to_energy[node] <= 0:
              lifetime.append(fuzzy_total_network_lifetime) 

        for node in node_to_energy: # Remove energy from all nodes.
          node_to_energy[node] = node_to_energy[node] - active_mode_energy_cost

        if index == len(path) - 1:
          
            return fuzzy_total_network_lifetime

        if current_node in maliciousNodesKeys:
            # Blackhole Attack
            package_dropped = package_dropped + 1
            return fuzzy_total_network_lifetime

            # Selective Forwarding Attack
            # if random.random() < PROBABILITY_OF_PACKET_LOST:
            #     package_dropped = package_dropped + 1
            #     return fuzzy_total_network_lifetime


        current_energy = node_to_energy[current_node]

        if index == 0:
            # Do Only transmission on first node
            node_to_energy[current_node] = current_energy - transmission_energy_cost
            continue
        
        # Send data
        node_to_energy[current_node] = current_energy - transmission_energy_cost - reception_cost()
    return fuzzy_total_network_lifetime


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
    # ix = random.randint(0, NUMBER_OF_NODES - 1)
    return nodes[NUMBER_OF_NODES - 1]

def calculate_energy_consumption():
    energy_left = sum(node_to_energy.values())
    return (initial_node_energy * NUMBER_OF_NODES) - energy_left


def main():
    #dict with edge - weight in this context
    edge_weight = {} # Key = edge, value = weight

    # Initialize routing requests
    routing_request = []
    create_source_nodes_list(routing_request)
   
    global sent_packet_count
    global fuzzy_total_network_lifetime
    fuzzy_total_network_lifetime = 0
    
    ix = 0 # Counter for terminal window
    
    for request in routing_request: # Iterate for different source nodes
        sent_packet_count = sent_packet_count + 1
        
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
            graph_delivery_rate.append((sent_packet_count - package_dropped) / sent_packet_count)
            graph_energy_consumption.append(calculate_energy_consumption())
            continue
        else:
            fuzzy_total_network_lifetime = send_data_and_compute_new_energy(minimum_weight_path, fuzzy_total_network_lifetime)
            
        graph_delivery_rate.append((sent_packet_count - package_dropped) / sent_packet_count)
        graph_energy_consumption.append(calculate_energy_consumption())

        # for node in node_to_energy:
        #     if node_to_energy[node] <= 0:
        #         return sent_packet_count
        if sent_packet_count == number_of_episodes:
          return sent_packet_count
            
    return sent_packet_count


if __name__ == '__main__':

    global fuzzy_packets_sent
    global fuzzy_packets_delivered
    global fuzzy_packets_dropped
    global fuzzy_energy_consumption
    global fuzzy_energy_efficiency
    global fuzzy_lifetime

    fuzzy_packets_sent = main()
    fuzzy_packets_delivered = sent_packet_count - package_dropped
    fuzzy_energy_consumption = calculate_energy_consumption()
    fuzzy_energy_efficiency = (sent_packet_count - package_dropped) / calculate_energy_consumption()
    if len(lifetime) == 0:
      lifetime.append(fuzzy_total_network_lifetime)
    
    if len(lifetime) == 0:
      lifetime.append(fuzzy_total_network_lifetime)
    fuzzy_lifetime = lifetime[0]

    print('Fuzzy Training complete!')
    print("Packages sent: ", fuzzy_packets_sent)
    print("Packages delivered: ", fuzzy_packets_delivered)
    print("delivery rate: ", fuzzy_packets_delivered / EPISODES)
    print("Dropped packages: ", package_dropped)
    print("Energy consumption: ", calculate_energy_consumption())
    print("Energy efficiency: ", (sent_packet_count - package_dropped) / calculate_energy_consumption())
    print("Network Lifetime: ", fuzzy_lifetime)
    

    life = []
    for x in range(0, sent_packet_count):
        life.append(x)

    print("NODES")
    for i, node in enumerate(node_to_energy):
        print(node, node_to_energy[node])

    # Uncomment to see plots
    
    # DELIVERY RATE
    plt.plot(life, graph_delivery_rate)
    plt.show()

    # ENERGY CONSUMPTION
    plt.plot(life, graph_energy_consumption)
    plt.show()

# packet_delivery , t_energy, alive_node = Thesis_approach()
# delivery , energy, alive_node3 = R2LTO()
# delivery2 , energy2, alive_node4 = RLBR()