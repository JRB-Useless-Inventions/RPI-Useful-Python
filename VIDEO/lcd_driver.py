from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time
import RPi.GPIO as GPIO
import sys, getopt

class ILI934x():
    def __init__(self,dc=13,rst=24,back_light=5,spi_port=0,spi_device=1,fonts_dir=None,resolution = (320,240)):
        self.screen_resolution =resolution
        self.DC = dc
        self.RST = rst
        self.SPI_PORT = spi_port
        self.SPI_DEVICE = spi_device
        self.BACK_LIGHT = back_light
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BACK_LIGHT, GPIO.OUT)
        
        self.disp = TFT.ILI9341(self.DC, rst=self.RST, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=64000000))
        self.disp.begin()
        

        # Clear the display to a red background.
        # Can pass any tuple of red, green, blue values (from 0 to 255 each).
        self.font_size = 35
        if fonts_dir == None:
                self.font = ImageFont.load_default()
        else:        
                self.font = ImageFont.truetype(fonts_dir + "basic.ttf", self.font_size)
        self.draw = self.disp.draw()
        
    def show(self,text = None):
        self.clear()
        
        if text is None:
            self.clear()
            return
        self.on()
        self.draw_rotated_text(self.disp.buffer,text, (0,0), 90)
        self.disp.display()
    def clear(self):
        self.disp.clear((0,0,0))
        self.disp.display()
    def off(self):
        GPIO.output(self.BACK_LIGHT,1)
    def on(self):
        GPIO.output(self.BACK_LIGHT,0)
        
    def draw_rotated_text(self,image,text, position, angle, fill=(255,255,255)):
        # Get rendered font width and height.
        font = self.font
        draw = ImageDraw.Draw(image)
        width, height = draw.textsize(text, font=font)
        # Create a new image with transparent background to store the text.
        textimage = Image.new('RGBA', (width, height), (0,0,0,0))
        # Render the text.
        textdraw = ImageDraw.Draw(textimage)
        textdraw.text((0,0), text, font=font, fill=fill)
        # Rotate the text image.
        rotated = textimage.rotate(angle, expand=1)
        if width > self.screen_resolution[0]:
            rotated = rotated.resize((height,self.screen_resolution[0]))
            x = 0
            y_c = self.screen_resolution[1] / 2
            y = y_c - height/2
        else:
            x_c = self.screen_resolution[0] / 2
            x = x_c - width/2
            y_c = self.screen_resolution[1] / 2
            y = y_c - height/2
        
        # Paste the text into the image, using it as a mask for transparency.
        image.paste(rotated, (int(y),int(x)), rotated)
