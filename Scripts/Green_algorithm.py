import math


environment_rows = 10
environment_columns = 10

number_of_episodes = 1000
transmission_energy_cost = 0.007    # the amount of energy(mJ) consumed by a node to receive and forward a packet to 1 hop distance
active_mode_energy_cost = 0.0005    #the amount of energy(mj) cosumed by a node for being in active mode
initial_node_energy = 0.7
MAX_RADIO_DISTANCE = 1


num_malicious_rows = 8
fuzzyMaliciousNodes = {} # comment out nodes for different tests

fuzzyMaliciousNodes[(3, 5)] = 0
fuzzyMaliciousNodes[(1, 6)] = 0
fuzzyMaliciousNodes[(2, 5)] = 0
fuzzyMaliciousNodes[(3, 6)] = 0
fuzzyMaliciousNodes[(2, 0)] = 0
fuzzyMaliciousNodes[(5, 7)] = 0
fuzzyMaliciousNodes[(7, 8)] = 0
fuzzyMaliciousNodes[(1, 3)] = 0


maliciousNodesKeys = fuzzyMaliciousNodes.keys()



maxRank = 18 # TODO will be set appropriatly later

link_table = []
sensor_node_table = []

nodes_dictionairy = {} #Tuple coordinate (x, y) is key, full node is value

nodes = []
edges = []
node_to_energy = {}

# def create_graph():
#     for y in range(0, environment_rows):
#         for x in range(0, environment_columns):
#             nodes.append((x, y))
            
#             node_to_energy[(x, y)] = initial_node_energy

#     for node_one in nodes:
#         for node_two in nodes:
            
#             if node_one != node_two:
#                 x_dist = (node_two[0] - node_one[0])**2
#                 y_dist = (node_two[1] - node_one[1])**2
#                 x_y_diff = x_dist + y_dist
#                 distance = math.sqrt(x_y_diff)
    
#                 if distance <= MAX_RADIO_DISTANCE:
#                     edges.append((node_one, node_two, distance))

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
        return "(x, y): {} \nenergy: {} \nrank: {}".format((self.x, self.y), self.energy, self.rank)
      

    def print_node(self):
        print("(x, y): {} \nenergy: {} \nrank: {}".format((self.x, self.y), self.energy, self.rank))
        neighbor_string = "Neighbors:"
        for neighbor in self.neighbors:
            neighbor_string += (" " + str(neighbor.get_position()))
        print(neighbor_string)
        print()
            




# def energy_aware_routing_algorithm(energy_cost, source, vertices):
#     sptSet = {}
#     pred = {}
#     energy = {}

#     for index, node in enumerate(vertices, start=1):
       

#         sptSet[node] = False
#         pred[node] = float('inf')
#         energy[node] = 0

    
#     sptSet[source] = True
#     energy[source] = float('inf')
#     pred[vertices[0]] = -1

#     # for x in vertices:
#     #     print(x.rank)

#     for rank in range(maxRank + 1):
#         for node in vertices:
#             if node.rank == rank and node.energy > 0:
#                 # print("ada", pred[node])
#                 while pred[node] == -1:
#                     # print("asd")
#                     u_index, u = max_energy(vertices)
                    
#                     sptSet[u] = True
#                     for index, v in enumerate(vertices):
                        
#                         if index == 0:
#                             continue
#                         v_index = index % 10
#                         if sptSet[v] == False and energy[u] + energy_cost[u_index][v_index] >= energy[v]:
#                             energy[v] = energy[u] + energy_cost[u_index][v_index]
#                             pred[v] = u
#                             print(pred[v])

# def energy_aware_routing_algorithm(energy_cost, source, vertices):
#     sptSet = []
#     pred = []
#     energy = []



#     for index, node in enumerate(vertices):
#         sptSet.append(False)
#         pred.append(float('inf'))
#         energy.append(0)
        

    
#     pred[0] = -1
    
#     sptSet[source] = True
#     energy[source] = float('inf')

#     for rank in range(maxRank + 1):
#         for i,node in enumerate(vertices):
#             # print(i)
#             # if i == 0:
#             #     return
#             if node.rank == rank and node.energy > 0:
#                 while pred[i] == -1:
#                     u_index, max_node = max_energy(vertices)
#                     sptSet[u_index] = True
#                     for v_index, v_node in enumerate(vertices):
#                         if v_index == 0:
#                             continue
#                         u = u_index % 10
#                         v = v_index % 10

#                         if sptSet[v_index] == False and energy[u_index] + energy_cost[u][v] >= energy[v_index]:
#                             energy[v_index] = energy[u_index] + energy_cost[u][v]
#                             pred[v_index] = max_node.energy
                            



def energy_aware_routing_algorithm(energy_cost, source, vertices):
    sptSet = []
    pred = []
    energy = []

    for index, node in enumerate(vertices):
        sptSet[index] = False
        pred[index] = float('inf')
        energy[index] = 0
    
    sptSet[source] = True
    energy[source] = float('inf')

    for rank in enumerate(maxRank + 1):
        for node in vertices:
            if node.rank == rank and node.energy > 0:
                while pred[node] == -1:
                    u =  max_energy(vertices)
                    sptSet[u] = True
                    for v in enumerate(vertices):
                        if v == 0:
                            continue
                        
                        if sptSet[v] == False and energy[u] + energy_cost[u][v] >= energy[v]:
                            energy[v] = energy[u] + energy_cost[u][v] #Replace with transmission cost
                            pred[v] = u




# returns the vertice with the highest residual energy???
def max_energy(vertices):
    max_energy_node = vertices[0]
    index = 0
    for ix, node in enumerate(vertices):
        if node.energy > max_energy_node.energy:
            index = ix
            max_energy_node = node
    
    return index, max_energy_node
  

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


def create_ranks_new(nodes_input, sink_node):
    for node in nodes_input:
        if node == sink_node:
            node.set_rank(0.0)
            continue
        node.set_rank(float('inf'))
    
    while(sum(node.rank for node in nodes if isinstance(node.rank, float)) == float('inf')):
        for node in nodes_input:
            neighbors = node.get_neighbors()

            for neighbor in neighbors:
                if node.rank > (neighbor.rank + 1):
                    node.rank = neighbor.rank + 1
    

def main():
    cost = [[0.001 for _ in range(environment_rows)] for _ in range(environment_columns)]
   
    # print(cost)
    for x in range(environment_rows):
        for y in range(environment_columns):
            node = Node(x, y)
            nodes.append(node) 
            
            # testing
            nodes_dictionairy[(x, y)] = node

    # for x in nodes_dictionairy:
    #     nodes_dictionairy[x].print_node()
    make_neighbors()

    # create_ranks_new(nodes_dictionairy)
    #     print()
    create_ranks_new(nodes, nodes[len(nodes) - 1])

    # for x in range(10):
    # energy_aware_routing_algorithm(cost, nodes[20], nodes)
    
    energy_aware_routing_algorithm(cost, 20, nodes)

    # for x in nodes:
    #     print(x.rank)


if __name__ == '__main__':
    main()