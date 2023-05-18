import math


environment_rows = 3
environment_columns = 3

NUMBER_OF_NODES = environment_columns * environment_rows

number_of_episodes = 1000
transmission_energy_cost = 0.007    # the amount of energy(mJ) consumed by a node to receive and forward a packet to 1 hop distance
active_mode_energy_cost = 0.0005    #the amount of energy(mj) cosumed by a node for being in active mode
initial_node_energy = 0.7
MAX_RADIO_DISTANCE = 1


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


link_table = []
sensor_node_table = []

nodes_dictionairy = {} #Tuple coordinate (x, y) is key, full node is value

nodes = []
edges = []
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
    
    def set_rank(self, rank):
        self.rank = rank

    def add_neighbor(self, new_neighbor):
        if new_neighbor not in self.neighbors:
            self.neighbors.append(new_neighbor)
    
    def get_neighbors(self):
        return self.neighbors

    def get_position(self):
        return (self.x, self.y)
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __str__(self):
        return "(x, y): {} \nenergy: {}".format((self.x, self.y), self.energy)
      
    def __repr__(self):
        return "(x, y): {} \nenergy: {}".format((self.x, self.y), self.energy)

    def print_node(self):
        print("(x, y): {} \nenergy: {} \nrank: {}".format((self.x, self.y), self.energy, self.rank))
        neighbor_string = "Neighbors:"
        for neighbor in self.neighbors:
            neighbor_string += (" " + str(neighbor.get_position()))
        print(neighbor_string)
        print()

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
     
                
def create_graph():
    for y in range(0, environment_rows):
        for x in range(0, environment_columns):
            nodes.append((x, y))
            
            node_to_energy[(x, y)] = initial_node_energy

    for node_one in nodes:
        for node_two in nodes:
            
            if node_one != node_two:
                x_dist = (node_two[0] - node_one[0])**2
                y_dist = (node_two[1] - node_one[1])**2
                x_y_diff = x_dist + y_dist
                distance = math.sqrt(x_y_diff)
    
                if distance <= MAX_RADIO_DISTANCE:
                    edges.append((node_one, node_two, distance))






# STATIC
c = 0

seq = []


def algorithm_1(source_node, hops):
    
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
                print("recursion")
                algorithm_1(neighbors[index], hops)
                # print(hops)
    
    
    if source_node in seq:
        return
    
    else:
        seq.append(source_node)
    
    for index, node in enumerate(neighbors):
        algorithm_1(neighbors[index], hops)
        # print(hops)


            
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
        


        
k = 0
shortest_path = []

def algorithm_2(hops, neighbors, hop_number, paths, sink_node):
    global k
    global shortest_path

    # init k maybe
    for i in range(hop_number): # FIck resultat vi hop_number - 1
        for index, node in enumerate(neighbors):
            
            if hops[neighbors[index]] == hop_number - i:
                paths[hop_number - i] = neighbors[index]
                algorithm_2(hops, max_of_hops(neighbors, hops)[0], hop_number - i, paths, node)
                # print(paths)
            # print("HOp ", hop_number)
            # print("I ", i)

            if (hop_number - i) == 1:
                # print(k)
                shortest_path.append(paths)
                # k = k + 1
    

def create_nodes():
    for x in range(environment_rows):
        for y in range(environment_columns):
            node = Node(x, y)
            nodes.append(node) 
            
            # testing
            nodes_dictionairy[(x, y)] = node



def main():
    create_nodes()
    make_neighbors()
    
    sink_node = nodes_dictionairy[(2, 2)]

    hops = nodes_dictionairy.values()
    hops = {x: 0 for x in hops}

    # TODO generate source node
    
    start_coordinate = (0, 0)
    
    algorithm_1(nodes_dictionairy[start_coordinate], hops)
    hops[nodes_dictionairy[start_coordinate]] = 0
    print("---------------")
    # for index, node in enumerate(hops):
    #     print(node.get_position(), hops[node])

    grid = create_grid(environment_rows, environment_columns, nodes_dictionairy, hops)

    # for row in grid:
    #     print(row)
    
    
    p = [0] * hops[sink_node] # TODO FIxa den här
    print(p)
    algorithm_2(hops, sink_node.get_neighbors(), hops[sink_node], p, sink_node)

    global shortest_path
    for x in shortest_path:
        for y in x:
            print(type(y))
            
        print("--")
    # print(shortest_path)
    global seq
    # print(seq)
    # hops[(0, 0)] = 0

def create_grid(rows, columns, nodes, hop):
    grid = [[0]*columns for _ in range(rows)]

    for i in range(rows):
        
        for j in range(columns):
            if (i, j) in nodes:
                node = nodes_dictionairy[(i, j)]
                grid[i][j] = hop[node]
                

    return(grid)

if __name__ == '__main__':
    main()