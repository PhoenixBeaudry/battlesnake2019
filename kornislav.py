"""Kornislav the unbeatable Turtle"""
"""Built for BattleSnake 2019"""


import bottle, json, os
from bottle import Bottle, run, post, get, request, response
from json import dumps
import networkx as nx
from logic import *
from strategies import *
app = Bottle()



"""Root Response"""
@app.route('/')
def hello():
    return "Hello, World!"



"""Signals Game Start"""
@app.post('/start')
def start():
    try:
        data = bottle.request.json
    except:
        raise ValueError 

    val = {"color": "#ff00ff", "headType": "bendr", "tailType": "pixel"}

    response.content_type = 'application/json'
    
    return dumps(val)


"""Respond to Pings"""
@app.post('/ping')
def ping():
    return bottle.HTTPResponse(status=200)



@app.post('/test')
def test():
    newgraph = dummygraph()
    newgraph[(0,0)][(0,1)]['weight'] = 10
    print(newgraph[(0,0)][(0,1)])
    return bottle.HTTPResponse(status=200)





"""Server is requesting a Move"""
@app.post('/move')
def move():
    directions = ['up', 'down', 'left', 'right']
    try:
        data = bottle.request.json
    except:
        raise ValueError 

    gameboard = Board(data)

    board_graph = generate_graph(strat_one, gameboard)

    lightestedgeweight = 1000000
    lightestedge = None
    for edge in nx.edges(board_graph, gameboard.myself[0]):
        if(board_graph[edge[0]][edge[1]]['weight'] < lightestedgeweight):
            lightestedge = edge
            lightestedgeweight = board_graph[edge[0]][edge[1]]['weight']

    print(lightestedge)
    val = {"move": next_direction(gameboard.myself[0], lightestedge)}
    response.content_type = 'application/json'

    return dumps(val)


""" Game has ended """
@app.post('/end')
def end():
    return bottle.HTTPResponse(status=200)



run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

'''
if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
else:
    run(host='192.169.1.100', port=25565, debug=True)
'''