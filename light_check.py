#!/usr/bin/python
import datetime
import os
import time
import pywemo

debug = os.getenv('debug') is not None
state_file = '/state/state.txt'

def IsOn(wemo_switch):
    return (wemo_switch.get_state(True) != 0)

def Refresh(wemo_object):
    _ = wemo_object.get_state(True)
    return wemo_object

def DrawingPower(wemo_switch):
    return (Refresh(wemo_switch).current_power > 6000)

def EnsureOn(wemo_switch):
    if not IsOn(wemo_switch):
        wemo_switch.on()

def GetOldState():
    try:
        return open(state_file, 'r').read(1) != '0'
    except Exception as e:
        Log("Getting state failed: ", e)
        return False 

def WriteState(On):
    try:
        char = '0'
        if On:
            char = '1'
        f = open(state_file, 'w')
        f.write(char)
        f.close()
    except Exception as e:
        Log("Writting state failed: ", e)
        return 

def Log(*message):
    if debug:
        print(*message)


devices = { x.name : x for x in pywemo.discover_devices()}
heater = devices["Heater"]
lightDetector = devices["Light detector"]

Log(devices)

light_was_drawing_power = GetOldState()
twentyMins = datetime.timedelta(minutes=20)
#twentyMins = datetime.timedelta(seconds=20)

#loop for an hour
second_sleep =5
for x in range(0, 3600, second_sleep):
    EnsureOn(lightDetector)
    
    time.sleep(second_sleep)
    twentyMinsFuture = datetime.datetime.now() + twentyMins

    drawing_power = DrawingPower(lightDetector)
    heater_on = IsOn(heater)

    Log("light_was_drawing_power:", light_was_drawing_power, "drawing_power:", drawing_power, "heater_on:", heater_on)

    while (not light_was_drawing_power) and heater_on and (not drawing_power) and datetime.datetime.now() < twentyMinsFuture:
        time.sleep(second_sleep)
        drawing_power = DrawingPower(lightDetector)
        heater_on = IsOn(heater)
        Log("Inner - ", "light_was_drawing_power:", light_was_drawing_power, "drawing_power:", drawing_power, "heater_on:", heater_on)
    
    if drawing_power:
        if not heater_on:
            heater.on()
    else:
        if heater_on:
            heater.off()
    
    if light_was_drawing_power != drawing_power:
        light_was_drawing_power = drawing_power
        WriteState(drawing_power)
        Log("Writting state:", drawing_power)
  
  #state = IsOn(switch)
  #greater than 6 watts
  #power = light_outlet.current_power
  #has_power = (power > 6000)
  #print (light_outlet, state, power, has_power)

