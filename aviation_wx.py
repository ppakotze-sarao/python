#!/usr/bin/python
#Rev. 21/6/2016 - change to aviation_wx from val_stripper3.py
#REv. 14/2/2016 - change to reduce number of lines saved

import numpy as np
import datetime
import time
import math

#Declare some constants
#  work_dir = '/home/pkotze/python/'
mag_var = 22.5 #magnetic variation

def moving_Avg(data_set, avg_len = 120):
 #xx=range(avg_len,len(nrm_wind_speed) )
 return [np.mean(data_set[x:x + avg_len]) for x in range(len(data_set) - avg_len)]
 #for x in range(len(nrm_wind_speed) - avg_len):
 # avg_wind_speed.append(numpy.mean(nrm_wind_speed[x:x + avg_len]) )

def index_frtime(all_lines, time_instant, time_history = 120):
 """
 Input: list of strings 
 Finds index of specified time_instant (unix) for a specified time_history upto that time_instant
 Output: list of index, list of time values
 """
 all_times = [ float(line.strip().split(',')[1]) for line in all_lines] 
 time_start = time_instant - time_history
 time_end = time_instant
 wanted_index = [all_times.index(sample_time) for sample_time in all_times if sample_time> time_start and sample_time <= time_end ]
 #wanted_times = all_times[wanted_index[0]:wanted_index[-1]]
 return wanted_index

def metarTime(unixTime):
 ts=time.gmtime(unixTime)
# hour = ts.tm_hour+2   
 return( '%02i' % ts.tm_mday + '%02i' % ts.tm_hour + '%02i' % ts.tm_min + 'Z ')
 
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

#def toKnots(from_ms):
# #Converts m/s to knots and returns as float 
# kts = [float(x) * 60 * 60 / 1852 for x in from_ms]
# return kts

def toKnots(from_ms):
 #Converts m/s to knots and returns as float 
 kts = float(from_ms) * 60 * 60 / 1852
 return kts

def wind_METAR(wind_speed, wind_direc):
 """
 Input: wind_speed raw, wind_direction in kts 
 Description: no magnetic variation considered, METAR supposed to be true
 Output: metar compatible wind string
 """
 WIND_LIMIT = 3 #kts or 6km/h
# wind_u = wind_speed * math.cos(math.radians(wind_direc))
# wind_v = j*wind_speed * math.sin(math.radians(wind_direc))
# wind_j = wind_speed * math.cos(math.radians(wind_direc)) + j*wind_speed * math.sin(math.radians(wind_direc))
# wind_u_2min = np.mean(wind_u[-120:-1])
# wind_v_2min = np.mean(wind_v[-120:-1])
# wind_c_2min = wind_u_2min + wind_v_2min
 # speed_2min = wind_speed
 # direc_2min = (wind_direc[-120:-1])
 speed_mean = np.mean(wind_speed)
 speed_gust = np.max(moving_Avg(wind_speed, 3) )
 gust_delta = speed_gust - speed_mean
 direc_mean = np.mean(wind_direc)
 direc_min = np.min(wind_direc)
 direc_max = np.max(wind_direc)
 direc_var = np.max(wind_direc) - np.max(wind_direc)
 #print speed_mean, speed_gust, direc_mean, direc_var
 wind_var_str = ''
 #wind direction and maybe  VRB
 if speed_mean < 0.5:
  wind_direc_str = '000'
 elif speed_mean <= WIND_LIMIT and direc_var >= 60:
  wind_direc_str = 'VRB'
 elif speed_mean > WIND_LIMIT and (direc_var > 60) and (direc_var < 180):
  wind_direc_str = '%03i' % round(direc_mean, -1)
  wind_var_str = ' ' + '%03i' % round(direc_min, -1) + 'V' + '%03i' % round(direc_max, -1)
 elif speed_mean > WIND_LIMIT and direc_var >= 180:
  wind_direc_str = 'VRB'
 else: # you get the value (should never see a 6??)
  wind_direc_str = '%03i' % round(direc_mean, -1)
 #Speed and kts
 if gust_delta >= 10: # if gust present you need to add the gust
  wind_speed_str = '%02i' % round(speed_mean) + 'G' + '%02i' % speed_gust + 'KT '
 else:
  wind_speed_str = '%02i' % round(speed_mean) + 'KT '
 return wind_direc_str + wind_speed_str + wind_var_str

def read_CSV(csv_file):
 """
 Reads in the CSV file retrieved from the katstore elsewhere returns all lines
 """ 
 "get 12 min period of data"
 "all data nominal"
 file=open(csv_file, 'r')
 lines=file.readlines()
 #for line in lines:
 # print line.strip().split(',')[-1]
 file.close()
 return lines
 
def nearest_Hour():
 """
 Input: None
 Output: Unix time of the nearest hour for which to process data
 """
 tn=time.gmtime() #time now
 dt=datetime.datetime(tn.tm_year, tn.tm_mon, tn.tm_mday, tn.tm_hour) #everything up to hour
 # return time.mktime(dt.timetuple()) #and back to unix time
 return dt

def saveMetar(save_file, save_txt): 
 f = open(save_file, 'r+')
 #use to read entire file and add new line to the top
 #old_content = f.read()
 for i in range(0,38):  #now only save last 40 lines
	old_content = f.next()
	old_content = old_content + f.next()
 f.seek(0, 0)
 f.write(save_txt + old_content)
 f.close()

def ftpMetar(file_name, file_txt): 
 import ftplib
 ftp_host = 'www.qsl.net'
 ftp_user = 'zs1pk'
 ftp_pass = 'hxh4fp24'
 ftp_file=open(file_name,'rb')
 ftp_session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
 ftp_session.storbinary('STOR ' + file_txt, ftp_file)
 ftp_session.quit()
 ftp_file.close()

def nearest_Hour():
 """
 Input: None
 Output: Unix time of the nearest hour for which to process data
 """
 tn=time.gmtime() #time now
 dt=datetime.datetime(tn.tm_year, tn.tm_mon, tn.tm_mday, tn.tm_hour) #everything up to hour
 # return time.mktime(dt.timetuple()) #and back to unix time
 return dt

