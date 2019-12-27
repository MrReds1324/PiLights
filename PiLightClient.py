import http.client
import json
import time
import asyncio

c = http.client.HTTPConnection('localhost', 8080)

c.request('POST', '/intensity', '{"target": 20, "force": "False"}')
doc = c.getresponse().read()
print(doc)

c.request('POST', '/rainbowS', '{"wait": 0.01}')
doc = c.getresponse().read()
print(doc)

c.request('POST', '/rainbowC', '{"wait": 0.01}')
doc = c.getresponse().read()
print(doc)

c.request('POST', '/rainbowColors', '{"wait": 0.01}')
doc = c.getresponse().read()
print(doc)

c.request('POST', '/solid', '{"wait": 0.01, "red": 255, "green": 50, "blue": 78}')
doc = c.getresponse().read()
print(doc)


c.request('POST', '/solidArr', '{"wait": 0.01}')
doc = c.getresponse().read()
print(doc)


# c.request('POST', '/appearfromback', '{"color": [4, 0, 255]}')
# doc = c.getresponse().read()
# print(doc)
#
# c.request('POST', '/intensity', '{"target": 0, "force": "False"}')
# doc = c.getresponse().read()
# print(doc)