import unittest
from parameterized import parameterized
from Scripts.script import *

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


    @unittest.skip
    def test_lall(self):
        expected = 1
        actual = 1
        self.assertEqual(expected, actual)

    @unittest.skip
    def test_inf(self):
        arr = [float('inf'), 0, 0]
        count = 0
        for x in arr:
            if x != 0:
                count = count + 1

        self.assertEqual(1, count)


    @parameterized.expand([
        (1, 1, 2),
        (2, 2, 4),
    ])
    def test_add(self, a, b, res):
        self.assertEqual(res, a+b)

if __name__ == '__main__':
    unittest.main()