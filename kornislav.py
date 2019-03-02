"""Kornislav the unbeatable Turtle"""
"""Built for BattleSnake 2019"""


import bottle, json, os
from bottle import Bottle, run, post, get, request, response
from json import dumps
import networkx as nx
from logic import *
from strategies import *
import sys
app = Bottle()

debug = False
info = False

turncount = 1

"""Root Response"""
@app.route('/')
def hello():
    return "Hello, World!"


"""Signals Game Start"""
@app.post('/start')
def start():

    # Reset turn count at start of new game
    global turncount
    turncount = 1

    # Receive JSON data
    try:
        data = bottle.request.json
    except:
        raise ValueError 

    # Respond with Kornislavs Appearance
    val = {"color": "#ff00ff", "headType": "evil", "tailType": "bolt"}

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
    global turncount
    if(info):
        print("Turn: ", turncount)
    if(debug):
            print("Turn: ", turncount)
            print(data)


    # Generate the board data
    gameboard = Board(data)


    # Hungry/NotHungry Meta Strategy Implementation
    chosen_strategy = hungry

    # Populate edges according to current strategy
    board_graph = generate_graph(chosen_strategy, gameboard)


    # How far should we look ahead?
    foresight = 14

    # Select the lightest adjacent edge and move in that direction
    selected_move = next_direction(gameboard.myself[0], determine_safest_move(gameboard, board_graph, foresight, chosen_strategy))

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
if os.environ.get('APP_LOCATION') == 'heroku':
    run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(app, host="192.168.1.100", port=int(os.environ.get("PORT", 25565)))
