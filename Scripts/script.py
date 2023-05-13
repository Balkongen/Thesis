import random
import matplotlib.pyplot as plt
import math
import heapq

ENERGY = 1
COLUMNS = 25
ROWS = 25
NUMBER_OF_NODES = 90

NUMBER_OF_TIMES_ZERO = 0

RADIO_DIST = 7

EPISODES = 200_000
PACKAGE_SIZE = 1000

lifetime_count = 0
shortes_path_ratio = 0

shortest_path_ratio_length = 0

maximum_path_distance = 0

distance_is_zero = 0

#-----SIMULATION SET UP-------

simulation_results_lifetime = []
simulation_results_path_ratio = []

nodes = [] # [(x-coordinate, y-coordinate), ...]

edges = [] # [(from_node, to_node, distance), ...]
# node = (x-coordinate, y-coordinate)

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node

node_to_maximum_path = {} # key = node (x-coordinate, y-coordinate). Value = maximum path to sink node

def setup():
    # Reset all data 
    global edges
    global nodes
    global node_to_energy
    global node_to_maximum_path

    
    global lifetime_count
    global shortes_path_ratio
    global maximum_path_distance 
    # for testing perhaps
    global distance_is_zero
    
    # good_network = True
    while True:
        nodes = []
        edges = []

        # For testing perhaps
        distance_is_zero = 0

        node_to_energy = {}
        node_to_maximum_path = {}

        maximum_path_distance = 0
        lifetime_count = 0
        shortes_path_ratio = 0

        create_network(rows=ROWS, columns=COLUMNS, num_of_nodes=NUMBER_OF_NODES, nodes=nodes, node_energy=node_to_energy)
        create_edges(edges=edges, nodes=nodes, max_radio_distance=RADIO_DIST)

        try:
            maximum_path_distance = driver()
            break

        except KeyError:
            print("retrying network")
    
    # print(edges)



def create_network(rows, columns, num_of_nodes, nodes, node_energy):
    for _ in range(num_of_nodes - 1):
        
        while True:
            x = random.randint(0, rows - 1)
            y = random.randint(0, columns - 1)

            if (x, y) not in nodes:
                nodes.append((x, y))
                node_energy[(x, y)] = ENERGY
                break
        
    sink_node = float('inf')

    node_to_energy[(0, 0)] = sink_node
    nodes.append((0,0))


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


#-----SIMULATION SET UP END-------

#constants used in energy calculation
A = 1.0e-9
B = 5.0e-11
m = 4

# Equation 3, Energy transmission cost
def transmission_eq3(distance, k):
    return (A + B * distance**m) * k
    # return 0

# Equation 4, Energy reseption cost
def reception_eq4(k):
    return A * k
    # return 0

#constants used in fuzzy lifetime membership function
ALPHA = 0.2
GAMMA = 0.9
BETA = 0.2
SIGMA = ENERGY

# Equation 6, Fuzzy lifetime membership function
def lifetime_membership_eq6(residual_energy, distance, k):
    MAXIMUM_LIFETIME = 0
    
    current_energy = residual_energy - transmission_eq3(distance, k)

    if (ALPHA * SIGMA) < current_energy and current_energy <= SIGMA:
        return 1 - ((1 - GAMMA) / (1 - ALPHA)) * (1 - current_energy / SIGMA)
        
    elif transmission_eq3(distance, k) < current_energy and current_energy <= (ALPHA * SIGMA):
        condition_1 = (GAMMA) / (ALPHA * (SIGMA - transmission_eq3(distance, k))) 
        condition_2 = current_energy - transmission_eq3(distance, k)
        return condition_1 * condition_2

    elif current_energy <= transmission_eq3(distance, k):
        return 0
    else:
        return 1 # Sink node
    
    
THETA_RANGE = [0.2, 0.8]
THETA = THETA_RANGE[0]

# Equation 7, fuzzy membership minimun delay
def minimum_delay_eq7(node):
    
    return 1 + (((THETA - 1) * node_to_maximum_path[node]) / maximum_path_distance) # THETA can change based on test runs


# Equation 10, mulitobjective membership function
def multi_objective_membership_eq10(umd, ulf):
    return (BETA * min(umd, ulf)) + ((1 - BETA) * ((umd + ulf) / 2)) 

# Equation 11, returns new value of weight of edge
def weight_assign_eq11(edge, package_size): 
    residual_energy = node_to_energy[edge[1]]
    return 1 - multi_objective_membership_eq10(lifetime_membership_eq6(residual_energy, edge[2], package_size), minimum_delay_eq7(edge[1]))


def create_routes(routes):
    indexes = []
    for _ in range(0, 10):

        while True:
            
            node = random.randint(0, len(nodes) - 1)
            nodexy = nodes[node]
            if node_to_maximum_path[nodexy] != float("inf"): #If source node does not have a path to sink node
                break
            print("recreating routes")
        indexes.append(node)
    
    for i in range(0, EPISODES): # Generate only ten random routes and loop them over and over
        
        # index = random.randint(0, len(nodes) - 1)

        package_size = PACKAGE_SIZE # Ask supervisor for correct reasonable size

        routes.append((nodes[indexes[i % 10]], package_size))
    
        
def dijsktras(edge_list, start_node, end_node):
    
    #dictionairy where key = a node and value is the previous node when calc dijkstras
    path_nodes = {}
    path_nodes[end_node] = None
    #add source node
    
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
              
                if new_dist < distances[to_node]:
                    
                    distances[to_node] = new_dist
                    #här lägger vi in föregående nod
                    path_nodes[to_node] = from_node
                    heapq.heappush(visited, (new_dist, to_node))

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

    #returnerar bara värdet. Vill returnera vägen också
    return path


def send_data_and_compute_new_energy(path, k):

    path_distance = 0

    for index, node in enumerate(path):
        
        if index == len(path) - 1:
            return path_distance

        next_node = path[index + 1]
        tmp_distance = 0
        current_energy = node_to_energy[node]
        
        for start_node, end_node, distance in edges:
            if start_node == node and end_node == next_node:
                tmp_distance = distance
                path_distance = path_distance + distance

        if index == 0:
            # Do Only transmission on first node
            node_to_energy[node] = current_energy - transmission_eq3(tmp_distance, k)
            continue
        
        #sending data
        node_to_energy[node] = current_energy - transmission_eq3(tmp_distance, k) - reception_eq4(k)
    
    return path_distance

        
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
                # print("Distances", distances)
                # print("No node", no_node)
                # print("W", w)
                if new_dist < distances[to_node]:
                    
                    distances[to_node] = new_dist
                    #här lägger vi in föregående nod
                    heapq.heappush(visited, (new_dist, to_node))

    return distances[end_node]


def driver():
    # ratio = Shortest distance from chosen path / shortest possible path
    # print(edges)
    for node in nodes:
        node_to_maximum_path[node] = disco_disk(edge_list=edges, start_node=node, end_node=(0, 0))


    # print(node_to_maximum_path)
    return max(node_to_maximum_path.values())


def z(min_weight_path):
    tmp_dist = 0
    
    for i, node in enumerate(min_weight_path):

        
        if i == len(min_weight_path) - 1:
            break


        for start_node, end_node, distance in edges:
            if (start_node == min_weight_path[i] and end_node == min_weight_path[i + 1]) or (end_node == min_weight_path[i] and start_node == min_weight_path[i + 1]):
                tmp_dist = tmp_dist + distance
                break

    return tmp_dist


def main():
    global lifetime_count
    global shortes_path_ratio
    global maximum_path_distance
    
    # For testing perhaps
    global distance_is_zero

   
    setup()

    #dict with edge - weight in this context
    edge_weight = {}

    # Initialize routing requests
    
    routing_request = []    
    create_routes(routing_request)
    
    
    # for all routing requests
    for request in routing_request:
        lifetime_count = lifetime_count + 1
        if lifetime_count % 1000 == 0:
            print(lifetime_count)
        # for each edge in network
        for i, edge in enumerate(edges):
            
            #assign weight to edges and add to dict
            edge_weight[edge] = weight_assign_eq11(edge, request[1])

        minimum_weight_path = dijsktras(edge_weight, request[0], (0, 0))

        # minimum_weight_path_length = len(minimum_weight_path)
        
        # print("minimum w path")
        # for node in minimum_weight_path:
        #     print(node)

        # temporary_dict_of_edges = {}

        # for nodeA, nodeB, distance in edges:
        #     temporary_dict_of_edges[(nodeA, nodeB, distance)] = distance

        # shortest_path_path = dijsktras(temporary_dict_of_edges, request[0], (0, 0))
        
        # shortest_path_path_length = len(shortest_path_path)
        # print("shortest possible path")
        # for node in shortest_path_path:
        #     print(node)
        
        path_length = z(minimum_weight_path)

        # print(path_distance_ration)
        if node_to_maximum_path[request[0]] == float('inf'):
            shortes_path_from_source = 0
        
        else:
            shortes_path_from_source = node_to_maximum_path[request[0]]
        
        

        
        # path_distance_ration = path_length / shortes_path_from_source

        # print(path_distance_ration)
        # if shortes_path_from_source == 0:
        #     NUMBER_OF_TIMES_ZERO = NUMBER_OF_TIMES_ZERO + 1


        if shortes_path_from_source != 0:
            
            # print("shortest path distances and ratio")
            # print(path_length)
            # print(shortes_path_from_source)

            
            shortes_path_ratio = shortes_path_ratio + (path_length / shortes_path_from_source)
            # shortest_length = minimum_weight_path_length / shortest_path_path_length
            # shortest_path_ratio_length = shortest_path_ratio_length + shortest_length

            # print(path_distance_ration)
            # print("----------------")
        
        else:
            distance_is_zero = distance_is_zero + 1

        # print("start node, end node: ", request)
        # print("MiNI", minimum_weight_path)

        if len(minimum_weight_path) == 1:
            
            continue
        else:
            take = send_data_and_compute_new_energy(minimum_weight_path, PACKAGE_SIZE)
            # print("send data distnace")
            # print(take)

        
        
        for node in node_to_energy:
            if node_to_energy[node] <= 0:
                return lifetime_count
            
    return lifetime_count


if __name__ == '__main__':
    for i in range(0, 50):
        print("currently evaluating number: " , i)
        life = main()
        simulation_results_lifetime.append(life)
        simulation_results_path_ratio.append(shortes_path_ratio / (life - distance_is_zero))
        # print("NODES")
        # for i, node in enumerate(node_to_energy):
        #     print(node, node_to_energy[node])

        # print("lifetime", life)
        # print("RATIO OF SHORTEST PATH distance", shortes_path_ratio / life)
    # print("RATIO OF SHORTEST PATH number of nodes", shortest_path_ratio_length / life)
    print("Number of nodes", NUMBER_OF_NODES)
    # Change the value of theta on tests.
    print("Theta: ", THETA)

    print("Average lifetime: ", sum(simulation_results_lifetime) / len(simulation_results_lifetime))


    for i,sim in enumerate(simulation_results_lifetime):
        print("Lifetime: ", i, sim)

    for i, sim in enumerate(simulation_results_path_ratio):
        print("Ratio: ", sim)

    print("Average ratio of shortest path: ", sum(simulation_results_path_ratio) / len(simulation_results_path_ratio))
    
    print("done")
    
    
    # print("NODES")
    # for i, node in enumerate(node_to_energy):
    #     print(node, node_to_energy[node])

    