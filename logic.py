import networkx as nx


class Board:
    def __init__(self, data):

        def generate_board():
            try:
                data = bottle.request.json
            except:
                raise ValueError 
            game_id = data['game']
            board_width = data['board']['width']
            board_height = data['board']['height']
            decision = 'right'
            return decision


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
        edge_list = list(nx.bfs_edges(board, start_node, depth_limit=depth))
        edge_list = list(set(edge_list) - set(visited_edges))
        for edge in edge_list:
            edge['weight'] = edge['weight'] + func(depth)
        visited_edges = visited_edges + edge_list
