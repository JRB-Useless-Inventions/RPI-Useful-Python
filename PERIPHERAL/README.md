# PERIPHERALS
This is a useful bundle of scripts to detect and allow for interfacing with the Raspberry Pi.
## Sensors
- Ultra Sonic
- Code Scanner
- Battery Monitor

## Hardware
- Button

# Ultra Sonic

This script allows the user to detect when an object is detected to be in front of the HCSR04 sensor.

For wiring, check `/assets/UltraSonic`

## Performance Notes
Ultrasonic is proven to only work sufficiently when an object is presnetd flat. When the object is angled, the distance is measured innaccuratley. This module is only to be used if the threshold set is a large set (between 2cm to 30 cm) and the distance is not of critical importance.

## How It Works
When an object is held in front of the sensor, if the object is between the `min_distance` and `max_distance` threshold, the `listener` event flag is raised. This loop runs for as long as the thread is alive, constantly checking for an object. 

## How To Import
```python
from RPI-Useful-Python-master.PERIPHERALS.sensors import UltraSonic

def objectDetected():
	print("Object Detected")
    
sonic = UltraSonic(trig=25,echo=23,listener=objectDetected,min_distance=2,max_distance=30)
```
- trig = *BCM PIN VALUE FOR TRIGGER PIN*
- echo = *BCM PIN VALUE FOR ECHO PIN*
- listener = *FUNCTION TO BE CALLED*
- min_distance = *DISTANCE IN CM*
- max_distance = *DISTANCE IN CM*

### start
Starts the thread

```python
sonic.start()
```

### pause
Pauses the thread

```python
sonic.pause()
```

### resume
If paused, this resumes the thread activity

```python
sonic.resume()
```

# Code Scanner

This script allows the user to detect when a QR or Barcode is presented to a camera.

For wiring, check `/assets/CodeScanner`

## Installing Dependencies 
```shell
sudo chmod +x ./setup.sh
./setup.sh
```

## Performance Notes
Capturing video as well as analyzing video frames is very costly on CPU capacity. This script checks a fraction of the frames, which in turn slows down response time but allows for the CPU to not be throttled keeping power consumption to a minimum.

## How It Works
Once started the camera checks for a code. To assist with Code detection (especially in traditional 2D-Barcodes) the image is rotated per frame.

This module also reports back if the image is too dark. This is useful for switching on / off InfraRed LED's to illuminate a code.

This loop runs for as long until a code is detected. Once detected the thread is paused until told to resume.

## How To Import
```python
from RPI-Useful-Python-master.PERIPHERALS.sensors import CodeScanner

def codeFound(codes):
	print("Codes(s) Detected")
def tooDark():
	print("Too Dark")
scanner = CodeScanner(codeFoundEvent = codeFound,tooDarkEvent = tooDark)
```

### start
Starts the thread.
```python
scanner.start()
```

### pause
Pauses the thread.
```python
scanner.pause()
```

### resume
If paused, this resumes the thread activity.

```python
scanner.resume()
```


# Battery Monitor

This script allows the user to detect the life of a battery's charge.

For wiring, check `/assets/BatteryMonitor`

## Installing Dependencies 
```shell
sudo chmod +x ./setup.sh
./setup.sh
```

## How To Import
```python
from RPI-Useful-Python-master.PERIPHERALS.sensors import BatteryMonitor

battery = BatteryMonitor(min_volts=3.1,max_volts=4)
```

### getCharge
This function is blocking. It returns the given charge of a power source depedant on the `min_volts` and `max_volts`.
```python
batteryLevel = battery.getCharge()
print(batteryLife)
```






