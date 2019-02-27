"""Kornislav the unbeatable Turtle"""
"""Built for BattleSnake 2019"""


import bottle, json, os
from bottle import Bottle, run, post, get, request, response
from json import dumps
from logic import *
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





"""Server is requesting a Move"""
@app.post('/move')
def move():
    directions = ['up', 'down', 'left', 'right']
    try:
        data = bottle.request.json
        game_id = data['game']
        board_width = data['board']['width']
        board_height = data['board']['height']
    except:
        raise ValueError 

    val = {"move": "right"}
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