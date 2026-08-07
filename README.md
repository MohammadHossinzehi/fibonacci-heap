# Fibonacci Heap

A from-scratch implementation of a Fibonacci heap data structure in Python, with O(1) amortized insert, extract-min, and decrease-key operations. This is an advanced data structure commonly used in Dijkstra's algorithm for optimal single-source shortest path performance.

## Why Fibonacci Heaps Matter

Most heaps (binary, binomial) have O(log n) extract-min and decrease-key. In algorithms like Dijkstra's shortest path, if you make many decrease-key calls (which you do: one per edge), this adds up. A Fibonacci heap trades internal complexity for speed: O(1) amortized decrease-key and insert mean that for dense graphs with E >> V, Dijkstra runs in O((V + E) log V) instead of O(E log V).

The cost: more complex code, higher constants, and worst-case operations are slower (but amortized time is what matters for algorithm analysis).

## What's Inside

- **fibonacci_heap.py** — The core implementation:
  - FibonacciNode — Node structure with circular doubly-linked list pointers
  - FibonacciHeap — Main heap with insert, extract-min, decrease-key, delete, union, and size operations
  - Lazy merging of roots after extract-min and decrease-key
  - Cascading cuts to maintain amortized complexity
  - Consolidation to merge trees of equal degree after extract-min
  
- **test_fibonacci_heap.py** — Comprehensive test suite:
  - Unit tests for basic operations (insert, extract-min, find-min)
  - Tests for decrease-key and delete
  - Heap union (merge)
  - Verification that elements come out sorted (min-heap property holds)
  - Large-scale stress tests with 100+ elements
  - Edge cases: empty heap, single element, cascading cuts

## How to Use

### Basic Operations

from fibonacci_heap import FibonacciHeap

heap = FibonacciHeap()
node1 = heap.insert(5)
node2 = heap.insert(3)
node3 = heap.insert(7)

print(heap.find_min())  # Output: 3
min_key = heap.extract_min()
print(min_key)  # Output: 3

heap.decrease_key(node1, 1)
print(heap.extract_min())  # Output: 1
heap.delete(node3)
print(heap.size())

### Merging Heaps

heap1 = FibonacciHeap()
heap1.insert(5)
heap1.insert(3)

heap2 = FibonacciHeap()
heap2.insert(7)
heap2.insert(1)

heap1.union(heap2)
print(heap1.size())  # Output: 4
print(heap1.find_min())  # Output: 1

## Running Tests

python -m pytest test_fibonacci_heap.py -v
python -m unittest test_fibonacci_heap -v
python -m unittest test_fibonacci_heap.TestFibonacciHeap -v

## Algorithm & Complexity

### Operations and Amortized Time

| Operation | Amortized Time | Worst Case |
|-----------|----------------|----------|
| insert | O(1) | O(1) |
| find-min | O(1) | O(1) |
| extract-min | O(log n) | O(log n) |
| decrease-key | O(1) | O(log n) |
| delete | O(log n) | O(log n) |
| union | O(1) | O(1) |
| size | O(1) | O(1) |

### Key Design Decisions

1. Lazy consolidation: Trees are only merged when extract-min is called. This defers the O(log n) work until necessary.

2. Cascading cuts: When decrease-key violates the min-heap property (child < parent), we cut the child from the parent and promote it to the root list. If the parent was already cut once before, we recursively cut it too. This keeps tree degrees logarithmic without rebalancing after every operation.

3. Circular doubly-linked lists: The root list and each node's children are circular doubly-linked lists, so insertion, removal, and iteration are O(1).

4. Degree table in consolidate: After extract-min, a degree-to-root mapping ensures we process each tree only once and merge efficiently.

### Why It Works: Amortized Analysis

The amortized complexity comes from a potential function. Roughly: each decrease-key uses credit from a lower-potential state created by extract-min. The cascading cuts prevent too many cuts from accumulating. The result: O(1) amortized on average over many operations, even though some individual extract-min calls cost O(log n).

## Structure & Implementation Details

### FibonacciNode

Each node is a record:
- key, value — the data
- degree — number of children
- marked — flag for cascading cuts (marks a node that has lost a child but not yet lost a sibling)
- parent, child — pointers in the tree
- left, right — pointers in circular doubly-linked lists

### FibonacciHeap

Maintains:
- min_node — pointer to the minimum node (root of some tree)
- size_val — total number of nodes
- A forest of min-heap-ordered trees (the root list)

### Main Methods

- insert(key, value): Create a new node, add it to the root list, update min if needed. O(1).
- find_min(): Return min_node.key. O(1).
- extract_min(): Remove min node, promote its children to the root list, then consolidate. O(log n) amortized.
- decrease_key(node, new_key): Lower a node's key, cut if it violates heap property, cascade if parent was cut. O(1) amortized.
- delete(node): Decrease to -inf, then extract_min. O(log n) amortized.
- union(other): Splice root lists together, update min. O(1) amortized.
- _consolidate(): Merge trees of equal degree. Called after extract_min.
- _link(child, parent): Make child a child of parent (parent's degree increases by 1).
- _cut(child, parent): Remove child from parent's children, add to root list.
- _cascading_cut(node): Recursively cut marked nodes up the tree to maintain degree invariants.

## Test Coverage

The test suite includes:

1. Basic operations: insert, find-min, extract-min, delete
2. Decrease-key: with and without cascading cuts
3. Heap property: extracted elements are always in sorted order
4. Union: merging two heaps maintains correctness
5. Edge cases: empty heap, single element, operations on empty result
6. Stress tests: 100+ element sequences, large alternating insert/extract patterns
7. Tree structure: degree invariant (max degree ~ log n) is maintained after consolidation

Run the tests with python -m unittest test_fibonacci_heap. All tests should pass.

## Design Decisions & Trade-offs

### Why from scratch?

Implementing from scratch makes the amortization analysis concrete: you see exactly where O(1) comes from (lazy merging, cascading cuts) and why individual operations can be slow (consolidation is O(log n) but spread across many inserts).

### Circular lists vs. linear lists

Circular doubly-linked lists let us insert and remove nodes in O(1) without bookkeeping a separate head pointer. The code is slightly more complex (handling the cycle) but the gains are real.

### Marked nodes and cascading cuts

Without marks, decrease-key could trigger an unbounded chain of cuts, making it O(log n) or worse. With marks, at most one node gets cut per decrease-key (amortized). This is the subtle trick that makes the whole analysis work.

### No rank-based consolidation

Some Fibonacci heap implementations use a rank (logarithmic in n) and precompute it. This one computes max_degree = 64 which is enough for any practical heap size.

## References

- Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms, Chapter 19 (Fibonacci Heaps).
- Fredman & Tarjan. Fibonacci heaps and their uses in improved network optimization algorithms (1987) — the original paper.
- Dijkstra's algorithm: With Fibonacci heaps, the complexity is O((V + E) log V) vs. O(E log V) with binary heaps.

## License

MIT
