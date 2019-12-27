import time
import json

from bottle import run, post, request, response

PIXEL_COUNT = 31
SPI_PORT = 0
SPI_DEVICE = 0
pixels = 0


@post('/rainbowS')
def rainbow_sequence():
    req_obj = json.loads(request.body.read())
    print(req_obj)
    return "{state: 1}"


@post('/rainbowC')
def rainbow_cycle():
    req_obj = json.loads(request.body.read())
    print(req_obj)
    return "{state: 2}"


@post('/rainbowColors')
def rainbow_colors():
    req_obj = json.loads(request.body.read())
    print(req_obj)
    return "{state: 3}"


@post('/solid')
def solid():
    req_obj = json.loads(request.body.read())
    print(req_obj)
    return "{state: 3}"


@post('/intensity')
def brightness_decrease():
    req_obj = json.loads(request.body.read())
    print(req_obj)
    return "{state: 4}"


run(host='localhost', port=8080, debug=True)
