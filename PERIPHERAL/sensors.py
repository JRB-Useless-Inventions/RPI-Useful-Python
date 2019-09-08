#GENERAL
import RPi.GPIO as GPIO
from events import Events
import threading
import time
import numpy as np

#CODE SCANNER
from imutils.video import VideoStream
from pyzbar import pyzbar
import imageio
import datetime
import imutils
import cv2

#BATTERY MONITOR
import board
import busio
import adafruit_ina219

class UltraSonic(threading.Thread):
    def __init__(self,trig,echo,listener,min_distance,max_distance):
        threading.Thread.__init__(self)
        self.can_run = threading.Event()
        self.can_run.set()
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.timer = threading.Event()
        self.GPIO_TRIG_PIN = trig
        self.GPIO_ECHO_PIN = echo
        self.trigger = Events()
        self.trigger.on_change += listener
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        self.isPaused = False
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_PIN, GPIO.IN)
        self.stop_event = False
        self.start()
    def pause(self):
        self.can_run.clear()

    def resume(self):
        self.can_run.set()

    def run(self):
        while self.stop_event == False:
            self.can_run.wait()
            GPIO.output(self.GPIO_TRIG_PIN, False)
            time.sleep(0.7)                      

            GPIO.output(self.GPIO_TRIG_PIN, True)                  #Set TRIG as HIGH
            time.sleep(0.00001)                     #Delay of 0.00001 seconds
            GPIO.output(self.GPIO_TRIG_PIN, False)                 #Set TRIG as LOW

            while GPIO.input(self.GPIO_ECHO_PIN)==0:               #Check whether the ECHO is LOW
                pulse_start = time.time()              #Saves the last known time of LOW pulse

            while GPIO.input(self.GPIO_ECHO_PIN)==1:              #Check whether the ECHO is HIGH
                pulse_end = time.time()                #Saves the last known time of HIGH pulse 

            pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

            distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
            
            if distance > self.min_distance and distance < self.max_distance:      #Check whether the distance is within range
                self.trigger.on_change() #Print distance with 0.5 cm calibration
        
    def stop(self, callback = None):
        self.stop_event = True
        self.join()
        print('Ultrasonic Stopped')

#CODE SCANNER
class Scanner(threading.Thread):
	def __init__(self,codeFoundEvent = None,tooDarkEvent = None):
		self.up_time_max = 15
		threading.Thread.__init__(self)
		# Pause thread
		self.can_run = threading.Event()
		self.can_run.set()
		#code found Trigger
		self.trigger = Events()
		self.trigger.on_change += codeFoundEvent
		#Too Dark Trigger
		self.tooDarkEvent = Events()
		self.tooDarkEvent.on_change += tooDarkEvent
		# initialize the video stream and allow the camera sensor to warm up
		#print "[INFO] starting video stream..."
		self.up_time = 0
		self.down_time = 0
		self.stop_event = False
		self.start()
	def img_est(self,img,thresh):
		is_light = np.mean(img) > thresh
		return True if is_light else False
		
	def run(self):
		rotation = 0
		self.vs = VideoStream(usePiCamera=True).start()
		time.sleep(2.0)
		self.active = True
		self.start_time = time.time()
		# loop over the frames from the video stream
		
		while self.stop_event == False:
			self.can_run.wait() # Run algo
			
			self.up_time = time.time() - self.start_time
			
			if self.up_time > self.up_time_max:
				time.sleep(0.1)
				self.trigger.on_change(None)
				self.pause()
				continue

			if rotation >= 360:
				rotation = 0
			
			# grab the frame from the threaded video stream and resize it to
			# have a maximum width of 400 pixels
			frame = self.vs.read()
			frame = imutils.resize(frame, width=400)
			rotation += 45
			frame = imutils.rotate(frame,rotation)
			
			if self.img_est(frame,40) is False:
				self.tooDarkEvent.on_change(True)
			else:
				self.tooDarkEvent.on_change(False)
			#print(self.img_est(frame,40))
				
		 
			# find the barcodes in the frame and decode each of the barcodes
			barcodes = pyzbar.decode(frame)
			# loop over the detected barcodes
			if len(barcodes) > 0:
				print('Code Found')
				self.trigger.on_change(barcodes)
				self.pause()
				continue
				
			for barcode in barcodes:
				# extract the bounding box location of the barcode and draw
				# the bounding box surrounding the barcode on the image
		 
				# the barcode data is a bytes object so if we want to draw it
				# on our output image we need to convert it to a string first
				barcodeData = barcode.data.decode("utf-8")
				barcodeType = barcode.type
		 
				# draw the barcode data and barcode type on the image
				text = "{} ({})".format(barcodeData, barcodeType)
			key = cv2.waitKey(1) & 0xFF

			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break
			time.sleep(0.2)
		return
	def pause(self):
		self.active = False
		self.can_run.clear()
	
	def resume(self):
		self.active = True
		self.start_time = time.time()
		self.can_run.set()
        
	def stop(self):
		print("[INFO] cleaning up...")
		cv2.destroyAllWindows()
		self.vs.stop()
		self.stop_event = True
		self.join()
		print('Scanner Stopped')

#BATTERY MONITOR
class RingBuffer():
	def __init__(self, sizeOfList):
		self.size = sizeOfList
		self.data = [ 50 for i in range(sizeOfList)]
	def append(self, x):
		self.data.pop(0)
		self.data.append(x)
	def get(self):
		return self.data
        
class BatteryMonitor(RingBuffer):  
	def __init__(self,min_volts=3, max_volts=4):
		RingBuffer.__init__(self,10)
		self.MIN_VOLTS = min_volts
		self.MAX_VOLTS = max_volts
		max_volts_diff = self.max_volts - self.min_volts
		i2c = busio.I2C(board.SCL, board.SDA)
                ina219 = adafruit_ina219.INA219(i2c)
	def getCharge(self):
		counter = 0
		is_active = True
		while is_active is True:
			diff = ina219.bus_voltage - 3.0
			
			battery_percentage = diff / max_volts_diff * 100
			q = self.append(battery_percentage)

			lst = self.get()
			avg = (sum(lst) / len(lst))
			counter += 1
			if counter > self.size:
				is_active = False
			time.sleep(0.25)
		if avg < 0 or avg > 100:
			avg = 100
		return avg



