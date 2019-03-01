import networkx as nx
from strategies import *

import bottle

# Board:
# Holds basic board information about size, food, and enemy snakes
class Board:
    size = 0
    food = None
    enemies = None
    myself = None
    myhealth = 0
    def __init__(self, data):
        
        self.food = []
        snake_body = []
        self.enemies = []
        self.myself = []
        self.myhealth = data['you']['health']

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

        if self.myself in self.enemies:
            self.enemies.remove(self.myself)


# next_direction:
# Given an edge incident to our snake_head node it returns 
# the direction in which to move to travel that edge        
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


# generate_graph:
# When passed the current gameboard information and a
# particular strategy dictionary it populates the graph
# with the desired edges weights
def generate_graph(strategy, gameboard):
    board = nx.grid_2d_graph(gameboard.size, gameboard.size)
    populate_graph(board)

    for bodypart in gameboard.myself:
        enhance(board, bodypart, strategy['self_function'], myself=True)

    for food in gameboard.food:
        enhance(board, food, strategy['food_function'])

    for enemy in gameboard.enemies:
        for enemypart in enemy:
            enhance(board, enemypart, strategy['enemy_function'])

    return board


# lightest_adjacent_edge:
# Returns the edge with the lightest weight adjacent to our head node
# that is also a safe move in 'foresight' steps
def determine_safest_move(gameboard, board_graph, foresight, strategy):
    lightestedgeweight = 10000000
    lightestedge = None
    currentedges = list(nx.edges(board_graph, gameboard.myself[0]))
    while(True):
        for edge in currentedges:
            if(board_graph[edge[0]][edge[1]]['weight'] < lightestedgeweight):
                lightestedge = edge
                lightestedgeweight = board_graph[edge[0]][edge[1]]['weight']
        if(safe_in_steps(gameboard, strategy, lightestedge, foresight)):
            break
        else:
            if(len(currentedges) == 0):
                # Were dead anyway
                return lightest_adjacent_edge(gameboard, board_graph)
            currentedges.remove(edge)

    return lightestedge


#Returns lightest edge
def lightest_adjacent_edge(gameboard, board_graph):
    lightestedgeweight = 10000000
    lightestedge = None
    currentedges = nx.edges(board_graph, gameboard.myself[0])
    for edge in currentedges:
        if(board_graph[edge[0]][edge[1]]['weight'] < lightestedgeweight):
            lightestedge = edge
            lightestedgeweight = board_graph[edge[0]][edge[1]]['weight']
    return lightestedge


# edges_of_depth_distance:
# Returns all edges that are within a given depth
# radius from a particular start node
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


# enhance:
# Given a starting node and an influence function of depth
# enhance spreads that nodes influence radially through all edges
# with a dropoff according to func(depth)
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


# populate_graph:
# Gives all edges in n*n board graph a default weight
def populate_graph(board):
    for edge in board.edges:
        board[edge[0]][edge[1]]['weight'] = 0



# see_into_future:
# After we choose a move, pretend we moved that square and run algorithm
# again. Repeat 'steps' times. If at any point were in a situation where we have
# no valid moves, we must have entered an area we could not have left
# Returns True on good move, False on bad
def safe_in_steps(gameboard, strategy, move, steps):
    if(steps <= 0):
        return True
    # New pseudo board
    newgameboard = gameboard
    # Determine location of new head node
    if newgameboard.myself[0] == move[0]:
        movenode = move[1]
    else:
        movenode = move[0]

    #Move our position as if we moved there
    newgameboard.myself.insert(0, movenode)
    del newgameboard.myself[-1]

    # Generate new graph
    newgraph = generate_graph(strategy, newgameboard)

    # Determine if lightest edge is below threshold
    edge = lightest_adjacent_edge(newgameboard, newgraph)
    if(newgraph[edge[0]][edge[1]]['weight'] < 1500000):
        # Move is safe!
        return safe_in_steps(newgameboard, strategy, lightest_adjacent_edge(newgameboard, newgraph), steps-1)
    else:
        return False

