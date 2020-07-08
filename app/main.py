import json
import os
import random
import bottle
from game import *
from api import ping_response, start_response, move_response, end_response

# TensorFlow and tf.kerasi
import tensorflow as keras
import tensorflow as tf

# Helper libraries
import numpy as np
model = tf.keras.models.load_model('active_model/nextgen_1')
probability_model = tf.keras.Sequential([model,tf.keras.layers.Softmax()])

defaultMap = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def getMaxIndex(arr):
    maxValue = arr[0]
    index = 0
    counter = 0
    for x in arr:
        if(maxValue < x):
            maxValue = x
            index = counter
        counter = counter + 1
    return index


def pickMove(inputs):
    # direction = random.choice(directions)
    directions = []
    values = probability_model.predict([inputs])
    #print(values)
    index = getMaxIndex(values[0])
    #print(index)
    # print(index)
    if(index >= 8):
        directions.append('right')
        index = index - 8
    if(index >= 4):
        directions.append('left')
        index = index - 4
    if(index >= 2):
        directions.append('down')
        index = index -2
    if(index ==1):
        directions.append('up')
    if(len(directions)==0):
        # print('no moves left, killing self')
        return random.choice(['up','down','left','right'])
    return random.choice(directions)


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"
    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    print(json.dumps(data))
    listMap=defaultMap
    # fill map with data from the model
    filledMap = fillMap(listMap,data)
    printMap(filledMap)
    inputs = genInputs(listMap,data)
    direction = pickMove(inputs)
    print(direction)
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


