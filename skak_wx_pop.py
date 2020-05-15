#!/usr/bin/python3.6
#Rev. 21/6/2016 - stripped down version -> no working retrieve sensor data
#Rev. 14/5/2020 - major rewrite to retrieve data from katstore
import datetime
import numpy as np
from cam_sensors import sensor_data_pvsn
from pathlib import Path
import aviation_wx

work_dir = Path("./output/")

#Functions
class stationData():
    def __init__(self):
        self.wind_direction = 'None'
        self.wind_speed = 'None'
        self.air_temperature = 'None'
        self.air_humidity = 'None'
        self.air_pressure = 'None'
        self.timestamp = 'None'

    def getSensors(self):
        """
        gets Sensor data from CAM Archive, using cam_sensors function
        hard coded to get latest 10 minutes, should be 600s per sensor
        """      
        dtnow_utc = datetime.datetime.utcnow()
        #for now it appears katstore needs SAST
        #if you send UTC you will get data 2hrs earlier than expected! 14/5/2020
        dtnow     = datetime.datetime.now()
        dtnow_m2  = dtnow - datetime.timedelta(minutes=2)
        dtnow_m10 = dtnow - datetime.timedelta(minutes=10)
            
        self.timestamp = dtnow_utc
        self.air_temperature = sensor_data_pvsn('anc_weather_temperature', dtnow_m2, dtnow)[2]
        self.air_humidity = sensor_data_pvsn('anc_weather_humidity', dtnow_m2, dtnow)[2]
        self.air_pressure =sensor_data_pvsn('anc_weather_pressure', dtnow_m2, dtnow)[2]
        self.wind_speed = sensor_data_pvsn('anc_wind_wind_speed', dtnow_m10, dtnow)[2]
        self.wind_direction = sensor_data_pvsn('anc_wind_wind_direction', dtnow_m2, dtnow)[2]
        
    def processSensors(self): 
        return(
            'VR041 ' 
            + aviation_wx.metarTimeDT(self.timestamp) 
            + 'AUTO '
            + aviation_wx.wind_METAR( self.wind_speed, self.wind_direction) 
            + aviation_wx.metarTemp( np.mean(self.air_temperature) )
            + '/' 
            + aviation_wx.metarTemp( aviation_wx.toDewpoint( np.mean(self.air_humidity), np.mean(self.air_temperature)) ) 
            + ' ' 
            + 'Q' 
            + '%04i' % round( aviation_wx.toQNH( np.mean(self.air_pressure), 1044.55 ) ) 
            + '=' 
            + '\n')

if __name__ == '__main__':
    #self test code
    faska=stationData()
    faska.getSensors()
    metar_txt = faska.processSensors()
    #Debug:
    #print(metar_txt)
    aviation_wx.saveMetar(Path(__file__).parents[0] / work_dir / 'vr041_metar.txt', metar_txt)
    aviation_wx.ftpMetar(Path(__file__).parents[0] / work_dir / 'vr041_metar.txt', 'vr041.txt','files.000webhost.com','ppakotze','wagwoord')
    #print('Upload done')
