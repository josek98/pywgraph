import pywgraph as pwg
import numpy as np


dic = {
    "A": {
        "B": 2,
        "C": 10, 
        "D": 15
    },
    "B": {
        "A": 2,
        "C": 2,
        "D": 5
    }
}

grafo = pwg.WeightedDirectedGraph.from_dict(dic)
print(grafo)
grafo.add_reverse_edges(inplace=True)
print(grafo)