"""Tester file for the inventory allocator.

Tester and allocator code written with Python 3.6

To run, `python test_allocator.py`
"""

from inventory_allocator import allocate
import unittest

class TestAllocator(unittest.TestCase):
    """Unit testing class for the inventory allocator."""

    def setUp(self):
        """Setup function to initialize various orders and warehouses."""

        self.mult_orders = { 'apple': 5, 'banana': 5, 'orange': 5 }
        self.mult_warehouses = [ 
            { 
                'name': 'owd', 
                'inventory': { 
                    'apple': 5, 
                    'orange': 10 
                } 
            }, 
            { 
                'name': 'dm', 
                'inventory': { 
                    'banana': 5, 
                    'orange': 10 
                } 
            } 
        ]
        self.one_order = { 'apple': 1 }
        self.one_warehouse = [{ 'name': 'owd', 'inventory': { 'apple': 1 }}]

        self.one_order_many_of_one = { 'apple': 10 }
        self.mult_warehouses_split_items = [
            { 
                'name': 'owd', 
                'inventory': { 
                    'apple': 5 
                } 
            }, 
            { 
                'name': 'dm', 
                'inventory': { 
                    'apple': 5 
                }
            }
        ]

        self.most_stock_at_end = [
            { 
                'name': 'owd', 
                'inventory': { 
                    'apple': 5 
                } 
            }, 
            { 
                'name': 'owd2', 
                'inventory': { 
                    'apple': 5 
                } 
            }, 
            { 
                'name': 'owd3', 
                'inventory': { 
                    'apple': 10 
                } 
            }, 
            
        ]

        self.several_orders_mult_sol = {
            'apple': 7,
            'orange': 1,
            'banana': 4
        }

        self.entire_stock = {
            'apple': 22,
            'orange': 6,
            'banana': 6
        }
        
        self.nonexisting_item = {
            'pear': 2
        }

        self.many_warehouses = [
            {
                'name': 'owd',
                'inventory': {
                    'apple': 1,
                    'orange': 1,
                }
            },
            {
                'name': 'dm',
                'inventory': {
                    'banana': 2,
                    'orange': 2,
                }
            },
            {
                'name': 'wh',
                'inventory':{
                    'apple':4,
                    'orange': 3
                }
            },
            {
                'name': 'wh1',
                'inventory':{
                    'apple':2
                }
            },
            {
                'name': 'wh2',
                'inventory':{
                    'apple': 6,
                    'banana': 4
                }
            },
            {
                'name': 'wh3',
                'inventory':{
                    'apple': 5
                }
            },
            {
                'name': 'wh4',
                'inventory':{
                    'apple': 1
                }
            },
            {
                'name': 'wh5',
                'inventory':{
                    'apple': 3
                }
            },
        ]

        self.no_order = {}
        self.no_warehouses = []
        self.empty_warehouse = [{ 'name': 'owd', 'inventory': { 'apple': 0 }}]


    def test_mult_orders_mult_warehouses(self):
        """Order multiple items contained in multiple warehouses"""
        res = allocate(self.mult_orders, self.mult_warehouses)
        sol = [
            {
                'name': 'owd', 
                'inventory': {
                    'apple': 5, 
                    'orange': 5
                }
            }, 
            {
                'name': 'dm', 
                'inventory': {
                    'banana': 5
                }
            }
        ]
        self.assertEqual(res, sol)

    def test_one_order_one_warehouse(self):
        """Order one item from one warehouse"""
        res = allocate(self.one_order, self.one_warehouse)
        sol = [{ 'name': 'owd', 'inventory': { 'apple': 1 }}]
        self.assertEqual(res, sol)

    def test_many_of_one_split_warehouses(self):
        """Order many of one item to be fulfilled by multiple warehouses"""
        res = allocate(self.one_order_many_of_one,
                self.mult_warehouses_split_items)
        sol = [
            {
                'name': 'owd', 
                'inventory': {
                    'apple': 5
                }
            }, 
            {
                'name': 'dm', 
                'inventory': {
                    'apple': 5
                }
            }
        ]
        self.assertEqual(res, sol)

    def test_one_order_empty_warehouse(self):
        """Order a single item with no warehouses"""
        res = allocate(self.one_order, self.no_warehouses)
        sol = []
        self.assertEqual(res, sol)

    def test_many_of_one_sparse_warehouse(self):
        """Order many of one item from warehouse that doesn't have enough"""
        res = allocate(self.one_order_many_of_one, self.one_warehouse)
        sol = []
        self.assertEqual(res, sol)

    def test_several_orders_many_warehouses(self):
        """Order multiple items from multiple warehouses.
        
        There are several combinations of warehouses that can fulfill this
        order. 
        """
        res = allocate(self.several_orders_mult_sol, self.many_warehouses)
        sol = [
            {
                'name': 'owd', 
                'inventory': {
                    'apple': 1, 
                    'orange': 1
                }
            }, 
            {
                'name': 'wh2', 
                'inventory': {
                    'apple': 6, 
                    'banana': 4
                }
            }
        ]
        self.assertEqual(res, sol)
    
    def test_entire_stock_many_warehouses(self):
        """Order the enitre stock of multiple warehouses"""
        res = allocate(self.entire_stock, self.many_warehouses)
        sol = self.many_warehouses
        self.assertEqual(res, sol)

    def test_one_order_split_warehouses(self):
        """Order one item that can be fulfilled by just the first warehouse"""
        res = allocate(self.one_order, self.mult_warehouses_split_items)
        sol = [{'name': 'owd', 'inventory': {'apple': 1}}]
        self.assertEqual(res, sol)
    
    def test_no_order_one_warehouse(self):
        """Order no items but have a warehouse"""
        res = allocate(self.no_order, self.one_warehouse)
        sol = []
        self.assertEqual(res, sol)

    def test_no_order_no_warehouses(self):
        """Order no items and have no warehouses"""
        res = allocate(self.no_order, self.no_warehouses)
        sol = []
        self.assertEqual(res, sol)

    def test_nonexisting_item_many_warehouses(self):
        """Order an item that no warehouse contains"""
        res = allocate(self.nonexisting_item, self.many_warehouses)
        sol = []
        self.assertEqual(res, sol)

    def test_mult_orders_insufficient_warehouses(self):
        """Order multiple items that no combination of warehouses can fulfill"""
        res = allocate(self.several_orders_mult_sol, self.mult_warehouses)
        sol = []
        self.assertEqual(res, sol)
        
    def test_optimal_answer_at_end(self):
        """Order an item whose optimal shipment is the final warehouse
        
        A combination of warehouses prior to the final warehouse can fulfill
        this shipment, but the final warehouse is optimal.
        """
        res = allocate(self.one_order_many_of_one, self.most_stock_at_end)
        sol = [{'name': 'owd3', 'inventory': {'apple': 10}}]
        self.assertEqual(res, sol)

if __name__ == '__main__':
    unittest.main()
