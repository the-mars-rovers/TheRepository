#!/usr/bin/env python2

import subprocess
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Less blinding & less burn-in
disp.set_contrast(10)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Load default font.
font = ImageFont.truetype('ttf/FiraCode-Regular.ttf', 14)

top = -2
left = 0
while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    ips = subprocess.check_output(["hostname", "-I"])
    offset = 0
    for ip in ips.split(' '):
        if len(ip) > 16:
            continue  # IPv6
        draw.text((left, top + offset), ip, font=font, fill=255)
        offset += 16

    disp.image(image)
    disp.display()
    time.sleep(10)

    left += 1
    top += 1

    if left >= 4:
        left = 0
        top = -2
