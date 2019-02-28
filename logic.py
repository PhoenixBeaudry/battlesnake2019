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


def generate_graph(strategy, 2dgameboard):
    board = nx.grid_2d_graph(5, 5)
    print(board)
    return 0