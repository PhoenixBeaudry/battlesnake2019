import networkx as nx
import bottle

class Board:
    def __init__(self, data):

        def size():
            try:
                data = bottle.request.json
            except:
                raise ValueError 
            board_size = data['board']['width']
            return board_size
        def food():
            food_list = []
            try:
                data = bottle.request.json
            except:
                raise ValueError 
            for food in data['board']['food']:
                x = data['x']
                y = data['y']
                food_list.append(tuple([x,y]))
            return food


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
