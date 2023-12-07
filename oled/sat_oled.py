#!/usr/bin/env python3
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import netifaces as ni
import socket
import shmgpsd
import time


def get_shm():
  return shmgpsd.SHM()

def get_visible_sats(shm_gpsd):
  return shm_gpsd.satellites_visible

def get_used_sats(shm_gpsd):
  return shm_gpsd.satellites_used

def get_fix(shm_gpsd):
  return shm_gpsd.fix.mode

def get_satellites(shm_gpsd):
  sat_dict = {}
  for sat_i in range(0, shmgpsd.MAXCHANNELS):
    if shm_gpsd.skyview[sat_i].PRN != 0:
      sat_dict.update({shm_gpsd.skyview[sat_i].PRN : { 'snr':  shm_gpsd.skyview[sat_i].ss }})
  return sat_dict


def main():
  # Change these
  # to the right size for your display!
  WIDTH = 128
  HEIGHT = 64     # Change to 64 if needed
  
  # Use for I2C.
  i2c = board.I2C()
  oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
  
  # Clear display.
  oled.fill(0)
  oled.show()

  # Load default font.
  font = ImageFont.load_default()
  font2 = ImageFont.truetype(font="Quicksand-Regular.ttf", size=14)
  
  while True:
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (oled.width, oled.height))
  
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    
    # Clear screen
    oled.fill(0)
    oled.show()

    # Get GPS info
    shm_gpsd  = get_shm()
    sats      = get_visible_sats(shm_gpsd)
    sats_used = get_used_sats(shm_gpsd)
    fix       = get_fix(shm_gpsd)
    
    # Draw Some Text
    draw.text((30,0), "GPS Monitor", font=font2, fill=255)
    draw.text((0,15), socket.gethostname(), font=font, fill=255)
    draw.text((0,25), ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'], font=font, fill=256)
    print(f"Fix: {fix}")
    draw.text((0,35), f"Fix: {fix}", font=font, fill=255)
    print(f"Sats:: {sats}")
    draw.text((0,45), f"Sats visible: {sats}", font=font, fill=255)
    print(f"Sats used: {sats_used}")
    draw.text((0,55), f"Sats used: {sats_used}", font=font, fill=255)
    
    small = Image.open("sat.bmp")
    draw.bitmap((0,0), small, fill=255)
    
    # Display image
    oled.image(image)
    oled.show()
    time.sleep(5)

if __name__ == "__main__":
  main()
