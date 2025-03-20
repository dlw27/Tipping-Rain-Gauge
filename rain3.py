# A tipping bucket rain gauge operates on a simple mechanism: a seesaw-like bucket system tips when a specific amount of rain is collected, triggering a switch. Each tip represents a fixed volume of rainfall. 
# Wiring Diagram 
# Connect the rain gauge to a microcontroller, like a Raspberry Pi, as follows: 

# Connect one wire from the rain gauge to a GPIO pin on the Raspberry Pi. 
# Connect the other wire from the rain gauge to a ground (GND) pin on the Raspberry Pi. 

# Python Code 
import RPi.GPIO as GPIO
import time
import datetime
import MySQLdb as mdb

# Set up GPIO pin numbering
GPIO.setmode(GPIO.BCM)


# Define the GPIO pin to which the rain gauge is connected
rain_pin = 17  # Example pin, change as needed

# Calibration value (amount of rain per bucket tip in mm)
BucketSize = 0.01193

# Set the GPIO pin as input with a pull-up resistor
GPIO.setup(rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variable to store the rain count
TipCount = 0



# Callback function to be executed when the rain gauge tips
def rain_callback(channel):
    global TipCount
    global BucketSize
    now = datetime.datetime.now()
    TipCount += 1
    print("Rain tip detected! Total tips:", TipCount)
    print(now.strftime("%Y"))
    YYYY_ = (now.strftime("%Y"))
    print(now.strftime("%m"))
    MM_ = (now.strftime("%m"))
    print(now.strftime("%d"))
    DD_ = (now.strftime("%d"))
    print(now.strftime("%H"))
    HR_ = int((now.strftime("%H")))
    print(now.strftime("%M"))
    MN_ = (now.strftime("%M"))
    print(now.strftime("%S"))
    SEC_ = (now.strftime("%S"))
    HR3_ = int(3+int(HR_/3)*3)
    HR6_ = int(6+int(HR_/6)*6)
    HR12_ = int(12+int(HR_/12)*12)
    print(YYYY_, MM_, DD_, HR_, MN_, SEC_, HR3_, HR6_, HR12_)
    
    print("trying database")
    con = mdb.connect('localhost', 'root', 'password', 'SkyWeather');

    cur = con.cursor()
    print ("before query")

    query = 'INSERT INTO Rain(YYYY,MM,DD,HR,MN,SEC,HR3,HR6,HR12) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (YYYY_, MM_, DD_, HR_, MN_, SEC_, HR3_, HR6_, HR12_)
        
    print("query=%s" % query)

    cur.execute(query)
    
    con.commit()

# Event detection for falling edge (when the switch closes)
GPIO.add_event_detect(rain_pin, GPIO.FALLING, callback=rain_callback, bouncetime=200)

try:
    print("Rain gauge monitoring... Press Ctrl+C to exit")
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Tip count: ", TipCount)
    RainTotal = TipCount*BucketSize
    print("Rain Total: %.4f in" % RainTotal)

finally:
    GPIO.cleanup()

    

