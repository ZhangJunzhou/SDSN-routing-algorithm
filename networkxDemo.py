from matplotlib import pyplot as plt
import networkx as nx


nodes = [0,1,2,3,4]
edges = [(0,1,10),(0,3,30),(0,4,100),(1,2,50),(2,3,20),(2,4,10),(3,4,60)]

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

path = nx.single_source_dijkstra_path(G,4)
length = nx.single_source_dijkstra_path_length(G,4)
print(path)
print(length)
nx.draw_networkx(G)
plt.show()