import networkx as nx
from strategies import *

import bottle
import copy

deadenddebug = False

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

# generate_graph:
# When passed the current gameboard information and a
# particular strategy dictionary it populates the graph
# with the desired edges weights
def generate_graph(strategy, gameboard):
    board = nx.grid_2d_graph(gameboard.size, gameboard.size)
    populate_graph(board)
    
    if(len(gameboard.myself) > 1):
        for bodypart in gameboard.myself[:-1]:
            enhance(board, bodypart, strategy['self_function'], myself=True)
        enhance(board, gameboard.myself[-1], strategy['tail_function'], myself=True)
    else:
        for bodypart in gameboard.myself:
            enhance(board, bodypart, strategy['self_function'], myself=True)

    for food in gameboard.food:
        enhance(board, food, strategy['food_function'])

    for enemy in gameboard.enemies:
        for enemypart in enemy:
            enhance(board, enemypart, strategy['enemy_function'])

    return board


# determine_safest_move:
# Returns the edge with the lightest weight adjacent to our head node
# that is also a safe move in 'foresight' steps
def determine_safest_move(gameboard, board_graph, foresight, strategy):
    lightestedgeweight = 10000000
    lightestedge = None
    prevedge = None
    currentedges = list(nx.edges(board_graph, gameboard.myself[0]))
    while(True):
        if(deadenddebug):
            print("All edges: ", currentedges)
        for edge in currentedges:
            if(board_graph[edge[0]][edge[1]]['weight'] < lightestedgeweight):
                prevedge = lightestedge
                lightestedge = edge
                lightestedgeweight = board_graph[edge[0]][edge[1]]['weight']
        if(deadenddebug):
            print("Testing-----------------------------------------: ", lightestedge)
        if(head_to_head(gameboard, lightestedge) = [] and safe_in_steps(gameboard, strategy, lightestedge, foresight)):
            return lightestedge
        else:
            if(len(currentedges) == 0):
                # Were dead anyway
                print("Were Dead Kid.")
                return lightest_adjacent_edge(gameboard, board_graph, edge)
            currentedges.remove(lightestedge)
            lightestedgeweight = 10000000


# see_into_future:
# After we choose a move, pretend we moved that square and run algorithm
# again. Repeat 'steps' times. If at any point were in a situation where we have
# no valid moves, we must have entered an area we could not have left
# Returns True on good move, False on bad
def safe_in_steps(gameboard, strategy, move, steps):
    if(steps <= 0):
        if(deadenddebug):
            print("Reached end of recursion! Step was safe!")
        return True
    # New pseudo board
    newgameboard = copy.deepcopy(gameboard)
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
    edge = lightest_adjacent_edge(newgameboard, newgraph, move)

    if(deadenddebug):
        print("Trying to move to: ", edge)
    if(newgraph[edge[0]][edge[1]]['weight'] < 1500000):
        # Move is safe!
        if(deadenddebug):
            print(str(edge) + " was safe! Going a step further!")
        return safe_in_steps(newgameboard, strategy, edge, steps-1)
    else:
        if(deadenddebug):
            print(str(edge) + " was not safe! Return!")
        return False

# edges_of_depth_distance:
# Returns all edges that are within a given depth
# radius from a particular start node
def edges_of_depth_distance(board, start_node, depth):
    nodebunch = {start_node}
    outer_radius = {start_node}
    if(depth == 1):
        return nx.edges(board, nbunch=nodebunch)
    else:
        for i in range(1, depth):
            newbunch = set()
            for node in outer_radius:
                for nbr in board[node]:
                    if nbr not in set(nodebunch):
                        newbunch.add(nbr)
            nodebunch = nodebunch + newbunch
            outer_radius = newbunch
            if(set(nodebunch) == set(nx.nodes(board))):
                print("AHA WEVE REACHED ALL THE NODES")
                break
        return nx.edges(board, nbunch=nodebunch)

# enhance:
# Given a starting node and an influence function of depth
# enhance spreads that nodes influence radially through all edges
# with a dropoff according to func(depth)
def enhance(board, start_node, func, max_depth=20, myself=False):
    weight = func(0)
    depth = 1
    visited_edges = []
    while weight:
        if depth > max_depth:
            break
        currentedges = edges_of_depth_distance(board, start_node, depth)
        currentedges = list(set(currentedges) - set(visited_edges))
        for edge in currentedges:
            board[edge[0]][edge[1]]['weight'] = board[edge[0]][edge[1]]['weight'] + weight
        if myself:
            break
        weight = func(depth)
        visited_edges = visited_edges + currentedges
        depth = depth + 1

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


#Returns lightest edge
def lightest_adjacent_edge(gameboard, board_graph, myedge):
    myedge = (myedge[1], myedge[0])
    lightestedgeweight = 10000000
    lightestedge = None
    currentedges = nx.edges(board_graph, gameboard.myself[0])
    for edge in currentedges:
        if(edge != myedge):
            if(board_graph[edge[0]][edge[1]]['weight'] < lightestedgeweight):
                lightestedge = edge
                lightestedgeweight = board_graph[edge[0]][edge[1]]['weight']
    return lightestedge


# populate_graph:
# Gives all edges in n*n board graph a default weight
def populate_graph(board):
    for edge in board.edges:
        board[edge[0]][edge[1]]['weight'] = 0

# detects if the potential space is adjacent to an enemy head
def head_to_head(gameboard, destination_edge):
    marker = 0
    if gameboard.myself[0] == destination_edge[0]:
        marker = 1
    else:
        marker = 0
    adjacent_spot = destination_edge[marker]
    enemy_head_list = []
    adjacent_spot = (adjacent_spot[0] + 1, adjacent_spot[1])
    for enemy_head in gameboard.enemies:
        if adjacent_spot == enemy_head[0]:
            enemy_head_list.append(enemy_head)
    adjacent_spot = destination_edge[marker]
    adjacent_spot = (adjacent_spot[0] - 1, adjacent_spot[1])
    for enemy_head in gameboard.enemies:
        if adjacent_spot == enemy_head[0]:
            enemy_head_list.append(enemy_head)
    adjacent_spot = destination_edge[marker]
    adjacent_spot = (adjacent_spot[0], adjacent_spot[1] + 1)
    for enemy_head in gameboard.enemies:
        if adjacent_spot == enemy_head[0]:
            enemy_head_list.append(enemy_head)
    adjacent_spot = destination_edge[marker]
    adjacent_spot = (adjacent_spot[0], adjacent_spot[1] - 1)
    for enemy_head in gameboard.enemies:
        if adjacent_spot == enemy_head[0]:
            enemy_head_list.append(enemy_head)
    return enemy_head_list