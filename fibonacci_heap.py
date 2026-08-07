"""
From-scratch Fibonacci Heap implementation.

A Fibonacci heap is an advanced data structure with O(1) amortized insert,
extract-min, and decrease-key operations, used in Dijkstra's algorithm for
optimal single-source shortest path complexity of O((V + E) log V).

Structure:
- Min-heap property: parent key <= child key
- Forest of min-heap-ordered trees (not necessarily balanced)
- Cascading cuts and lazy merging for efficiency

Operations and amortized complexity:
- insert(key, value): O(1) amortized
- extract_min(): O(log n) amortized
- decrease_key(node, new_key): O(1) amortized
- delete(node): O(log n) amortized (via decrease to -inf then extract-min)
- find_min(): O(1) worst-case
- union(heap1, heap2): O(1) amortized
- size(): O(1) worst-case
"""


class FibonacciNode:
    """Node in a Fibonacci heap."""
    
    def __init__(self, key, value=None):
        self.key = key
        self.value = value if value is not None else key
        self.degree = 0  # number of children
        self.marked = False  # for cascading cuts
        self.parent = None
        self.child = None  # any child (children form circular doubly-linked list)
        self.left = self  # circular doubly-linked list
        self.right = self
    
    def __repr__(self):
        return f"FibonacciNode({self.key})"


class FibonacciHeap:
    """A Fibonacci heap data structure."""
    
    def __init__(self):
        self.min_node = None
        self.size_val = 0
    
    def insert(self, key, value=None):
        """
        Insert a new key-value pair into the heap.
        
        Time: O(1) amortized
        """
        node = FibonacciNode(key, value)
        if self.min_node is None:
            self.min_node = node
        else:
            self._insert_into_root_list(node)
            if key < self.min_node.key:
                self.min_node = node
        self.size_val += 1
        return node
    
    def find_min(self):
        """
        Return the minimum key in the heap.
        
        Time: O(1) worst-case
        """
        if self.min_node is None:
            raise ValueError("Heap is empty")
        return self.min_node.key
    
    def extract_min(self):
        """
        Remove and return the minimum key from the heap.
        
        Time: O(log n) amortized
        """
        if self.min_node is None:
            raise ValueError("Heap is empty")
        
        min_key = self.min_node.key
        old_min = self.min_node
        
        # Promote all children of min node to root list
        if self.min_node.child is not None:
            child = self.min_node.child
            while True:
                next_child = child.right
                child.parent = None
                self._insert_into_root_list(child)
                child = next_child
                if child == self.min_node.child:
                    break
        
        # Remove min node from root list
        if self.min_node.right == self.min_node:
            self.min_node = None
        else:
            self.min_node.left.right = self.min_node.right
            self.min_node.right.left = self.min_node.left
            self.min_node = self.min_node.right
            self._consolidate()
        
        self.size_val -= 1
        return min_key
    
    def decrease_key(self, node, new_key):
        """
        Decrease the key of a node to a new value.
        
        Time: O(1) amortized
        """
        if new_key > node.key:
            raise ValueError("New key is greater than old key")
        
        node.key = new_key
        
        if node.parent is not None and node.key < node.parent.key:
            self._cut(node, node.parent)
            self._cascading_cut(node.parent)
        
        if node.key < self.min_node.key:
            self.min_node = node
    
    def delete(self, node):
        """
        Delete a node from the heap.
        
        Time: O(log n) amortized
        """
        self.decrease_key(node, float('-inf'))
        self.extract_min()
    
    def union(self, other):
        """
        Merge another Fibonacci heap into this one.
        
        Time: O(1) amortized
        """
        if other.min_node is None:
            return
        
        if self.min_node is None:
            self.min_node = other.min_node
        else:
            # Concatenate root lists
            self.min_node.right.left = other.min_node.left
            other.min_node.left.right = self.min_node.right
            self.min_node.right = other.min_node
            other.min_node.left = self.min_node
            
            if other.min_node.key < self.min_node.key:
                self.min_node = other.min_node
        
        self.size_val += other.size_val
    
    def size(self):
        """Return the number of nodes in the heap."""
        return self.size_val
    
    def is_empty(self):
        """Return True if the heap is empty."""
        return self.size_val == 0
    
    # Private helper methods
    
    def _insert_into_root_list(self, node):
        """Insert a node into the root list."""
        if self.min_node.right == self.min_node:
            self.min_node.right = node
            self.min_node.left = node
            node.left = self.min_node
            node.right = self.min_node
        else:
            node.right = self.min_node.right
            node.left = self.min_node
            self.min_node.right.left = node
            self.min_node.right = node
    
    def _consolidate(self):
        """
        Consolidate the root list by merging trees of equal degree.
        This is called after extract_min to restore heap structure.
        """
        if self.min_node is None:
            return
        
        # Max degree is O(log n), so we use a slightly larger array
        max_degree = 64
        degree_table = [None] * max_degree
        
        # Collect all roots
        roots = []
        node = self.min_node
        while True:
            roots.append(node)
            node = node.right
            if node == self.min_node:
                break
        
        # Process each root
        for root in roots:
            degree = root.degree
            current = root
            
            while degree_table[degree] is not None:
                other = degree_table[degree]
                
                # Ensure current has smaller key (becomes parent)
                if current.key > other.key:
                    current, other = other, current
                
                # Link other under current
                self._link(other, current)
                degree_table[degree] = None
                degree += 1
            
            degree_table[degree] = current
        
        # Rebuild root list
        self.min_node = None
        for i in range(max_degree):
            if degree_table[i] is not None:
                if self.min_node is None:
                    self.min_node = degree_table[i]
                    self.min_node.left = self.min_node
                    self.min_node.right = self.min_node
                else:
                    self._insert_into_root_list(degree_table[i])
                    if degree_table[i].key < self.min_node.key:
                        self.min_node = degree_table[i]
    
    def _link(self, child, parent):
        """Link child under parent (child becomes child of parent)."""
        # Remove child from root list
        child.left.right = child.right
        child.right.left = child.left
        
        # Make child a child of parent
        child.parent = parent
        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.right = parent.child.right
            child.left = parent.child
            parent.child.right.left = child
            parent.child.right = child
        
        parent.degree += 1
        child.marked = False
    
    def _cut(self, child, parent):
        """Remove child from parent's child list and add to root list."""
        # Remove from parent's children
        if child.right == child:
            parent.child = None
        else:
            child.left.right = child.right
            child.right.left = child.left
            if parent.child == child:
                parent.child = child.right
        
        parent.degree -= 1
        child.parent = None
        child.marked = False
        self._insert_into_root_list(child)
    
    def _cascading_cut(self, node):
        """Perform cascading cuts up the tree."""
        parent = node.parent
        if parent is not None:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)
