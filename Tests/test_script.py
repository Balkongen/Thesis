import unittest
from parameterized import parameterized
from Scripts.script import *
import math

class Test_reserv(unittest.TestCase):

    ROWS = 25
    COLUMNS = 25

    def test_number_of_nodes(self):
        
        coordniates = []
        expected = 30
        create_network(rows=ROWS, columns=COLUMNS, num_of_nodes=expected, random_list=coordniates, node_energy={})
        actual = len(coordniates)

        self.assertEqual(expected, actual)


    @parameterized.expand([
        (30, 30),
        (40, 40),
        (80, 80),
        (100, 100),
        ])
    def test_number_of_nodes_in_network_parameterized(self, input, expected):
        
        coordinates = []
        create_network(rows=ROWS, columns=COLUMNS, num_of_nodes=input, random_list=coordinates, node_energy={})
        actual = len(coordinates)

        self.assertEqual(expected, actual)

    
    def test_number_of_nodes_in_small_network(self):
        coordinates = []
        create_network(rows=2, columns=2, num_of_nodes=4, random_list=coordinates, node_energy={})
        expected = 4
        actual = len(coordinates)
        
        self.assertEqual(expected, actual)

    
    def test_number_of_nodes_zero_added(self):
        coordniates = []
        expected = 1
        create_network(rows=ROWS, columns=COLUMNS, num_of_nodes=0, random_list=coordniates, node_energy={})
        actual = len(coordniates)

        self.assertEqual(expected, actual)


    def __create_edges(self, nodes, edges, distance):
        for node_one in nodes:
            for node_two in nodes:
                
                if node_one != node_two:
                    x_dist = (node_two[0] - node_one[0])**2
                    y_dist = (node_two[1] - node_one[1])**2
                    c_sum = x_dist + y_dist
                    dist = math.sqrt(c_sum)

                    if dist <= distance:
                        edges.append((node_one, node_two, dist))



    def test_create_edges(self):
        coordinates = [(0,0), (1,1), (2,2), (0,1), (0,3), (0,4), (10,10)]
        actual = []
        expected = []
        create_edges(edges=actual, nodes=coordinates, max_radio_distance=2)
        self.__create_edges(nodes=coordinates, edges=expected, distance=2)

        list.sort(expected)
        list.sort(actual)

        print("--------")
        for x in expected:
            print(x)
        print("--------")
        for x in actual:
            print(x)

        self.assertEqual(expected, actual)
    
    def test_arr(self):
        x = [(1),(2)]
        y = [(2),(1)]
        list.sort(y)

        self.assertTrue(x == y)

if __name__ == '__main__':
    unittest.main()