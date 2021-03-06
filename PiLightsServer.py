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
RATIO = INTENSITY / 255
QUEUE = queue.Queue()

pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)


def get_IP():
    global IP
    while IP == "":
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc.connect(('8.8.8.8', 1))
            IP = soc.getsockname()[0]
        except Exception as e:
            print("Waiting for network connection")
            time.sleep(2.5)


# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(int(pos * 3 * RATIO), int((255 - pos * 3) * RATIO), 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(int((255 - pos * 3) * RATIO), 0, int(pos * 3 * RATIO))
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, int(pos * 3 * RATIO), int((255 - pos * 3) * RATIO))


# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256))
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def rainbow_cycle(pixels, wait=0.005):
    for j in range(256):  # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256))
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def rainbow_colors(pixels, wait=0.05):
    for j in range(256):  # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256))
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


def appear_from_back(pixels, color=[255, 0, 0], wait=0):
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(int(color[0] * RATIO), int(color[2] * RATIO), int(color[1] * RATIO)))
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(int(color[0] * RATIO), int(color[2] * RATIO), int(color[1] * RATIO)))
            pixels.show()
            time.sleep(wait)


def solid_colors(pixels, color=[255, 0, 0], wait=0):
    for i in range(pixels.count()):
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(int(color[0] * RATIO), int(color[2] * RATIO), int(color[1] * RATIO)))
        pixels.show()
        if wait > 0:
            time.sleep(wait)


def solid_array(pixels, arr, wait=0):
    for i in range(pixels.count()):
        pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(int(arr[i][0] * RATIO), int(arr[i][2] * RATIO), int(arr[i][1] * RATIO)))
        pixels.show()
    if wait > 0:
        time.sleep(wait)


def two_colors_alternate(pixels, first_color, second_color, wait=1):
    for i in range(pixels.count()):
        if i % 2 == 0:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(int(first_color[0] * RATIO), int(first_color[2] * RATIO), int(first_color[1] * RATIO)))
        else:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(int(second_color[0] * RATIO), int(second_color[2] * RATIO), int(second_color[1] * RATIO)))
    pixels.show()
    time.sleep(wait)
    for i in range(pixels.count()):
        if i % 2 == 0:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(int(second_color[0] * RATIO), int(second_color[2] * RATIO), int(second_color[1] * RATIO)))
        else:
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(int(first_color[0] * RATIO), int(first_color[2] * RATIO), int(first_color[1] * RATIO)))
    pixels.show()
    time.sleep(wait)


def set_ratio():
    global RATIO
    RATIO = INTENSITY / 255


@post('/rainbowSequence')
def rainbow_sequence_set():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('rainbowSequence', req_obj))
    return '{"success": True}'


@post('/rainbowCycle')
def rainbow_cycle_set():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('rainbowCycle', req_obj, True))
    return '{"success": True}'


@post('/rainbowColors')
def rainbow_colors_set():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('rainbowColors', req_obj, True))
    return '{"success": True}'


@post('/solid')
def solid_set():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('solid', req_obj))
    return '{"success": True}'


@post('/solidArray')
def solid_arr_set():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('solidArray', req_obj))
    return '{"success": True}'


@post('/intensity')
def intensity_set():
    global INTENSITY
    req_obj = json.loads(request.body.read())
    intensity_target = req_obj.get('target')
    if req_obj.get('force') and req_obj.get('force') == "True":
        if intensity_target > INTENSITY:
            INTENSITY = min(255, intensity_target)
        else:
            INTENSITY = max(0, intensity_target)
        set_ratio()
    else:
        QUEUE.put(build_task('intensity', req_obj))
    return "{intensity: " + str(INTENSITY) + "}"


@post('/appearFromBack')
def appear_from_back_set():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('appearFromBack', req_obj, True))
    return '{"success": True}'


@post('/twoColorAlternate')
def two_color_alternate():
    req_obj = json.loads(request.body.read())
    QUEUE.put(build_task('twoColorAlternate', req_obj, True))
    return '{"success": True}'


def build_task(task, body, replay=False):
    return {'task': task, 'body': body, 'replay': replay}


def worker():
    global INTENSITY
    while True:
        item = QUEUE.get()
        print(item)
        # This ends the worker thread and sets the last light to be red to indicate the server is not running properly1wqa1
        if item is None:
            pixels.clear()
            pixels.set_pixel(30, Adafruit_WS2801.RGB_to_color(255, 0, 0))
            pixels.show()
            print(QUEUE.empty())
            break
        else:
            # Parse out all possible information for each light function
            data = item.get('body')
            wait_time = data.get('wait', 0)
            intensity_target = data.get('target', 255)
            if item.get('task') == "appearFromBack":
                appear_from_back(pixels, data.get('color', [255, 0, 4]), wait_time)
            elif item.get('task') == "intensity":
                step_size = data.get('stepSize', 1)
                if intensity_target > INTENSITY:
                    brightness_increase(pixels, min(256, intensity_target - INTENSITY), wait_time, step_size)
                    INTENSITY = min(255, intensity_target)
                elif intensity_target < INTENSITY:
                    brightness_decrease(pixels, min(256, INTENSITY - intensity_target), wait_time, step_size)
                    INTENSITY = max(0, intensity_target)
                set_ratio()
            elif item.get('task') == "solidArray":
                solid_array(pixels, data.get('colors', [(255, 0, 4)] * PIXEL_COUNT), wait_time)
            elif item.get('task') == "solid":
                solid_colors(pixels, data.get('color', [255, 0, 4]), wait_time)
            elif item.get('task') == "rainbowColors":
                rainbow_colors(pixels, wait_time)
            elif item.get('task') == "rainbowCycle":
                rainbow_cycle(pixels, wait_time)
            elif item.get('task') == "rainbowSequence":
                rainbow_cycle_successive(pixels, wait_time)
            elif item.get('task') == 'twoColorAlternate':
                two_colors_alternate(pixels, data.get('first_color', [255, 0, 4]), data.get('second_color', [4, 0, 255]), wait_time)
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
