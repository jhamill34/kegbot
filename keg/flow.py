import RPi.GPIO as GPIO
import signal
import time
import sys

continue_running = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

def signal_handler(signal, frame):
	global continue_reading
	print "Cleaning up GPIO pins"
	continue_reading = False
	GPIO.cleanup()	
	sys.exit(1)
	
signal.signal(signal.SIGINT, signal_handler)

lastPinState = False
pouring = False
pinState = 0 
lastPinChange = int(time.time() * 1000)
pourStart = 0
pinChange = lastPinChange
pinDelta = 0
hertz = 0
flow = 0
litersPoured = 0
pintsPoured = 0

while continue_running:
	currentTime = int(time.time() * 1000)
	if GPIO.input(7):
		pinState = True
	else:
		pinState = False

	if(pinState != lastPinState and pinState == True):
		if(pouring == False):
			pourStart = currentTime
		pouring = True
		pinChange = currentTime
		pinDelta = pinChange - lastPinChange
		if(pinDelta > 0 and pinDelta < 1000):
			hertz = 1000.0000 / pinDelta
			flow = hertz / (60 * 7.5)
			litersPoured += flow * (pinDelta / 1000.0000)
			pintsPoured = litersPoured * 2.11338

	if(pouring == True and pinState == lastPinState and pintsPoured > 1.0):
		print 'Closing valve'
		pouring = False
		if(pintsPoured > 0.1):
			pourTime = int((currentTime - pourStart)/1000) - 3
			print 'Someone just poured ' + str(pintsPoured) + ' pints of beer'
			litersPoured = 0
			pintsPoured = 0

	lastPinChange = pinChange
	lastPinState = pinState
