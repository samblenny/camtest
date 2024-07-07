# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# CamTest: A simple demo of Pi Pico + Adafruit PiCowbell Camera Breakout
#
# Related Docs and Code:
# - https://learn.adafruit.com/adafruit-picowbell-camera-breakout
# - https://docs.circuitpython.org/projects/ov5640/en/latest/
# - https://github.com/adafruit/Adafruit_CircuitPython_OV5640/blob/main/adafruit_ov5640/__init__.py
#
from board import (
    GP0, GP1, GP2, GP3, GP4, GP5, GP6, GP7, GP8, GP9, GP10,
    GP11, GP12, GP13, GP14, GP18, GP19, GP22,
)
from busio import I2C, SPI
from digitalio import DigitalInOut, Pull
from displayio import Bitmap
from gc import collect, mem_free
from time import sleep

import adafruit_bus_device
from adafruit_ov5640 import (
    OV5640, OV5640_SIZE_96X96, OV5640_SIZE_240X240, OV5640_COLOR_GRAYSCALE
)

def free(print_=True):
    collect()
    if print_:
        print("mem_free", mem_free())

def ttyPrint(pxBuf):
    # Print pixel buffer using Unicode Block Element characters
    blocks = [' ', '▀', '▄', '█']
    for y in range(pxBuf.height >> 1):
        y0 = y << 1
        y1 = y0 + 1
        s = []
        for x in range(pxBuf.width):
            s.append(blocks[
                ((pxBuf[x,y1]>> 7) << 1) | (pxBuf[x,y0] >> 7) ])
        print(''.join(s))

def main():
    gc = free
    gc()
    # Configure the camera
    spi = SPI(clock=GP18, MOSI=GP19)
    i2c = I2C(GP5, GP4)  # I2C(SCL, SDA)
    # shutter = DigitalInOut(GP22)
    # shutter.switch_to_input(Pull.UP)  # active low
    cam = OV5640(
        i2c,
        vsync=GP0,
        href=GP2,
        clock=GP3,
        shutdown=DigitalInOut(GP1),
        data_pins=(GP6, GP7, GP8, GP9, GP10, GP11, GP12, GP13),
        reset=DigitalInOut(GP14),
        mclk=None,
        size=OV5640_SIZE_240X240,
    )
    cam.flip_x = True
    cam.colorspace = OV5640_COLOR_GRAYSCALE
    # Make a buffer to hold captured pixel data
    gc()
    pxBuf = Bitmap(240, 240, 256)
    gc()
    # Capture and print a frame every 2 seconds
    while True:
        sleep(2)
        cam.capture(pxBuf)
        ttyPrint(pxBuf)
        gc()


main()
