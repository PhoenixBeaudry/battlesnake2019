#tester code for kornislav BFS implementation

import networkx as nx

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

edges = []

for edge in graph.edges:
	a = edge[0][0]
	b = edge[0][1]
	c = edge[1][0]
	d = edge[1][1]
	if (a+b) > (c+d):
		ta = a
		tb = b
		a = c
		b = d
		c = ta
		d = tb

	edges.append([a,b,c,d,graph[edge[0]][edge[1]]['weight']])

for i in [0, 2, 1, 3]:
	edges = sorted(edges, key = lambda x : x[i])

w = []
for e in edges:
	#print e
	w.append(e[4])

wi = 0
for i in xrange(size*2 - 1):
	if i%2==0:
		pl = "   "
		for j in xrange(size-1):
			pl = pl + str(w[wi]).rjust(3) + "   "
			wi = wi + 1
	else:
		pl = ""
		for j in xrange(size):
			pl = pl + str(w[wi]).rjust(3) + "   "
			wi = wi + 1
	print pl
	
'''
for edge in graph.edges:
	print str(edge) + " weight = " + str(graph[edge[0]][edge[1]]['weight'])
'''