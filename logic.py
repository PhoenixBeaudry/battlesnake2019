import networkx as nx
from strategies import *

import bottle

class Board:
    def __init__(self, data):
        try:
            data = bottle.request.json
        except:
            raise ValueError 
        
        food_list = []
        snake_body = []
        snake_list = []
        our_snake = []

        #gets the size of board
        size = data['board']['width']

        # lists the food
        for food in data['board']['food']:
            x = food['x']
            y = food['y']
            food_list.append((x,y))
        
        # creates a list of snakes
        for snake in data['board']['snakes']:
            for body in snake:
                x = snake['x']
                y = snake['y']
                snake_body.append((x,y))
            snake_list.append(snake_body)
            snake_body = []

        # creates a location of ourselves
        for body in data['you']:
            x = body['x']
            y = body['y']
            our_snake.append((x,y))
        
def next_direction(snake_head, input_destination):

    if snake_head[0] == input_destination[0][0] and snake_head[1] == input_destination[0][1]:
        destination = input_destination[1]
    else:
        destination = input_destination[0]

    if snake_head[0] - destination[0] == 0 and snake_head[1] - destination[1] < 0:
        return "up"
    if snake_head[0] - destination[0] == 0 and snake_head[1] - destination[1] > 0:
        return "down"
    if snake_head[0] - destination[0] < 0 and snake_head[1] - destination[1] == 0:
        return "right"
    if snake_head[0] - destination[0] > 0 and snake_head[1] - destination[1] == 0:
        return "left"

def generate_graph(strategy, gameboard):
    board = nx.grid_2d_graph(gameboard.size, gameboard.size)
    for food in gameboard.food:
        enhance_cell(board, food, strategy['food_function'])

    for enemy in gameboard.enemies:
        enhance_cell(board, enemy, strategy['enemy_function'])

    for bodypart in gameboard.myself:
        enhance_cell(board, bodypart, strategy['self_function'], myself=True)

    return board

def enhance_cell(board, start_node, func, myself=False):
    visited_edges = []
    if(myself):
        edge_list = list(nx.bfs_edges(board, start_node, depth_limit=1))
        edge_list = list(set(edge_list) - set(visited_edges))
        for edge in edge_list:
            edge['weight'] = edge['weight'] + func(depth)
        visited_edges = visited_edges + edge_list
    else:
        for depth in range(1, len(board)):
        print("Depth = ", depth)
        edge_list = list(nx.bfs_edges(board, start_node, depth_limit = depth))
        edge_list = list(set(edge_list) - set(visited_edges))
        for edge in edge_list:
            edge['weight'] = edge['weight'] + func(depth)
        visited_edges = visited_edges + edge_list

