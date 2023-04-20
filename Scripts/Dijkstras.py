# import heapq

# def dijsktras(edge_list, start_node, end_node):
#     # Step 1
    
#     #dictionairy where key = a node and value is the previous node when calc dijkstras
#     path_nodes = {}
    
    
#     #new shit:
#     distances = {}
#     # for (from_node, to_node, distance) in edge_list:
#     #     if from_node not in distances:
#     #         distances[from_node] = float('inf')
#     #     if to_node not in distances:
#     #         distances[to_node] = float('inf')
        
    
#     distances = {node: float('inf') for node,_,_ in edge_list}
#     distances[start_node] = 0
#     print(distances)
    
#     #print("start node:")
#     #print(start_node)
#     #print("end node:")
#     #print(end_node)
#     #print("Distances:")
#     #print(distances)
#     #print("End of distances")

#     # Step 2
#     visited = [(0, start_node)]
#     heapq.heapify(visited)
    
#     while visited: # change name
#         # Step 3.1
#         (curr_dist, curr_node) = heapq.heappop(visited)

#         print("current distance: ")
#         print(curr_dist)

#         print("current node:")
#         print(curr_node)

        
#         #stop if visiting end_node
#         if curr_node == end_node:
#             break

#         # Step 3.2
#         for (from_node, to_node, w) in edge_list:
#             if from_node == curr_node:
#                 new_dist = curr_dist + w
#                 # print("Distances", distances)
#                 # print("No node", no_node)
#                 # print("W", w)
#                 if new_dist < distances[to_node]:
                    
#                     distances[to_node] = new_dist
#                     #här lägger vi in föregående nod
#                     path_nodes[to_node] = from_node
#                     heapq.heappush(visited, (new_dist, to_node))
        
        
    
#     # Step 4

#     # Creates a list of the nodes between start_node and end_node
#     path = []
#     node = end_node
#     while node != start_node:
#         path.append(node)
#         #just in case there is no path between nodes the loop stops if the previous value is None
    
#         # FIXME if-satsen behövs fixas 
#         # if path_nodes[node] != None:
#         #     node = path_nodes[node]
#         # else:
#         #     break
#         if path_nodes.get(node) != None:
#             node = path_nodes[node]
#         else:
#             break
#     path.append(start_node)
#     path.reverse()

#     #returnerar bara värdet. Vill returnera vägen också
#     return path



# edge_list = [(("A"), ("B"), 7), (("B"), ("A"), 7), (("A"), ("C"), 12), (("C"), ("A"), 12), (("B"), ("C"), 2), (("C"), ("B"), 2), (("B"), ("D"), 9), (("D"), ("B"), 9), (("C"), ("E"), 10), (("E"), ("C"), 10), (("D"), ("E"), 4), (("E"), ("D"), 4), (("D"), ("F"), 1), (("F"), ("D"), 1), (("E"), ("F"), 5), (("F"), ("E"), 5)]


# actual = dijsktras(edge_list=edge_list, start_node=("A"), end_node=("F"))

# print("OUTPUT LIST")
# print(actual)


arr = [1,2,3]

print(len(arr))