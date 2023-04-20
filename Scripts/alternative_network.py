import random

def print_network(network):
    for x, node in enumerate(network):
        print(x, node)


nodes = []
NUMBER_OF_NODES = 25
PACKET = 1000
# ENERGY_COST = 5.0e-11 # Real cost value
ENERGY_COST = 0.00001


for _ in range(0, NUMBER_OF_NODES):
    nodes.append(1)

sink_pos = int(len(nodes) / 2)
nodes[sink_pos] = float('inf')

def iterate():
    lifetime = 0

    while True:
        start_node = random.randint(0, len(nodes))
        
        if start_node <= sink_pos:
            for x in range(start_node, len(nodes)):
                
                lifetime = lifetime + 1
                if nodes[x] == float('inf'):
                    
                    break
                else:
                    if nodes[x] <= 0:
                        
                        return lifetime
                    else:
                        nodes[x] = nodes[x] - (ENERGY_COST * PACKET)
                
        else:
            for x in reversed(range(sink_pos, start_node)):
    
                lifetime = lifetime + 1
                if nodes[x] == float('inf'):
        
                    break
                else:
                    if nodes[x] <= 0:
                        return lifetime
                    else:
                        
                        nodes[x] = nodes[x] - (ENERGY_COST * PACKET)

# TODO Can add malicious nodes simulation.
          
print(iterate())

print_network(nodes)