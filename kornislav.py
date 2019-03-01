"""Kornislav the unbeatable Turtle"""
"""Built for BattleSnake 2019"""


import bottle, json, os
from bottle import Bottle, run, post, get, request, response
from json import dumps
import networkx as nx
from logic import *
from strategies import *
app = Bottle()

debug = True

turncount = 1

"""Root Response"""
@app.route('/')
def hello():
    return "Hello, World!"


"""Signals Game Start"""
@app.post('/start')
def start():

    # Reset turn count at start of new game
    turncount = 1

    # Receive JSON data
    try:
        data = bottle.request.json
    except:
        raise ValueError 

    # Respond with Kornislavs Appearance
    val = {"color": "#ff00ff", "headType": "bendr", "tailType": "pixel"}

    response.content_type = 'application/json'
    
    return dumps(val)


"""Respond to Pings"""
@app.post('/ping')
def ping():
    return bottle.HTTPResponse(status=200)


"""Local Testing Method"""
""" Responds to POST requests to the /test route """
@app.post('/test')
def test():
    newgraph = dummygraph()
    newgraph[(0,0)][(0,1)]['weight'] = 10
    print(newgraph[(0,0)][(0,1)])
    return bottle.HTTPResponse(status=200)


"""Server is requesting a Move"""
@app.post('/move')
def move():

    # Recieve JSON data
    try:
        data = bottle.request.json
    except:
        raise ValueError

    # If we are in debugging mode, every 100 turns
    # Kornislav will output the current gameboard state data
    # which can then be used in tester.py to determine his thinking
    if(debug):
        '''
        if(turncount%100 == 0):
            print(data)
        '''
        print(data)

    # Generate the board graph and populate its edges
    gameboard = Board(data)
    board_graph = generate_graph(strat_one, gameboard)

    # Select the lightest adjacent edge and move in that direction
    selected_move = next_direction(gameboard.myself[0], lightest_adjacent_edge(gameboard, board_graph))
    
    # Move to next turn
    turncount = turncount + 1

    #Respond with our move decision
    val = {"move": selected_move}
    response.content_type = 'application/json'
    return dumps(val)


""" Game has ended """
@app.post('/end')
def end():
    return bottle.HTTPResponse(status=200)

# Start Kornislav
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

