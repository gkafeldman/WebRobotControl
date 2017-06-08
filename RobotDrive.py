#!/usr/bin/pythonRoot
# bring in the libraries
import RPi.GPIO as G     
from flup.server.fcgi import WSGIServer
import sys, urlparse

inpPinLeft = 18
inpPinRight = 17

# set up our GPIO pins
G.setmode(G.BCM)
G.setup(inpPinLeft, G.IN)
G.setup(inpPinRight, G.IN)

G.setup(24, G.IN)

path = '/home/pi/adafruit-motor-hat-python-library/Adafruit_MotorHAT'

if path not in sys.path:
    sys.path.append(path)

import Robot

LEFT_TRIM   = 0
RIGHT_TRIM  = 15

SPEED = 110

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# all of our code now lives within the app() function which is called for each http request
# we receive
def app(environ, start_response):
    # start our http response 
    start_response("200 OK", [("Content-Type", "text/plain")]) #parameters: "status string", "list of tuples representing response headers"
    # flup expects a string to be returned from this function
    # either as: return [""]
    # or as yield ("")

    # look for inputs on the URL
    i = urlparse.parse_qs(environ["QUERY_STRING"])

    # if there's a url variable named 'q'
    if "q" in i:
      if ((i["q"][0] == "w") and (G.input(inpPinLeft) == 1) and (G.input(inpPinRight) == 1)): 
        robot.forward(SPEED)
      elif i["q"][0] == "s":
        robot.backward(SPEED/2,0.75)
      elif i["q"][0] == "a":
        robot.left(SPEED/3,0.75)
      elif i["q"][0] == "d":
        robot.right(SPEED/3,0.75)
      elif i["q"][0] == ".":
        robot.stop()

    output = ""

    if (G.input(inpPinLeft) == 0):
      robot.stop()
      output = output + "l"
    else:
      output = output + "-"

    if (G.input(inpPinRight) == 0):
      robot.stop()
      output = output + "r"
    else:
      output = output + "-"

    yield(output)

      
#by default, Flup works out how to bind to the web server for us, so just call it
# with our app() function and let it get on with it
WSGIServer(app).run()
