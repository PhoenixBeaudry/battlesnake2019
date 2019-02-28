#tester code for kornislav BFS implementation

import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def populateGraph(board):
    for edge in board.edges:
        board[edge[0]][edge[1]]['weight'] = 0

def enhance_cell(board, start_node, func):
    visited_edges = []
    for depth in range(1, len(board)):
        edge_list = list(nx.bfs_edges(board, start_node, depth_limit = depth))
        edge_list = list(set(edge_list) - set(visited_edges))
        for edge in edge_list:
            board[edge[0]][edge[1]]['weight'] = board[edge[0]][edge[1]]['weight'] + func(depth)
        if(visited_edges == visited_edges + edge_list):
            break
        visited_edges = visited_edges + edge_list


size = 5
graph = nx.grid_2d_graph(size, size)

populateGraph(graph)
f = lambda d : 5 - (d-1)*2
enhance_cell(graph, (2,2), f)

pos = {}
for node in graph:
	pos[node] = node
print(pos)

# nodes
nx.draw_networkx(graph, pos, font_size=8)

edges = {}

for edge in graph.edges:
	edges[edge] = graph[edge[0]][edge[1]]['weight']

nx.draw_networkx_edge_labels(graph, pos, edges, font_size=8)


plt.axis('off')
plt.gca().invert_yaxis()
plt.savefig("test")