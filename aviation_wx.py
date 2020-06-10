#!/usr/bin/python
#Rev. 21/6/2016 - change to aviation_wx from val_stripper3.py
#REv. 14/2/2016 - change to reduce number of lines saved
#REv. 13/5/2020 - update to use sensor data from archive again

import numpy as np
import datetime
import time
import math

#Declare some constants
#  work_dir = '/home/pkotze/python/'
mag_var = 22.5 #magnetic variation

def moving_Avg(data_set, avg_len = 120):
 return [np.mean(data_set[x:x + avg_len]) for x in range(len(data_set) - avg_len)]

def metarTimeDT(dt):
 """convert datetime.datetime to metar time string"""
 return( '%02i' % dt.day + '%02i' % dt.hour + '%02i' % dt.minute + 'Z ')

def metarTemp(tempF):
 #[ str(x) if x>=0 else 'M'+ str(-x) for x in tempF ]
 if tempF >= 0:
  t = '%02i'%  (tempF)
 else:
  t = 'M' + '%02i'% (-tempF)
 return t
  
def toDewpoint(from_rh, at_Temp):
 """
 Calculates dewpoint from relative humidity
 """
 #local constants
 A = 6.116441
 m = 7.591386
 Tn = 240.7263
 P_ws = A * 10.0 ** ( m * at_Temp / ( at_Temp + Tn ))
 P_w = from_rh/100.0 * P_ws
 Tdew = Tn /( (m / math.log( P_w / A, 10)) - 1 )
 return (Tdew)

#hard coded VR041 airport elevation in m as default
def toQNH(from_QFE, airport_h=1044.55):
 """
 Calculates QNH from QFE using simple ICAO method
 """
 #local constants
 Rd = 287.04 #specific gas constant of dry air (287.04 J/kg/K Rindert 1978) 
 p0 = 1013.25 #hPa 
 T0 = 288.15 #K is +15 deg C
 g = 9.80665 #m/s^2 (standard gravity) 
 gamma = -0.0065 #K/m 
 H = airport_h
 H_ISA = 44330.77 - 11880.32 * from_QFE ** 0.190263
 QNH = 1013.25 * ( 1 - 0.0065 * (H_ISA - H) / 288.15) ** 5.25588 
 return (QNH)

def toKnots(from_ms):
 #Converts m/s to knots and returns as float 
 kts = float(from_ms) * 60 * 60 / 1852
 return kts

def phase_avg(dataset):
    """
    So to get wind direction (or phase) average 
    break angles into componentx x and y
    do summation of components
    and then calculate arctan2 (not arctan) to get resultant angle
    """
    v=np.array(dataset)
    x=np.cos(v/180.0*np.pi)
    y=np.sin(v/180.0*np.pi)
    avg=(np.arctan2(np.sum(y),np.sum(x))/np.pi*180.0+360)%360
    return(avg)
    
def phase_diff(angle1, angle2): 
    """
    For wind direction assuming 0 deg is North, increasing clockwise to 359 degrees
    """
    return(min((angle1-angle2)%360, (angle2-angle1)%360))
    
def maxDiff(arr, arr_size): 
    '''
    Cannot simply use max and min values in list as wind direction wraps at 360
    Search through list to find max difference between current element and all others
    If a new maximum difference found stored as max_diff
    Also the elements compared must form the new maximum and new minimum value
    '''
    max_diff = arr[1] - arr[0] #initialise to first difference
    for i in range( 0, arr_size ): 
        for j in range( i+1, arr_size ): #only need to test remaining items in list
            if phase_diff(arr[i],arr[j]) > max_diff:  #new max difference (angle) between elements in list
                max_diff = phase_diff(arr[i],arr[j])  #new max difference (angle) between elements in list
                max_dir=max(arr[i],arr[j])            #for this max_diff this is the max angle 
                min_dir=min(arr[i],arr[j])            #for this max_diff this is the min angle 
    return max_diff,min_dir,max_dir

def round_wind(wind_angle): 
    """
    Crude method to report windirection 0 as 360
    """
    wind_round_str = '%03i' % round(wind_angle, -1)
    #clunky but don't want to see 000 unless it is calm
    if wind_round_str == '000':
      wind_round_str = '360'
    return(wind_round_str)
    
def wind_METAR(wind_speed, wind_direc):
 """
 Input: wind_speed raw, wind_direction in kts 
 Description: no magnetic variation considered, METAR supposed to be true
 Output: metar compatible wind string
 We are assuming 10minutes worth of data stored at 1s intervals for windspeed and 5s intervals for winddirection
 """
 WIND_LIMIT = 3 #3kts after converted from m/s
 
 speed_mean = toKnots(np.mean(wind_speed[-121:-1])) #last 2 minutes of wind speed at interval of 1s
 speed_gust = toKnots(np.max(moving_Avg(wind_speed, 5)))# peak average over 5s for last *10 minutes* assuming data stored in 1s intervals
 gust_delta = speed_gust - speed_mean #already in knots
 
 direc_mean = phase_avg(wind_direc) #wind direction only in 5s intervals

 direc_var,direc_min,direc_max = maxDiff(wind_direc,len(wind_direc))
 #Debug: 
 print(speed_mean, speed_gust, gust_delta)
 print(direc_mean, direc_var,direc_min, direc_max)
 
 wind_var_str = ''
 #wind direction and maybe  VRB or CALM as 00000KT
 if speed_mean < 0.5:
  wind_direc_str = '000'
 elif speed_mean >= 0.5 and speed_mean <= WIND_LIMIT and direc_var >= 60:
  wind_direc_str = 'VRB'
 elif speed_mean > WIND_LIMIT and (direc_var > 60) and (direc_var < 180):
  wind_direc_str = round_wind(direc_mean)
  #need to remind myself why this works 
  if direc_max-direc_min <= 180:
      wind_var_str = ' ' + round_wind(direc_min) + 'V' + round_wind(direc_max)
  else:
      wind_var_str = ' ' + round_wind(direc_max) + 'V' + round_wind(direc_min)
 elif speed_mean > WIND_LIMIT and direc_var >= 180:
  wind_direc_str = 'VRB'
 else: # you get the value (wind stronger than  WIND_LIMIT but not varying)
  wind_direc_str = round_wind(direc_mean)

 #Now add Speed and (possibly gusts) then units of KT for knots
 if gust_delta >= 10: # if gust present you need to add the gust
  wind_speed_str = '%02i' % round(speed_mean) + 'G' + '%02i' % speed_gust + 'KT'
 else:
  wind_speed_str = '%02i' % round(speed_mean) + 'KT'

 return wind_direc_str + wind_speed_str + wind_var_str + ' '

def saveMetar(save_file, save_txt): 
    #constants
    total_lines=6*24
    #open file 
    f = open(save_file, 'r+')
    #get all lines
    lines=f.readlines()
    f.seek(0, 0) #seek to start to write new line at top of file
    f.write(save_txt)
    #Debug
    #print(len(lines))
    if len(lines) < total_lines:
        for line in lines:
            f.write(line)
    else:
        for i in range(0,total_lines-1):
            f.write(lines[i])
    f.close()

def ftpMetar(file_name, file_txt, ftp_host, ftp_user, ftp_pass): 
    import ftplib
    ftp_file=open(file_name,'rb')
    ftp_session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
    ftp_session.cwd('/public_html')
    ftp_session.storbinary('STOR ' + file_txt, ftp_file)
    ftp_session.quit()
    ftp_file.close()



