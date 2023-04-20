import random
import matplotlib.pyplot as plt
import math
import heapq

ENERGY = 1
COLUMNS = 25
ROWS = 25
NUMBER_OF_NODES = 10

RADIO_DIST = 7

#-----SIMULATION SET UP-------

nodes = [] # [(x-coordinate, y-coordinate), ...]

edges = [] # [(from_node, to_node, distance), ...]
# node = (x-coordinate, y-coordinate)

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node


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

    node_to_energy[(0, 0)] = sink_node
    nodes.append((0,0))

    
create_network(rows=ROWS, columns=COLUMNS, num_of_nodes=NUMBER_OF_NODES, nodes=nodes, node_energy=node_to_energy)
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

create_edges(edges=edges, nodes=nodes, max_radio_distance=RADIO_DIST)

#-----SIMULATION SET UP END-------

#constants used in energy calculation
A = 1.0e-9
B = 5.0e-11
m = 4

# Equation 3, Energy transmission cost
def transmission_eq3(distance, k):
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
    
    current_energy = residual_energy - transmission_eq3(distance, k)

    if ALPHA * SIGMA < current_energy and current_energy <= SIGMA:
        #lollolo
        return 1 - ((1 - GAMMA) / (1 - ALPHA)) * (1 - current_energy / SIGMA)
        
    elif transmission_eq3(distance, k) < current_energy and current_energy <= ALPHA * SIGMA:
        condition_1 = (GAMMA) / (ALPHA * (SIGMA - transmission_eq3(distance, k))) 
        condition_2 = current_energy - transmission_eq3(distance, k)
        return condition_1 * condition_2

    elif current_energy <= transmission_eq3(distance, k):
        return 0


THETA = [0.2, 0.8]

# Equation 7, fuzzy membership minimun delay
def minimum_delay_eq7(x):
    return x


# Equation 10, mulitobjective membership function
# FIXME DON'T FORGET X FFS
def multi_objective_membership_eq10(umd, ulf):
    return (BETA * min(umd, ulf)) + ((1 - BETA) * ((umd + ulf) / 2)) 

# Equation 11, returns new value of weight of edge
def weight_assign_eq11(edge, package_size):
    residual_energy = node_to_energy[edge[0]]
    #DON'T FORGET X FFS
    return 1 - multi_objective_membership_eq10(lifetime_membership_eq6(residual_energy, edge[2], package_size), minimum_delay_eq7(1000))

# Must be of existing node
# TODO TEST
# routing_request = nodes[0::3]

# FIXME GÖR OM ELLER TA BORT
def create_routes(routes):

    for _ in range(0, 10_000):
        index = random.randint(0, len(nodes) - 1)
        package_size = random.randint(16, 64) # Ask supervisor for correct reasonable size
        routes.append((nodes[index], package_size))
        

def dijsktras(edge_list, start_node, end_node):
    # Step 1
    
    #dictionairy where key = a node and value is the previous node when calc dijkstras
    path_nodes = {}
    distances = {node: float('inf') for node,_,_ in edge_list}
    

    distances[start_node] = 0
    
    # Step 2
    visited = [(0, start_node)]
    heapq.heapify(visited)
    
    while visited: # change name
        # Step 3.1
        (curr_dist, curr_node) = heapq.heappop(visited)
        
        #stop if visiting end_node
        if curr_node == end_node:
            break

        # Step 3.2
        for (from_node, to_node, w) in edge_list:
            if from_node == curr_node:
                new_dist = curr_dist + w
                # print("Distances", distances)
                # print("No node", no_node)
                # print("W", w)
                if new_dist < distances[to_node]:
                    
                    distances[to_node] = new_dist
                    #här lägger vi in föregående nod
                    path_nodes[to_node] = from_node
                    heapq.heappush(visited, (new_dist, to_node))
        
        
    
    # Step 4

    # Creates a list of the nodes between start_node and end_node
    path = []
    node = end_node
    while node != start_node:
        path.append(node)
        #just in case there is no path between nodes the loop stops if the previous value is None
    
        # FIXME if-satsen behövs fixas 
        # if path_nodes[node] != None:
        #     node = path_nodes[node]
        # else:
        #     break
        if path_nodes.get(node) != None:
            node = path_nodes[node]
        else:
            break
    path.append(start_node)
    path.reverse()

    #returnerar bara värdet. Vill returnera vägen också
    return path


def send_data_and_compute_new_energy(path, k):
    
    # tranmission cost on start_node
    
    print(path)
    
    for index, node in enumerate(path):
        if index == 0:
            # Do Only transmission
            continue
        if index == len(path) - 1:
            return
        #sending data
        
        next_node = path[index + 1]
        tmp_distance = None
        current_energy = node_to_energy[node]
        
        for start_node, end_node, distance in edges:
            if start_node == node and end_node == next_node:
                tmp_distance = distance

        # To node
        print("current node, transmission cost and reception cost")
        print(node)
        print(transmission_eq3(tmp_distance, k))
        print(reception_eq4(k))
        print("end")
        node_to_energy[node] = current_energy - transmission_eq3(tmp_distance, k) - reception_eq4(k)


def main():

    #dict with edge - weight in this context
    edge_weight = {}

    # Initialize routing requests
    routing_request = []
    # create_routes(routing_request)
    routing_request.append(nodes[1])

    lifetime_count = 0

    # for all routing requests
    for request in routing_request:
        # for each edge in network
        for i, edge in enumerate(edges):
            #assign weight to edges and add to dict
            edge_weight[edge] = weight_assign_eq11(edge, request[1])

        #find shortest path based on new weights
        #TODO ska request vara indexerat med 0??
        ###BORTA

        print("start node:")
        print(request)
        minimum_weight_path = dijsktras(edge_weight, request, (0, 0))
        

        send_data_and_compute_new_energy(minimum_weight_path, 1000)
        
        #check_energy_levels
            #if any node energy = 0
            #return
        lifetime_count = lifetime_count = 1
    
    return lifetime_count




if __name__ == '__main__':
    main()
    print("NODES")
    for i, node in enumerate(node_to_energy):
        print(node, node_to_energy[node])