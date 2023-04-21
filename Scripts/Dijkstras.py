import heapq

def dijsktras(edge_list, start_node, end_node):
    # Step 1
    
    #dictionairy where key = a node and value is the previous node when calc dijkstras
    path_nodes = {}
    
    
    #new shit:
    distances = {}
    # for (from_node, to_node, distance) in edge_list:
    #     if from_node not in distances:
    #         distances[from_node] = float('inf')
    #     if to_node not in distances:
    #         distances[to_node] = float('inf')
        
    
    distances = {node: float('inf') for node,_,_ in edge_list}
    distances[start_node] = 0
    print(distances)
    
    #print("start node:")
    #print(start_node)
    #print("end node:")
    #print(end_node)
    #print("Distances:")
    #print(distances)
    #print("End of distances")

    # Step 2
    visited = [(0, start_node)]
    heapq.heapify(visited)
    
    while visited: # change name
        # Step 3.1
        (curr_dist, curr_node) = heapq.heappop(visited)

        print("current distance: ")
        print(curr_dist)

        print("current node:")
        print(curr_node)

        
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
    print("distances after")
    print(distances)    
    print("path nodes")
    print(path_nodes)

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



edge_list = [(("A"), ("B"), 7), (("B"), ("A"), 7), (("A"), ("C"), 12), (("C"), ("A"), 12), (("B"), ("C"), 2), (("C"), ("B"), 2), (("B"), ("D"), 9), (("D"), ("B"), 9), (("C"), ("E"), 10), (("E"), ("C"), 10), (("D"), ("E"), 4), (("E"), ("D"), 4), (("D"), ("F"), 1), (("F"), ("D"), 1), (("E"), ("F"), 5), (("F"), ("E"), 5)]


actual = dijsktras(edge_list=edge_list, start_node=("A"), end_node=("D"))

print("OUTPUT LIST")
print(actual)


# arr = [1,2,3]

# print(len(arr))


nodes = [] # [(x-coordinate, y-coordinate), ...]

edges = []  # [(from_node, to_node, distance), ...]


edges.append(((3, 5), (5, 5), 5))
edges.append(((5, 5), (5, 7), 5))
edges.append(((5, 7), (2, 2), 5))
edges.append(((2, 2), (1, 1), 5))
edges.append(((1, 1), (7, 5), 5))
# node = (x-coordinate, y-coordinate)

node_to_energy = {} # key = node (x-coordinate, y-coordinate). Value = residual energy of node

node_to_energy = {}

node_to_energy[(3, 5)] = 1
node_to_energy[(5, 5)] = 1
node_to_energy[(5, 7)] = 1
node_to_energy[(2, 2)] = 1
node_to_energy[(1, 1)] = 1
node_to_energy[(7, 5)] = 1


path = [(3, 5), (5, 5), (5, 7), (2, 2), (1, 1), (7, 5)]

A = 1.0e-9
B = 5.0e-11
m = 4

def transmission_eq3(distance, k):
    return (A + B * distance**m) * k

# Equation 4, Energy reseption cost
def reception_eq4(k):
    return A * k



def send_data_and_compute_new_energy(path, k):
    
    # tranmission cost on start_node

    for index, node in enumerate(path):
        
        if index == len(path) - 1:
            return

        next_node = path[index + 1]
        tmp_distance = None
        current_energy = node_to_energy[node]
        
        for start_node, end_node, distance in edges:
            if start_node == node and end_node == next_node:
                tmp_distance = distance

        # To node
        # print("current node, transmission cost and reception cost")
        # print(node)
        # print(transmission_eq3(tmp_distance, k))
        # print(reception_eq4(k))
        # print("end")

        if index == 0:
            # Do Only transmission on first node
            node_to_energy[node] = current_energy - transmission_eq3(tmp_distance, k)
            continue
    
        
        node_to_energy[node] = current_energy - transmission_eq3(tmp_distance, k) - reception_eq4(k)

for x in node_to_energy:
    print(x, node_to_energy[x])

print("----------------")

for x in range(0, 1000):
    send_data_and_compute_new_energy(path=path, k=100)

for x in node_to_energy:
    print(x, node_to_energy[x])
