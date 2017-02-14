#!/usr/bin/python
#Rev. 21/6/2016 - stripped down version -> no working retrieve sensor data

import getpass
import sys
import telnetlib
import time
import math
import aviation_wx

work_dir = '/home/pkotze/tmp/'

#Functions
class stationData():
 def __init__(self):
  self.wind_direction = 'None'
  self.wind_speed = 'None'
  self.air_temperature = 'None'
  self.air_humidity = 'None'
  self.air_pressure = 'None'
  self.raw_list = []

 def stripVal(self, var ): 
  """
  For a string selects only the sensor value and returns as a float
  """
  return float(var.split('\n')[0].split(' ')[-1])

 def stripDate(self, var ): 
  """
  For a DATE string selects only the sensor value and returns as a float
  """
  return float(var.split('\n')[0].split(' ')[1])
 
 def processVal(self): 
  return(
   'VR041 ' + aviation_wx.metarTime(self.raw_list[5]) + 'AUTO '+ 
   #'%03i' % round( self.raw_list[0] + aviation_wx.mag_var, -1) + '%02i' % round(aviation_wx.toKnots(self.raw_list[1])) + 'KT ' 
   aviation_wx.wind_METAR( [self.raw_list[1],self.raw_list[1],self.raw_list[1],self.raw_list[1]], [self.raw_list[0],self.raw_list[0],self.raw_list[0],self.raw_list[0]]) + 
   aviation_wx.metarTemp( self.raw_list[2]) + '/' + 
   aviation_wx.metarTemp( aviation_wx.toDewpoint( self.raw_list[3], self.raw_list[2] ) ) + ' ' +
   'Q' + '%04i' % round( aviation_wx.toQNH( self.raw_list[4], 1044.55 ) ) + '=' +
   ' *** Image -> http://www.qsl.net/zs1pk/oneshotimage.jpg *** Refresh browser!\n')



 def buildVal(self): 
  self.raw_list = (
  [self.stripVal(self.wind_direction),
  self.stripVal(self.wind_speed), 
  self.stripVal(self.air_temperature), 
  self.stripVal(self.air_humidity), 
  self.stripVal(self.air_pressure),
  self.stripDate(self.wind_speed) ] #get time '%02i'%ts[2]+'%02i'%ts[3]+'%02i'%ts[4]+'Z'
  )

 def getRawdata(self): 
  """
  gets Raw Data 
  """  
  HOST = "192.168.193.4"  #asc enviro
  PORT = '1251'
  wait = 0.1

  tn = telnetlib.Telnet(HOST, PORT)
  time.sleep(wait)
  login_text=tn.read_very_eager()
 
  tn.write("?sensor-value wind.direction\n")
  time.sleep(wait)
  self.wind_direction=tn.read_very_eager()
  
  tn.write("?sensor-value wind.speed\n")
  time.sleep(wait)
  self.wind_speed=tn.read_very_eager()

  tn.write("?sensor-value air.temperature\n")
  time.sleep(wait)
  self.air_temperature=tn.read_very_eager()

  tn.write("?sensor-value air.relative-humidity\n")
  time.sleep(wait)
  self.air_humidity=tn.read_very_eager()

  tn.write("?sensor-value air.pressure\n")
  time.sleep(wait)
  self.air_pressure=tn.read_very_eager()

  tn.close()

if __name__ == '__main__':
 #self test code
 faska=stationData()
 faska.getRawdata()
 faska.buildVal()
 print faska.processVal()
 metar_txt = faska.processVal()
 aviation_wx.saveMetar(work_dir + 'vr041_metar.txt', faska.processVal())
 aviation_wx.ftpMetar(work_dir + 'vr041_metar.txt', 'vr041.txt')
