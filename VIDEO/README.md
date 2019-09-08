# RPI-Useful-Python

This script allows the user to display text to an LCD screen attached to the relevant pins.

For wiring, check `/assets`

# LCD Text Driver
## Installing Dependencies 
```shell
sudo chmod +x ./setup.sh
./setup.sh
```
## How To Import
```python
from RPI-Useful-Python-master.VIDEO.lcd_driver import ILI934x

lcd = ILI934x(dc=13,rst=24,back_light=5,spi_port=0,spi_device=1,fonts_dir=None,resolution = (320,240))
```
- dc = *BCM PIN VALUE*
- rst = *BCM PIN VALUE*
- back_light = *BCM PIN VALUE*
- spi_port = *BCM PIN VALUE*
- spi_device = *BCM PIN VALUE*
- fonts_dir = *FONT TO USE*
- resolution = (*X AXIS PIXELS*, *Y AXIS PIXELS*)

### show
Shows the text provided on the LCD screen. The text is scaled to the pixel dimensions given `resolution (xxx,yyy)`

```python
lcd.show("Hello World")
```

### clear
Clears everything form the LCD screen. `resolution (xxx,yyy)`

```python
lcd.clear()
```

### off
If a backlight pin is given, this will switch off the display.

```python
lcd.off()
```

### on
If a backlight pin is given, this will switch on the display.

```python
lcd.on()
```

# Dependencies
- Adafruit ILI9341 - https://github.com/adafruit/Adafruit_Python_ILI9341


# Devices Supported


|         | RPI 3 | RPI Zero (W) |
|---------|-------|--------------|
| ILI934x | Yes   | Yes          |