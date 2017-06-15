#!/usr/bin/env python

from RPLCD.common import CursorMode
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import MFRC522
import time
import signal
import sys
import glob
import os

startKeglevel = 40.0
keglevel = 40.0

users = {
	'64,84,139,25': {
		'name': 'Josh',
		'tokens': 2
	},
	'80,77,34,25': {
		'name': 'Robert',
		'tokens': 2
	},
	'6,4,136,187': {
		'name': 'Ty',
		'tokens': 2
	},
	'149,6,90,190': {
		'name': 'Brittany',
		'tokens': 2
	}
}

continue_reading = True

relay_control_channel = 8
flow_sensor_channel = 5

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_control_channel, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(flow_sensor_channel, GPIO.IN)

delay = 3
run = True

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

lcd = CharLCD(pin_rs=40,pin_e=38,pins_data=[36,37,35,33],numbering_mode=GPIO.BOARD,cols=20,rows=4,dotsize=8,charmap='A02',auto_linebreaks=True)
lcd.cursor_mode = CursorMode.hide

lcd.write_string('Please Scan Card...')

def signal_handler(signal, frame):
	global continue_reading
	print "Cleaning up GPIO pins"
	continue_reading = False
	GPIO.cleanup()

signal.signal(signal.SIGINT, signal_handler)

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def flow_routine():
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

	keep_open = True

	while keep_open:
		currentTime = int(time.time() * 1000)
		if GPIO.input(flow_sensor_channel):
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

		if(pouring == True and pinState == lastPinState and (pintsPoured > 1.0 or (currentTime - lastPinChange) > 3000)):
			keep_open = False
			pouring = False
			if(pintsPoured > 0.1):
				global keglevel
				keglevel -= pintsPoured
				print 'Someone just poured ' + str(pintsPoured) + ' pints of beer'
				litersPoured = 0
				pintsPoured = 0

		lastPinChange = pinChange
		lastPinState = pinState

while continue_reading:
  temp_c, temp_f = read_temp()
  lcd.cursor_pos = (1, 0)
  lcd.write_string('Temp: '+ "{0:.2f}".format(temp_f) + ' F')
  lcd.cursor_pos = (2, 0)
  lcd.write_string("{0:.2f}".format(keglevel) + ' pints left')
  lcd.cursor_pos = (3, 0)
  lcd.write_string(int(round(keglevel / startKeglevel * 20)) * "=")

  # Scan for cards
  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

  # If a card is found
  if status == MIFAREReader.MI_OK:
    print "Card detected"

  # Get the UID of the card
  (status,uid) = MIFAREReader.MFRC522_Anticoll()

  # If we have the UID, continue
  if status == MIFAREReader.MI_OK:
    # Print UID
    uid_string = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
    user = users[uid_string]
    if user['tokens'] > 0:
      users[uid_string]['tokens'] -= 1
      lcd.clear()
      lcd.write_string('Welcome '+ user['name'] + '!')
      lcd.crlf()
      lcd.write_string('Tokens Left: ' + str(users[uid_string]['tokens']))
      lcd.crlf()
      lcd.write_string('Start pouring...')
      GPIO.output(relay_control_channel, GPIO.LOW)
      flow_routine()
      GPIO.output(relay_control_channel, GPIO.HIGH)
      lcd.clear()
      lcd.write_string('Enjoy! :)')
    else:
      lcd.clear()
      lcd.write_string('Sorry ' + user['name'])
      lcd.crlf()
      lcd.write_string('You have 0 tokens')

    time.sleep(5)
    lcd.clear()
    lcd.write_string('Please Scan Card...')
