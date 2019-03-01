#tester code for kornislav BFS implementation

import networkx as nx

def populateGraph(board):
    for edge in board.edges:
        board[edge[0]][edge[1]]['weight'] = 0

#
#polarity is 1 or -1, to define whether the cell to be enhanced
#is at the apex of a topographical hill (1) or the bottom of a valley (-1)
#
#NOTE: if polarity does not match weight, this function will fail and return
#		immediately
def enhance_new(board, start_node, func, polarity=1):
	visited_edges = []
	def recursive_enhance(b, w, d, s, f):
		if polarity > 0:
			if w <= 0: return
		else:
			if w >= 0: return
		ns = [] #node list
		es = [] #edge list
		for e in b.edges(nbunch=s):
			es.append(e)
		for n1,n2 in es:
			n2x,n2y = n2
			sx,sy = start_node
			if (n1,n2) not in visited_edges and (n2,n1) not in visited_edges and (abs(n2x-sx)+abs(n2y-sy))==d:
				b.adj[n1][n2]['weight'] = b.adj[n1][n2]['weight'] + w
				visited_edges.append((n1,n2))
			ns.append(n2)
		for n in ns:
			recursive_enhance(b, f(d), d+1, n, f)
	recursive_enhance(board, func(0), 1, start_node, func)

size = 5
graph = nx.grid_2d_graph(size, size)
populateGraph(graph)
#return a function that linearly increments the weight
def linear_decay(weight, inc):
	return lambda depth : weight - depth*inc

#return a function that increments the weight polynomially
def poly_decay(weight, poly, sign=1):
    return lambda depth: weight + (-1*sign)*poly**depth

enhance_new(graph, (2,2), linear_decay(5,1))

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


print "adjacency list: "
for n, nbrs in graph.adj.items():
	print str(n) + " -> " + str(nbrs)