#tester code for kornislav BFS implementation

import networkx as nx

def populateGraph(board):
    for edge in board.edges:
        board[edge[0]][edge[1]]['weight'] = 0

def edges_of_depth_distance(board, start_node, depth):
    nodebunch = [start_node]
    if(depth == 1):
        return nx.edges(board, nbunch=nodebunch)
    else:
        for i in range(1, depth):
            newbunch = []
            for node in nodebunch:
                for nbr in board[node]:
                    if nbr not in nodebunch:
                        newbunch.append(nbr)
            nodebunch = nodebunch + newbunch

        return nx.edges(board, nbunch=nodebunch)

def enhance(board, start_node, func, myself=False):
    weight = func(0)
    depth = 1
    visited_edges = []
    while weight > 0:
        edges_at_depth = edges_of_depth_distance(board, start_node, depth)
        for edge in edges_at_depth:
            board.adj[edge[0]][edge[1]]['weight'] = board.adj[edge[0]][edge[1]]['weight'] + weight
        weight = func(depth)
        depth = depth + 1

size = 5
graph = nx.grid_2d_graph(size, size)
populateGraph(graph)

def linear_decay(weight, inc):
	return lambda depth : (weight - depth*inc) if (weight - depth*inc) > 0 else 0

#return a function that increments the weight polynomially
def poly_decay(weight, poly):
	if weight>0:
		return lambda depth: (weight - depth**poly) if (weight - depth**poly) > 0 else 0
	else:
		return lambda depth: (weight + depth**poly) if (weight - depth**poly) < 0 else 0

def self_function():
	return 1000000

enhance(graph, (2,2), linear_decay(5,2))

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
	print(pl)

'''
print "adjacency list: "
for n, nbrs in graph.adj.items():
	print str(n) + " -> " + str(nbrs)
	'''