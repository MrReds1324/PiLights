import http.client
import json
import time
import asyncio

c = http.client.HTTPConnection('localhost', 8080)
# c.request('POST', '/rainbowS', '{"delay": 1}')
# doc = c.getresponse().read()
# print(doc)
#
# c.request('POST', '/rainbowC', '{"state": 1}')
# doc = c.getresponse().read()
# print(doc)
#
# c.request('POST', '/rainbowColors', '{"state": 1}')
# doc = c.getresponse().read()
# print(doc)

c.request('POST', '/intensity', '{"target": 100}')
doc = c.getresponse().read()
print(doc)
time.sleep(1)
c.request('POST', '/intensity', '{"target": 255}')
doc = c.getresponse().read()
print(doc)
time.sleep(1)
c.request('POST', '/intensity', '{"target": 500, "wait": 0.1, "stepSize": 1}')
doc = c.getresponse().read()
print(doc)