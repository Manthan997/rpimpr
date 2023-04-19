#Libraries
import RPi.GPIO as GPIO
import time
# sudo pip install Adafruit-CharLCD
import Adafruit_CharLCD as LCD
# https://learn.adafruit.com/character-lcd-with-raspberry-pi-or-beaglebone-black/usage
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)      
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_button = 16  #change this integer
 # LCD pin configuration:
lcd_rs        = 27  
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4
 

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_button, GPIO.IN)
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
                           lcd_columns, lcd_rows, lcd_backlight)

SonicSpeed = 34300.0 #cm/s

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * SonicSpeed) / 2
 
    return distance

def getTime(pin):
    while GPIO.input(pin) == 0:
        butStrartTime = time.time()
    while GPIO.input(pin) == 1:
        butStopTime = time.time()
    butTime = butStopTime - butStrartTime
    return butTime

def syncMode():
    lcd.clear()
    lcd.message("sync mode")
    time.sleep(1)
    # for 3cm distance
    lcd.clear()
    lcd.message("adjust 3cm then\n press button")
    while GPIO.input(GPIO_button) == 0:
        #do nothing
        print("waiting for response...")
        #exits loop when button is 1
    lcd.clear()
    time3a = getTime(GPIO_ECHO) # call time noting function[trigers and returns time in float]
    lcd.message("again...")
    while GPIO.input(GPIO_button) == 0:
        #do nothing
        print("waiting for response...")
        #exits loop when button is 1
    lcd.clear()
    time3avg = (time3a + getTime(GPIO_ECHO)) / 2.0# call time noting function[trigers and returns time in float]
    # update sonic
    SonicSpeedAvg = 6 / time3avg
    SonicSpeed = (SonicSpeed + SonicSpeedAvg) /2

    # for 6cm distance
    lcd.clear()
    lcd.message("adjust 6cm then\n press button")
    while GPIO.input(GPIO_button) == 0:
        #do nothing
        print("waiting for response...")
        #exits loop when button is 1
    lcd.clear()
    time3a = getTime(GPIO_ECHO) # call time noting function[trigers and returns time in float]
    lcd.message("again...")
    while GPIO.input(GPIO_button) == 0:
        #do nothing
        print("waiting for response...")
        #exits loop when button is 1
    lcd.clear()
    time3avg = (time3a + getTime(GPIO_ECHO)) / 2.0# call time noting function[trigers and returns time in float]
    # update sonic
    SonicSpeedAvg = 12 / time3avg
    SonicSpeed = (SonicSpeed + SonicSpeedAvg) /2


    # for 10cm distance
    lcd.clear()
    lcd.message("adjust 10cm then\n press button")
    while GPIO.input(GPIO_button) == 0:
        #do nothing
        print("waiting for response...")
        #exits loop when button is 1
    lcd.clear()
    time3a = getTime(GPIO_ECHO) # call time noting function[trigers and returns time in float]
    lcd.message("again...")
    while GPIO.input(GPIO_button) == 0:
        #do nothing
        print("waiting for response...")
        #exits loop when button is 1
    lcd.clear()
    time3avg = (time3a + getTime(GPIO_ECHO)) / 2.0# call time noting function[trigers and returns time in float]
    # update sonic
    SonicSpeedAvg = 20 / time3avg
    SonicSpeed = (SonicSpeed + SonicSpeedAvg) /2
    lcd.clear()
    lcd.message("sonic speed:\n%f",SonicSpeed)
    time.sleep(1)
'''
3 sync distances 
each reading 3 times
and give setting time + button push to start each dist
take time readings -> average them for each dist -> sonic value 
sonicspeed = dist / time
avg the 3 sonic values
store in global var 
use that to tell distances
'''


if __name__ == '__main__':
    try:
        while True:
    # button status not used cause it implies 
    # when previous code is done it will check button as a condition and move morword accordingly
            while GPIO.input(GPIO_button) == 0:
                butStrartTime = time.time() 
                # butStopTime will increase untill button in not pressed(low)
                # once pressed, it will shift to next line
            while GPIO.input(GPIO_button) == 1:
                # butStopTime = time.time()
                # butStartTime will increase untill button in pressed(high)
                # once released it will exit this loop and execute further codE
                butTime = time.time() - butStrartTime
                if butTime > 2:
                    syncMode()
                else:
                    continue
                # IF butTime overflows, jump to syncMode

            # butTime = butStopTime - butStrartTime
            if butTime > 0 and butTime <= 2: # this line is redundant 
                # trigger dist reporting 
                dist = distance()  #call the sensing function
                lcd.clear()
                lcd.message("Distance:\n%.2f cm" % dist) #check availablity of formatted string
            '''elif butTime > 2: 
                syncMode()'''       #cause this block is redundant
                # sync mode function
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
