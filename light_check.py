#!/usr/bin/python
import datetime
from ouimeaux.environment import Environment
env = Environment()
env.start()
env.discover(seconds=10)

state_file = '/data/state.txt'

def IsOn(wemo_switch):
  return (wemo_switch.get_state(True) != 0)

def DrawingPower(wemo_switch):
  return (wemo_switch.current_power > 6000)

def EnsureOn(wemo_switch):
  if not IsOn(wemo_switch):
    wemo_switch.on()

def GetOldState():
  try:
    return open(state_file, 'r').read(1) != '0'
  except:
    return False 

def WriteState(On):
  try:
    char = '0'
    if On:
      char = '1'
    f = open(state_file, 'w')
    f.write(char)
    f.close()
  except:
    return 

def Log(*message):
  if debug:
    for m in message:
      print(m)

debug = True
light_was_drawing_power = GetOldState()
twentyMins = datetime.timedelta(minutes=20)
#twentyMins = datetime.timedelta(seconds=20)

#loop for an hour
second_sleep =5
for x in range(0, 3600, second_sleep):
  EnsureOn(env.get_switch('Light detector'))
  
  env.wait(second_sleep)
  light_outlet = env.get_switch('Light detector')
  heater = env.get_switch('Heater')
  twentyMinsFuture = datetime.datetime.now() + twentyMins

  drawing_power = DrawingPower(light_outlet)
  heater_on = IsOn(heater)

  while (not light_was_drawing_power) and heater_on and (not drawing_power) and datetime.datetime.now() < twentyMinsFuture:
    env.wait(second_sleep)
    drawing_power = DrawingPower(light_outlet)
    heater_on = IsOn(heater)
  
  if drawing_power:
    if not heater_on:
      heater.on()
  else:
    if heater_on:
      heater.off()
  
  if light_was_drawing_power != drawing_power:
     light_was_drawing_power = drawing_power
     WriteState(drawing_power)
  
  #state = IsOn(switch)
  #greater than 6 watts
  #power = light_outlet.current_power
  #has_power = (power > 6000)
  #print (light_outlet, state, power, has_power)

