import copy
import random
import matplotlib.pyplot as plt

environment_rows = 10
environment_columns = 10

NUMBER_OF_NODES = environment_columns * environment_rows

NUMBER_OF_EPISODES = 1000
transmission_energy_cost = 0.007    # the amount of energy(mJ) consumed by a node to receive and forward a packet to 1 hop distance
active_mode_energy_cost = 0.0005    #the amount of energy(mj) cosumed by a node for being in active mode
initial_node_energy = 0.7
MAX_RADIO_DISTANCE = 1

# lifetime = 0

graph_delivery_rate = []
graph_energy_consumption = []
total_consumption = []

package_dropped = 0
sent_packet_count = 0
lifetime = []
path_lenght = 0


num_malicious_rows = 8
fuzzyMaliciousNodes = {} # comment out nodes for different tests


nodes_dictionairy = {} #Tuple coordinate (x, y) is key, full node is value
node_to_energy = {}


class Node:
    
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.neighbors = []
        self.energy = initial_node_energy
        self.rank = 0

    def set_energy(self, energy):
        self.energy = energy   

    def add_neighbor(self, new_neighbor):
        if new_neighbor not in self.neighbors:
            self.neighbors.append(new_neighbor)
    
    def get_neighbors(self):
        return self.neighbors

    def get_position(self):
        return (self.x, self.y)
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented
        
    def __hash__(self):
        return hash(repr(self))
    
    def __str__(self):
        return "(x, y): {}".format((self.x, self.y))
      
    def __repr__(self):
        return "(x, y): {}".format((self.x, self.y))

    def print_node(self):
        print("(x, y): {} \nenergy: {} \nrank: {}".format((self.x, self.y), self.energy, self.rank))
        neighbor_string = "Neighbors:"
        for neighbor in self.neighbors:
            neighbor_string += (" " + str(neighbor.get_position()))
        print(neighbor_string)
        print()

fuzzyMaliciousNodes[Node(1, 5)] = 0
fuzzyMaliciousNodes[Node(1, 3)] = 0
fuzzyMaliciousNodes[Node(2, 1)] = 0
fuzzyMaliciousNodes[Node(2, 6)] = 0
fuzzyMaliciousNodes[Node(3, 2)] = 0
fuzzyMaliciousNodes[Node(3, 5)] = 0
fuzzyMaliciousNodes[Node(4, 3)] = 0
fuzzyMaliciousNodes[Node(4, 6)] = 0
fuzzyMaliciousNodes[Node(5, 2)] = 0
fuzzyMaliciousNodes[Node(6, 5)] = 0
fuzzyMaliciousNodes[Node(6, 7)] = 0
fuzzyMaliciousNodes[Node(7, 8)] = 0
fuzzyMaliciousNodes[Node(7, 7)] = 0
fuzzyMaliciousNodes[Node(8, 3)] = 0
fuzzyMaliciousNodes[Node(8, 1)] = 0

malicoius_nodes = fuzzyMaliciousNodes.keys()

def create_nodes():
    for x in range(environment_rows):
        for y in range(environment_columns):
            node = Node(x, y)
            # init node energy for all created nodes in node list
            node_to_energy[node] = initial_node_energy  
            nodes_dictionairy[(x, y)] = node


def make_neighbors():
    for x in range(environment_rows):
        for y in range(environment_columns):
            
            if x > 0:
                nodes_dictionairy[(x, y)].add_neighbor(nodes_dictionairy[((x - 1), y)])
            if x < environment_rows - 1:
                nodes_dictionairy[(x, y)].add_neighbor(nodes_dictionairy[((x + 1), y)])
            if y > 0:
                nodes_dictionairy[(x, y)].add_neighbor(nodes_dictionairy[(x, (y - 1))])
            if y < environment_columns - 1:
                nodes_dictionairy[(x, y)].add_neighbor(nodes_dictionairy[(x, (y + 1))])

# STATIC
seq = []

def get_number_of_hops(source_node, hops):
    global c
    global seq
    
    neighbors = source_node.get_neighbors()
    
    for index, node in enumerate(neighbors):
        
        if hops[neighbors[index]] == 0:
            hops[neighbors[index]] = hops[source_node] + 1
        
        elif (hops[neighbors[index]] - hops[source_node]) <= 1:
            continue
        
        elif hops[neighbors[index]] < (hops[source_node] - 1):
            hops[source_node] = hops[neighbors[index]] + 1
        
        else:
            hops[neighbors[index]] = hops[source_node] + 1
            
            if (max_of_hops(neighbors=neighbors, hops=hops)[1] - hops[neighbors[index]]) > 1:
               
                get_number_of_hops(neighbors[index], hops)

    if source_node in seq:
        return
    
    else:
        seq.append(source_node)
    
    for index, node in enumerate(neighbors):
        get_number_of_hops(neighbors[index], hops)
      
    
shortest_path = []


def get_shortest_paths(hops, neighbors, hop_number, paths, sink_node, org_sink):
    global shortest_path
    hop_number -= 1

    for i in range(hop_number + 1): 
        for index, node in enumerate(neighbors):
           
            if hops[neighbors[index]] == (hop_number - i):
                 
                paths[hop_number - i] = neighbors[index]
 
                get_shortest_paths(hops, node.get_neighbors(), hop_number - i, paths, node, org_sink)

            if (hop_number - i) == 1 and i == 0:
                temp_paths = [node for node in paths if node != None]

                # if (temp_paths not in shortest_path) and len(temp_paths) == hops[org_sink]:
                #     shortest_path.append(temp_paths)
                if len(temp_paths) == hops[org_sink]: #TODO changed this. May affect results
                    shortest_path.append(temp_paths)
      

# returns distance of neighbor with max distance from source node
def max_of_hops(neighbors, hops):
    max_distance = 0
    neighbor_list = []
    
    for neighbor in neighbors:
        neighbor_of_neigbhors = neighbor.get_neighbors()
        
        for neighbor_two in neighbor_of_neigbhors:
            
            if neighbor_two not in neighbor_list:
                neighbor_list.append(neighbor_two)
            
            if max_distance < hops[neighbor_two]:
                max_distance = hops[neighbor_two]

    return (neighbor_list, max_distance)
        

def __init__():
    create_nodes()
    make_neighbors()


def find_shortest_path(sink_node, source_node):
    global shortest_path
    global seq

    shortest_path = []
    seq = []
    
    hops = {x: 0 for x in copy.deepcopy(list(nodes_dictionairy.values()))}

    get_number_of_hops(nodes_dictionairy[source_node], hops)
    hops[nodes_dictionairy[source_node]] = 0

    p = [None] * (hops[sink_node])
    get_shortest_paths(hops, sink_node.get_neighbors(), hops[sink_node], p, sink_node, sink_node)
    

def print_shortest_path(shortest_path):
    for x in shortest_path:
        for y in x:
            print(y)
            
        print("--")


def create_grid(rows, columns, nodes, hop):
    grid = [[0]*columns for _ in range(rows)]

    for i in range(rows):
        for j in range(columns):

            if (i, j) in nodes:
                node = nodes_dictionairy[(i, j)]
                grid[i][j] = hop[node]
                
    return(grid)


def send_data_along_path(path, total_lifetime):
    global lifetime
    global package_dropped
    total_lifetime += 1

    for node in node_to_energy:
        if node_to_energy[node] <= 0:
            lifetime.append(total_lifetime)
    
    if len(path) > 1:
        for node in path:
            # lifetime.append(total_lifetime)
            # lifetime += 1
            if node in malicoius_nodes:
                package_dropped += 1
                return total_lifetime
            
            node_to_energy[node] -= transmission_energy_cost
    else:
        
        node_to_energy[path[0]] -= transmission_energy_cost

    for node in node_to_energy:
        node_to_energy[node] -= active_mode_energy_cost
    
    return total_lifetime


def calculate_energy_consumption():
    energy_left = sum(node_to_energy.values())
    return (initial_node_energy * NUMBER_OF_NODES) - energy_left


def main():
    global shortest_path
    global recursive_total_lifetime
    global sent_packet_count

    recursive_total_lifetime = 0
    __init__()
    
    sink_node = nodes_dictionairy[(9, 9)]
    
    print("start energy for nodes: ")
    for node in node_to_energy:
        print(node, " ", node_to_energy[node])

    for x in range(0, NUMBER_OF_EPISODES):

        sent_packet_count += 1

        print(x)
        while(True):
            x = random.randint(0, environment_rows - 1)
            y = random.randint(0, environment_columns - 1)
            source_node = (x, y)

            if not source_node == sink_node:
                break
        
        find_shortest_path(sink_node=sink_node, source_node=source_node)
        # print_shortest_path(shortest_path)
        
        ix = 0
        if len(shortest_path) >= 1:
            ix = random.randint(0, len(shortest_path) - 1)
            recursive_total_lifetime = send_data_along_path(shortest_path[ix], recursive_total_lifetime)
        
        else: # If source node is one hop away from sink          
            recursive_total_lifetime = send_data_along_path([nodes_dictionairy[source_node]], recursive_total_lifetime)

        graph_delivery_rate.append((sent_packet_count - package_dropped) / sent_packet_count)
        graph_energy_consumption.append(calculate_energy_consumption())

        if sent_packet_count == NUMBER_OF_EPISODES:
            return sent_packet_count
        
    return sent_packet_count


if __name__ == '__main__':
    
    recursive_packets_sent = main()
    recursive_delievered = sent_packet_count - package_dropped
    total_energy_consumption = calculate_energy_consumption()
    
    if len(lifetime) == 0:
        lifetime.append(recursive_total_lifetime)

    if len(lifetime) == 0:
        lifetime.append(recursive_total_lifetime)
    
    recursive_lifetime = lifetime[0]

    print("Training complete")
    print("Packages sent: ", recursive_packets_sent)
    print("Packages delivered: ", recursive_delievered)
    print("Delivery rate: ", recursive_delievered / NUMBER_OF_EPISODES)
    print("Dropped packages: ", package_dropped)
    print("Energy consumption: ", total_energy_consumption)
    print("Energy efficiency: ", (sent_packet_count - package_dropped) / total_energy_consumption)
    print("Network Lifetime: ", recursive_lifetime)

    life = []
    for x in range(0, sent_packet_count):
        life.append(x)


    print("end energy for nodes: ")
    for node in node_to_energy:
        print(node, " ", node_to_energy[node])

    # DELIVERY RATE
    plt.plot(life, graph_delivery_rate)
    plt.show()

    # ENERGY CONSUMPTION
    plt.plot(life, graph_energy_consumption)
    plt.show()