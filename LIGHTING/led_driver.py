import time
import neopixel
import board
import threading
import sys, getopt

class _chase_sequence():
    def __init__(self,leds,speed=0.2):
        self.speed = speed
        self.pixels = leds
        self.stop_chase_event = threading.Event()
        self.stop_chase_event.clear()
        self.stop_event = False
        self.chase_thread = threading.Thread(target=self.__chase)
        self.chase_thread.start()
        
    def start_chase(self):
        self.stop_chase_event.set()
    def stop_chase(self):
        self.stop_chase_event.clear()
    def __chase(self):
        currentLed = 1
        lastLed = 0
        while self.stop_event == False:
            self.stop_chase_event.wait()
            if currentLed >= len(self.pixels):
                currentLed = 0
                lastLed = currentLed-1
            self.pixels[currentLed] = ((200,200,200))
            self.pixels[lastLed] = ((0,0,0))
            lastLed = currentLed
            currentLed += 1
            
            time.sleep(self.speed)
    def stop(self, callback = None):
        self.stop_event = True
        self.chase_thread.join()
        print('LED Chase thread Stopped')
        
        
class WS2182x(_chase_sequence):
    def __init__(self,pixels):
        self.GPIO_PIN = board.D12

        self.COLOR = None
        self.NUM_OF_PIXELS = pixels
        
        self.pixels = neopixel.NeoPixel(self.GPIO_PIN, self.NUM_OF_PIXELS, brightness=0.1, auto_write=True, pixel_order=neopixel.GRB)
        self.colors = {
        "red" : tuple((255,0,0)),
        "green" : tuple((0,255,0)),
        "blue" : tuple((0,0,255)),
        "yellow" : tuple((255,255,0)),
        "orange" : tuple((255,102,0)),
        "purple" : tuple((102,0,255)),
        "white" : tuple((255,255,255))
        }
        
        _chase_sequence.__init__(self,self.pixels)
        
    def flash(self,color = None):
        if color == None:
            color = self.COLOR
            self.off()
        self.pixels.fill(color)
        time.sleep(0.25)
        self.off()
        
    def off(self):
        self.stop_chase()
        self.pixels.fill((0,0,0))
        
        self.isOff = True
    def hold(self,color=None):
        if color == None:
            color = self.COLOR
        self.pixels.fill(color)
