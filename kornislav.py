"""Kornislav the unbeatable Turtle"""
"""Built for BattleSnake 2019"""


import bottle, json, os
from bottle import Bottle, run, post, get, request, response
from json import dumps
app = Bottle()



"""Root Response"""
@app.get('/')
def hello():
    return "Hello, World!"



"""Signals Game Start"""
@app.post('/start')
def start():

    try:
        data = request.json
    except:
        raise ValueError 

    val = [{"cool": "cool"}]
    response.content_type = 'application/json'

    return dumps(val)


"""Signals Game Start"""
@app.post('/ping')
def ping():
    return bottle.HTTPResponse(status=200)





"""Server is requesting a Move"""
@app.post('/move')
def move():
    try:
        data = request.json
    except:
        raise ValueError 

    val = [{"move": "right"}]
    response.content_type = 'application/json'

    return dumps(val)

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
else:
    run(host='192.169.1.100', port=25565, debug=True)
