import time
import json
import RPi.GPIO as GPIO
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
# Import bottle simple http server
from bottle import run, post, request, response
# Dynamically find IP
import socket
# Create thread to handle replaying certain animations forever
import threading
import queue

IP = ""
PIXEL_COUNT = 31
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT = 0
SPI_DEVICE = 0
INTENSITY = 10
QUEUE = queue.Queue()

pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

def get_IP():
    global IP
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect(('8.8.8.8', 1))
    IP = soc.getsockname()[0]

# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)


# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256))
        set_intensity(i)
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def rainbow_cycle(pixels, wait=0.005):
    for j in range(256):  # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256))
            set_intensity(i)
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def rainbow_colors(pixels, wait=0.05):
    for j in range(256):  # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256))
            set_intensity(i)
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def brightness_decrease(pixels, steps=256, wait=0.01, step=1):
    for j in range(int(steps // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def brightness_increase(pixels, steps=256, wait=0.01, step=1):
    for j in range(int(steps // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(min(255, r + step))
            g = int(min(255, g + step))
            b = int(min(255, b + step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def blink_color(pixels, blink_times=5, wait=0, color=[255, 0, 0]):
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(color[0], color[2], color[1]))
                set_intensity(k)
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)


def appear_from_back(pixels, color=[255, 0, 0], wait=0):
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(color[0], color[2], color[1]))
                set_intensity(k)
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(color[0], color[2], color[1]))
            set_intensity(j)
            pixels.show()
            time.sleep(wait)


def solid_colors(pixels, color=[255, 0, 0], wait=0):
    for i in range(pixels.count()):
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(color[0], color[2], color[1]))
        set_intensity(i)
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def solid_array(pixels, arr, wait=0):
    for i in range(pixels.count()):
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(arr[i][0], arr[i][2], arr[i][1]))
        set_intensity(i)
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def set_intensity(index):
    try:
        r, b, g = pixels.get_pixel_rgb(index)
        ratio = INTENSITY / 255
        r = int(r * ratio)
        g = int(g * ratio)
        b = int(b * ratio)
        pixels.set_pixel(index, Adafruit_WS2801.RGB_to_color(r, b, g))
    except():
        return False
    return True


@post('/rainbowS')
def rainbow_sequence_set():
    req_obj = json.loads(request.body.read())
    wait_time = 0.1
    if req_obj.get('wait'):
        wait_time = req_obj.get('wait')
    rainbow_cycle_successive(pixels, wait_time)
    return '{"success": True}'


@post('/rainbowC')
def rainbow_cycle_set():
    req_obj = json.loads(request.body.read())
    wait_time = 0.005
    if req_obj.get('wait'):
        wait_time = req_obj.get('wait')
    rainbow_cycle(pixels, wait_time)
    return '{"success": True}'


@post('/rainbowColors')
def rainbow_colors_set():
    req_obj = json.loads(request.body.read())
    wait_time = 0.05
    if req_obj.get('wait'):
        wait_time = req_obj.get('wait')
    rainbow_colors(pixels, wait_time)
    return '{"success": True}'


@post('/solid')
def solid_set():
    req_obj = json.loads(request.body.read())
    wait_time = 0
    if req_obj.get('wait'):
        wait_time = req_obj.get('wait')
    color = [255, 0, 0]
    if req_obj.get('color'):
        color = req_obj.get('color')
    solid_colors(pixels, color, wait_time)
    return '{"success": True}'


@post('/solidArr')
def solid_arr_set():
    req_obj = json.loads(request.body.read())
    wait_time = 0
    if req_obj.get('wait'):
        wait_time = req_obj.get('wait')
    colors = [(255, 0, 4)] * PIXEL_COUNT
    if req_obj.get('colors'):
        colors = req_obj.get('colors')
    solid_array(pixels, colors, wait_time)
    return '{"success": True}'


@post('/intensity')
def intensity_set():
    global INTENSITY
    req_obj = json.loads(request.body.read())
    intensity_target = req_obj.get('target')
    wait_time = 0.01
    if req_obj.get('wait'):
        wait_time = req_obj.get('wait')
    step_size = 1
    if req_obj.get('step_size'):
        step_size = req_obj.get('stepSize')
    if req_obj.get('force') and req_obj.get('force') == "True":
        if intensity_target > INTENSITY:
            INTENSITY = min(255, intensity_target)
        else:
            INTENSITY = max(0, intensity_target)
    else:
        if intensity_target > INTENSITY:
            brightness_increase(pixels, min(256, intensity_target - INTENSITY), wait_time, step_size)
            INTENSITY = min(255, intensity_target)
        elif intensity_target < INTENSITY:
            brightness_decrease(pixels, min(256, INTENSITY - intensity_target), wait_time, step_size)
            INTENSITY = max(0, intensity_target)
    return "{intensity: " + str(INTENSITY) + "}"


@post('/appearfromback')
def appear_from_back_set():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('appearfromback', req_obj, True))
    return '{"success": True}'

def build_task(task, body, replay=False):
    return {'task': task, 'body': body, 'replay': replay}

def worker():
    while True:
        item = QUEUE.get()
        # This ends the worker thread and sets the last light to be red to indicate the server is not running properly1wqa1
        if item is None:
            pixels.clear()
            pixels.set_pixel(30, Adafruit_WS2801.RGB_to_color(255, 0, 0))
            pixels.show()
            print(QUEUE.empty())
            break
        else:
            data = item.get('body')
            color = [255, 0, 4]
            if data.get('color'):
                color = data.get('color')
            wait_time = 0
            if data.get('wait'):
                wait_time = data.get('wait')
            if item.get('task') == "appearfromback":
                appear_from_back(pixels, color, wait_time)
        QUEUE.task_done()
        if item.get('replay') and QUEUE.empty():
            QUEUE.put(item)


def start_worker():
    thread = threading.Thread(target=worker)
    thread.start()
    return thread


WORKER = start_worker()


def stop_worker():
    QUEUE.put(None)
    WORKER.join()


pixels.clear()
pixels.show()
get_IP()
print(IP)
run(host=IP, port=8080, debug=True)
stop_worker()