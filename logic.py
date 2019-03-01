import networkx as nx
from strategies import *

import bottle

class Board:
    size = 0
    food = None
    enemies = None
    myself = None
    def __init__(self, data):
        
        self.food = []
        snake_body = []
        self.enemies = []
        self.myself = []

        #gets the size of board
        self.size = data['board']['width']

        # lists the food
        for foodpiece in data['board']['food']:
            x = foodpiece['x']
            y = foodpiece['y']
            self.food.append((x,y))
        
        # creates a list of snakes
        for snake in data['board']['snakes']:
            snakebody = snake['body']
            for body in snakebody:
                x = body['x']
                y = body['y']
                snake_body.append((x,y))
            self.enemies.append(snake_body)
            snake_body = []

        # creates a location of ourselves
        for body in data['you']['body']:
            x = body['x']
            y = body['y']
            self.myself.append((x,y))
        
def next_direction(snake_head, input_destination):

    if snake_head == input_destination[0]:
        destination = input_destination[1]
    else:
        destination = input_destination[0]

    if snake_head[0] - destination[0] == 0 and snake_head[1] - destination[1] > 0:
        return "up"
    if snake_head[0] - destination[0] == 0 and snake_head[1] - destination[1] < 0:
        return "down"
    if snake_head[0] - destination[0] < 0 and snake_head[1] - destination[1] == 0:
        return "right"
    if snake_head[0] - destination[0] > 0 and snake_head[1] - destination[1] == 0:
        return "left"

def dummygraph():
    return nx.grid_2d_graph(10, 10)
    
def generate_graph(strategy, gameboard):
    board = nx.grid_2d_graph(gameboard.size, gameboard.size)
    populateGraph(board)

    for bodypart in gameboard.myself:
        enhance_new(board, bodypart, strategy['self_function'], myself=True)

    for food in gameboard.food:
        enhance_new(board, food, strategy['food_function'])

    for enemy in gameboard.enemies:
        for enemypart in enemy:
            enhance_new(board, enemypart, strategy['enemy_function'])

    return board

#
#polarity is 1 or -1, to define whether the cell to be enhanced
#is at the apex of a topographical hill (1) or the bottom of a valley (-1)
#
#NOTE: if polarity does not match weight, this function will fail and return
#       immediately


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



def enhance_new(board, start_node, func, myself=False):
    visited_edges = []
    def recursive_enhance(b, w, d, s, f):
        if w == 0: return
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
        if not myself:
            for n in ns:
                recursive_enhance(b, f(d), d+1, n, f)
    recursive_enhance(board, func(0), 1, start_node, func)

def populateGraph(board):
    for edge in board.edges:
        board[edge[0]][edge[1]]['weight'] = 0