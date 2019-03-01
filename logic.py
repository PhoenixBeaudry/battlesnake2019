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
        enhance(board, bodypart, strategy['self_function'], myself=True)

    for food in gameboard.food:
        enhance(board, food, strategy['food_function'])

    for enemy in gameboard.enemies:
        for enemypart in enemy:
            enhance(board, enemypart, strategy['enemy_function'])

    return board


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
    while weight != 0:
        currentedges = edges_of_depth_distance(board, start_node, depth)
        currentedges = list(set(currentedges) - set(visited_edges))
        for edge in currentedges:
            board.adj[edge[0]][edge[1]]['weight'] = board.adj[edge[0]][edge[1]]['weight'] + weight
        if myself:
            break
        weight = func(depth)
        visited_edges = visited_edges + currentedges
        depth = depth + 1

def populateGraph(board):
    for edge in board.edges:
        board[edge[0]][edge[1]]['weight'] = 0