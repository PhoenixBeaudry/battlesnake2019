import networkx as nx
import bottle

class Board:
    def __init__(self, data):
        try:
            data = bottle.request.json
        except:
            raise ValueError 
        size = data['board']['width']
        food_list = []
        for food in data['board']['food']:
            x = food['x']
            y = food['y']
            food_list.append((x,y))


def generate_graph(strategy, gameboard):
    board = nx.grid_2d_graph(5, 5)
    return board

def enhance_cell(board, start_node, func):
    visited_edges = []

    for depth in range(1, len(board)):
        print("Depth = ", depth)
        edge_list = list(nx.bfs_edges(board, start_node, depth_limit=depth))
        edge_list = list(set(edge_list) - set(visited_edges))
        for edge in edge_list:
            edge['weight'] = edge['weight'] + func(depth)
        visited_edges = visited_edges + edge_list
