import http.client
import json
import time
import asyncio

c = http.client.HTTPConnection('localhost', 8080)

#
# c.request('POST', '/rainbowC', '{"state": 1}')
# doc = c.getresponse().read()
# print(doc)
#
# c.request('POST', '/rainbowColors', '{"state": 1}')
# doc = c.getresponse().read()
# print(doc)

c.request('POST', '/intensity', '{"target": 20, "force": "False"}')
doc = c.getresponse().read()
print(doc)

c.request('POST', '/rainbowS', '{"wait": 0.1}')
doc = c.getresponse().read()
print(doc)

# time.sleep(1)
# c.request('POST', '/intensity', '{"target": 255}')
# doc = c.getresponse().read()
# print(doc)
# time.sleep(1)
# c.request('POST', '/intensity', '{"target": 50, "wait": 0.01, "stepSize": 1}')
# doc = c.getresponse().read()
# print(doc)