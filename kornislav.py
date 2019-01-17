"""Kornislav the unbeatable Turtle"""
"""Built for BattleSnake 2019"""


import bottle, json
from bottle import Bottle, run, post, get, request, response
from json import dumps
app = Bottle()


"""Decorator used to enable CORS on HTTP Responses"""
"""Code taken from https://stackoverflow.com/questions/17262170/bottle-py-enabling-cors-for-jquery-ajax-requests"""
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors




"""Root Response"""
@app.route('/')
def hello():
    return "Hello, World!"



"""Signals Game Start"""
@app.post('/start')
@enable_cors
def start():

    try:
        data = request.json
    except:
        raise ValueError 

    val = [{"cool": "cool"}]
    response.content_type = 'application/json'

    return dumps(val)





"""Server is requesting a Move"""
@app.post('/move')
@enable_cors
def move():
    try:
        data = request.json
    except:
        raise ValueError 

    val = [{"cool": "cool"}]
    response.content_type = 'application/json'

    return dumps(val)



run(app, host='192.168.1.100', port=25565)
