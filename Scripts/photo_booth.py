#!/usr/bin/python

import RPi.GPIO as GPIO, time, os, subprocess

# GPIO setup
GPIO.setmode(GPIO.BCM)
SWITCH = 24
GPIO.setup(SWITCH, GPIO.IN)
RESET = 25
GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 22
POSE_LED1 = 17
POSE_LED2 = 18
POSE_LED3 = 27
BUTTON_LED = 23
GPIO.setup(POSE_LED1, GPIO.OUT)
GPIO.setup(POSE_LED2, GPIO.OUT)
GPIO.setup(POSE_LED3, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)
print("Setup done. Waiting for button press...")
while True:
  print("Button Status:")
  GPIO.output(POSE_LED2,True)
  print(GPIO.input(SWITCH))
  
  # Is button pressed?
  if (GPIO.input(SWITCH)):
    snap = 0
    GPIO.output(POSE_LED2, False)
    
    # Make 3 Photos
    while snap < 3:
      print("pose!")
      GPIO.output(BUTTON_LED, False) # BUTTON LED OFF!
      GPIO.output(POSE_LED1, True) # Pose LED ON!
      time.sleep(1.5)
      for i in range(5): # Some fancy blinking
        GPIO.output(POSE_LED2, False)
        time.sleep(0.4)
        GPIO.output(POSE_LED2, True)
        time.sleep(0.4)
      for i in range(20):# faster fancy blinking
        GPIO.output(POSE_LED3, False)
        time.sleep(0.1)
        GPIO.output(POSE_LED3, True)
        time.sleep(0.1)
      print("SNAP")
      
      # Make a Photo
      gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobooth_images/photobooth%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True)
      print(gpout)
      
      # Turn LEDs off for next round
      GPIO.output(POSE_LED2,False)
      GPIO.output(POSE_LED3,False)	
      GPIO.output(POSE_LED1, False)

      if "ERROR" not in gpout: 
        snap += 1 # How many photos?
      time.sleep(0.5)
    print("please wait while your photos print...")
    
    # build image and send to printer
    subprocess.call("sudo /home/pi/Scripts/assemble_and_print", shell=True)
    # TODO: implement a reboot button
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time
    # time.sleep(60)
    print("ready for next round")
    GPIO.output(POSE_LED2,True)
  time.sleep(0.05)
