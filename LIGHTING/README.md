# LIGHTING
This is a useful bundle of scripts to detect and allow for interfacing with the Raspberry Pi.

# LED Chipset Support

|         | RPI 3 | RPI Zero (W) |
|---------|-------|--------------|
| WS2182  | Yes   | Yes          |
| WS2182b | Yes   | Yes          |


# WS2182 

This script allows the user to control the WS2182 led pixel.

For wiring, check `/assets`

## How to Install Dependcies
```shell
sudo chmod +x ./setup.sh
./setup.sh
```

## How To Import
```python
from RPI-Useful-Python-master.LIGHTING.led_driver import WS2182

led = WS2182b(pixels=2)
```

### flash
Sends a short pulse to the LED's

```python
led.flash()
```

### off
Tells the LED's to display no light

```python
led.off()
```

### hold
Tells the LED's to stay lit.

an optional argument of `color` can be given to override the default color property temporarily.

```python
led.hold(led.colors["green"])
```

### startChase
This starts a [chase sequence](https://en.wikipedia.org/wiki/Chase_(lighting)) thread.

```python
led.startChase()
```

### stopChase
This stops the [chase sequence](https://en.wikipedia.org/wiki/Chase_(lighting)) thread.

```python
led.stopChase()
```

# Dependencies
- [Adafruit Circuit Python](https://github.com/adafruit/CircuitPython_Community_Bundle/releases)
- Adafruit NeoPixel `sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`
- Adafruit Blinka `sudo pip3 install adafruit-blinka`

