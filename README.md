# pywgraph
A library to manipulate weighted graphs in python. This library focus on directed graphs whose edges have weights. The goal is that the weights can be any set o objects that have an intern binary operation and an inverse. In mathematical meanings, a group. The reason behind this is to be able to trasverse the graph using the group operation. 

In the actual version, the weight is only allowed to be a float, and the operation is the multiplication. When the package has almost all of the necessary features to be used, I will add the possibility to use other types of weights.

## QUICKSTART

### Edges

The main object to construct the graph is the `WeightedDirectedEdge` class. This represents a directed edge with a weight. The construction is as follows: 

```python
from pywgraph import WeightedDirectedEdge

edge = WeightedDirectedEdge("A", "B", 0.5)
```

The first two parameters are the nodes that the edge connects. The last parameter is the weight. It is important to notice that, since this is a directed edge, the order of the nodes is important.

You can call the start and end nodes with `edge.start` and `edge.end`, respectevely. To get the weight, simply use `edge.weight`. You can also get the *inverse edge* with `edge.inverse`. This is, the edge that connects the end node of `edge` to the start node of `edge` and has `1/edge.weight` as weight (as said previously, in the future this is meant to be the inverse of the weight in the underlying group).

Also, this class is hashable and iterable, yielding the start node, end node and weight. 


### Graph

The graph is represented by the `WeightedDirectedGraph` class. This class is the main class of the package. The graph itself is a set of nodes and a set of `WeightedDirectedEdge`s. 

It is also possible, and more comfortable, to create the graph using the `WeightedDirectedGraph.from_dict` method, which instantiates the graph from a dictionary. The keys of the dictionary are the starting nodes. The values must consists of another dictionary, where the keys are the ending nodes and the value is the weight of the edge. It is important that all nodes of the graph must be keys in the dictionary. If, for example, there is a node "C" that has no children nodes, then the dictionary must have a key "C" with a value of `{}`.

```python
from pywgraph import WeightedDirectedGraph

g = WeightedDirectedGraph.from_dict({
    "A": {"B": 0.5},
    "B": {"A": 0.5, "C": 1.0},
    "C": {}
})
```

The equivalent construction using set of nodes and set of edges is as follows: 

```python 
from pywgraph import WeightedDirectedGraph

graph = WeightedDirectedGraph(
    nodes={"A", "B", "C"},
    edges={
        WeightedDirectedEdge("A", "B", 0.5),
        WeightedDirectedEdge("B", "A", 0.5),
        WeightedDirectedEdge("B", "C", 1.0)
    }
)
``` 

You can instantiate a bad define graph by not writting all the nodes that appear in the edges in the nodes set. There is a method `check_defintion` that checks if the graph is well defined, but the check is not enforce. You can retrieve the nodes and edges by `graph.nodes` and `graph.edges`, respectively.

You can also acces the children and the parents of a nodes with the methods `children` and `parents`, respectively.

```python
graph.children("A")
# {"B"}

graph.parents("A")
# {}

graph.children("B")
# {"A", "C"}
```

The main use of this graph object is to work with their weights as group elements, so you should not add the reverse edge of an existing edge with a bad inverse weight. For this, there is the method `add_reverse_edges` that returns a new graph with the original graph with all the reverse edges added. You can also modify the graph directly with the paremeter `inplace=True`. 

```python
graph_w_inverse_edges = graph.add_reverse_edges()

# Updating the graph 
graph.add_reverse_edges(inplace=True)
```

### Path finding

There is a method `find_path` that finds one of the shortest path between two nodes. This method returns a list of edges that represents the path. The method has two parameters: `start` and `end`. Both must be nodes of the graph. If not, an error is raised. If there is not path between the given nodes the empty list will be return. 

```python
dictionary = {
    "A": {"B": 1.0, "C": 2.5},
    "B": {"C": 2.5},
    "C": {"A": 1 / 2.5, "D": 1.3},
    "D": {"E": 3.4},
    "E": {"C": 1 / (1.3 * 3.4), "A": 13.0},
    "Z": {},
}
graph = WeightedDirectedGraph.from_dict(dictionary)

graph.find_path("A", "B")
# ["A", "B]

graph.find_path("A", "Z")
# []

graph.find_path("A", "E")
# ["A", "C", "D", "E"]

graph.find_path("A", "A")
# ["A"]
```

There are also methods to get the weight of following a path. This methods are `path_weight` and `weight_between`. The first one receives a path (a list of consecutive nodes) and returns the weight of the path (the product of the weights). If the given path does not exists an exception will be raised. If the empty path is given the return weight will be `0`. The second method receives the start and end nodes and returns the weight of one of the shortest paths between them. If there is not path between the given nodes the return weight will be `0`. The weight between a node an itself will be `1`. 

```python
graph.path_weight([])
# 0.0

graph.path_weight(["A", "B"])
# 1.0

graph.path_weight(["A", "B", "C"])
# 2.5

grap.weight_between("A", "C")
# 2.5

grap.weight_between("A", "Z")
# 0.0

grap.weight_between("A", "A")
# 1.0
```

**WARNING**: Currently, if a path that contains a cycle is given the method `path_weight` will raise an error. In future this behaviour will be change to allow cycles. 