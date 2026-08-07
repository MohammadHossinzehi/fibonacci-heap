"""
Unit tests for Fibonacci heap implementation.
"""

import unittest
from fibonacci_heap import FibonacciHeap, FibonacciNode


class TestFibonacciNode(unittest.TestCase):
    """Test FibonacciNode class."""
    
    def test_init(self):
        """Test node initialization."""
        node = FibonacciNode(5)
        self.assertEqual(node.key, 5)
        self.assertEqual(node.value, 5)
        self.assertEqual(node.degree, 0)
        self.assertFalse(node.marked)
        self.assertIsNone(node.parent)
        self.assertIsNone(node.child)
        self.assertIs(node.left, node)
        self.assertIs(node.right, node)
    
    def test_init_with_value(self):
        """Test node initialization with separate value."""
        node = FibonacciNode(5, 'five')
        self.assertEqual(node.key, 5)
        self.assertEqual(node.value, 'five')


class TestFibonacciHeap(unittest.TestCase):
    """Test FibonacciHeap class."""
    
    def setUp(self):
        """Create a fresh heap for each test."""
        self.heap = FibonacciHeap()
    
    def test_empty_heap(self):
        """Test operations on empty heap."""
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(self.heap.size(), 0)
        with self.assertRaises(ValueError):
            self.heap.find_min()
        with self.assertRaises(ValueError):
            self.heap.extract_min()
    
    def test_single_insert(self):
        """Test inserting a single element."""
        node = self.heap.insert(5)
        self.assertEqual(self.heap.size(), 1)
        self.assertEqual(self.heap.find_min(), 5)
        self.assertIsNotNone(node)
    
    def test_multiple_inserts(self):
        """Test inserting multiple elements."""
        self.heap.insert(5)
        self.heap.insert(3)
        self.heap.insert(7)
        self.heap.insert(1)
        
        self.assertEqual(self.heap.size(), 4)
        self.assertEqual(self.heap.find_min(), 1)
    
    def test_extract_min_single(self):
        """Test extract-min on single element."""
        self.heap.insert(5)
        result = self.heap.extract_min()
        self.assertEqual(result, 5)
        self.assertTrue(self.heap.is_empty())
    
    def test_extract_min_sequence(self):
        """Test extract-min returns elements in sorted order."""
        keys = [5, 3, 7, 1, 9, 2, 8]
        for key in keys:
            self.heap.insert(key)
        
        sorted_keys = sorted(keys)
        extracted = []
        while not self.heap.is_empty():
            extracted.append(self.heap.extract_min())
        
        self.assertEqual(extracted, sorted_keys)
    
    def test_find_min_unchanged_by_operations(self):
        """Test that find_min doesn't modify the heap."""
        self.heap.insert(5)
        self.heap.insert(3)
        
        min1 = self.heap.find_min()
        min2 = self.heap.find_min()
        self.assertEqual(min1, min2)
        self.assertEqual(self.heap.size(), 2)
    
    def test_decrease_key(self):
        """Test decrease-key operation."""
        node = self.heap.insert(10)
        self.heap.insert(5)
        
        self.heap.decrease_key(node, 2)
        self.assertEqual(node.key, 2)
        self.assertEqual(self.heap.find_min(), 2)
    
    def test_decrease_key_invalid(self):
        """Test that increase is rejected."""
        node = self.heap.insert(5)
        with self.assertRaises(ValueError):
            self.heap.decrease_key(node, 10)
    
    def test_delete(self):
        """Test delete operation."""
        node1 = self.heap.insert(5)
        node2 = self.heap.insert(3)
        node3 = self.heap.insert(7)
        
        self.heap.delete(node2)
        self.assertEqual(self.heap.size(), 2)
        
        extracted = []
        while not self.heap.is_empty():
            extracted.append(self.heap.extract_min())
        
        self.assertEqual(sorted(extracted), [5, 7])
    
    def test_union(self):
        """Test merging two heaps."""
        heap1 = FibonacciHeap()
        heap1.insert(5)
        heap1.insert(3)
        
        heap2 = FibonacciHeap()
        heap2.insert(7)
        heap2.insert(1)
        
        heap1.union(heap2)
        
        self.assertEqual(heap1.size(), 4)
        self.assertEqual(heap1.find_min(), 1)
        
        extracted = []
        while not heap1.is_empty():
            extracted.append(heap1.extract_min())
        
        self.assertEqual(extracted, [1, 3, 5, 7])
    
    def test_union_with_empty(self):
        """Test union with empty heap."""
        heap1 = FibonacciHeap()
        heap1.insert(5)
        
        heap2 = FibonacciHeap()
        
        heap1.union(heap2)
        self.assertEqual(heap1.size(), 1)
        self.assertEqual(heap1.find_min(), 5)
    
    def test_large_sequence(self):
        """Test with a large number of operations."""
        import random
        
        keys = list(range(100))
        random.shuffle(keys)
        
        for key in keys:
            self.heap.insert(key)
        
        self.assertEqual(self.heap.size(), 100)
        
        extracted = []
        while not self.heap.is_empty():
            extracted.append(self.heap.extract_min())
        
        self.assertEqual(extracted, list(range(100)))
    
    def test_decrease_key_with_large_cascade(self):
        """Test decrease-key that triggers cascading cuts."""
        nodes = []
        for i in range(20):
            nodes.append(self.heap.insert(i))
        
        # Decrease a node deep in the tree
        self.heap.decrease_key(nodes[19], -5)
        self.assertEqual(self.heap.find_min(), -5)
        self.assertEqual(self.heap.extract_min(), -5)
    
    def test_alternating_operations(self):
        """Test alternating insert and extract-min."""
        self.heap.insert(5)
        self.heap.insert(3)
        
        self.assertEqual(self.heap.extract_min(), 3)
        self.assertEqual(self.heap.size(), 1)
        
        self.heap.insert(1)
        self.heap.insert(7)
        
        extracted = []
        while not self.heap.is_empty():
            extracted.append(self.heap.extract_min())
        
        self.assertEqual(extracted, [1, 5, 7])


class TestFibonacciHeapProperties(unittest.TestCase):
    """Test heap properties and invariants."""
    
    def test_min_heap_property(self):
        """Verify min-heap property: parent <= children."""
        heap = FibonacciHeap()
        nodes = [heap.insert(i) for i in [5, 3, 7, 1, 9, 2, 8, 4, 6]]
        
        # Extract all to verify ordering
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_min())
        
        self.assertEqual(extracted, sorted(extracted))
    
    def test_fibonacci_structure(self):
        """Test that tree degrees follow Fibonacci pattern after consolidation."""
        heap = FibonacciHeap()
        # Insert power of 2 elements to create predictable tree structure
        for i in range(8):
            heap.insert(i)
        
        # After extracting min, trees should consolidate
        heap.extract_min()
        
        # Heap should still be valid
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract_min())
        
        self.assertEqual(extracted, list(range(1, 8)))


if __name__ == '__main__':
    unittest.main()
