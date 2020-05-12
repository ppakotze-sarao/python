#Revised September 2019 - remove plotting
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates

log_files=[['/home/pkotze/anaconda3/97intvl.csv','Initial power check']]


for log_file,description in log_files:   #print(log_file)
    df=pd.read_csv(log_file,header=1,parse_dates=['Time'])
    
timestamps=(df['Time'])

#line to neutral voltage
aveirms1=np.asarray( df['AveUrms1'] ).astype(float)
aveirms2=np.asarray( df['AveUrms2'] ).astype(float)
aveirms3=np.asarray( df['AveUrms3'] ).astype(float)

#average PF sum
avepfsum=np.asarray( df['AvePFsum'] ).astype(float)

#frequency 
minfreq=np.asarray( df['MinFreq'] ).astype(float)
avefreq=np.asarray( df['AveFreq'] ).astype(float)
maxfreq=np.asarray( df['MaxFreq'] ).astype(float)

#average  rms line currents?
aveirms1=np.asarray( df['AveIrms1'] ).astype(float)
aveirms2=np.asarray( df['AveIrms2'] ).astype(float)
aveirms3=np.asarray( df['AveIrms3'] ).astype(float)
aveirms4=np.asarray( df['AveIrms4'] ).astype(float)

#Average P Q S power
avepsum=np.asarray( df['AvePsum'] ).astype(float) #active?
aveqsum=np.asarray( df['AveQsum'] ).astype(float) #reactive?
avessum=np.asarray( df['AveSsum'] ).astype(float) #total?


#Plot average p q s power

fig,ax = plt.subplots(figsize=(20,15))

ax.set(title="Basic hioki parameters: =>  "+log_file, ylabel='AvePMaxSsum [W?]', 
xlabel='Time [s]')
ax.plot(timestamps,avepsum)
ax.plot(timestamps,aveqsum)
ax.plot(timestamps,avessum)


ymin=0
ymax=3000
ystep=100
#plt.yticks(range(ymin,ymax,ystep))
#plt.ylim(ymin,ymax)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) 
_=plt.xticks(rotation=65)
ax.legend(['P','Q','S'])
ax.grid()


#Plot ave I rms

fig,ax = plt.subplots(figsize=(20,20))

ax.set(title="Basic hioki parameters: =>  "+log_file, ylabel='Ave I RMS', 
xlabel='Time [s]')
ax.plot(timestamps,aveirms1)
ax.plot(timestamps,aveirms2)
ax.plot(timestamps,aveirms3)
ax.plot(timestamps,aveirms4)

ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) 
_=plt.xticks(rotation=90)
ax.legend(['1','2','3','4'])
ax.grid()


#Plot power factor

fig,ax = plt.subplots(figsize=(20,20))

ax.set(title="Basic hioki parameters: =>  "+log_file, ylabel='Ave I RMS', 
xlabel='Time [s]')
ax.plot(timestamps,avepfsum)

ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) 

ax.legend(['1','2','3','4'])
ax.grid()



#Plot min max average frequency

fig,ax = plt.subplots(figsize=(20,20))

ax.set(title="Basic hioki parameters: =>  "+log_file, ylabel='AvePMaxSsum [W?]', 
xlabel='Time [s]')
ax.plot(timestamps,minfreq)
ax.plot(timestamps,avefreq)
ax.plot(timestamps,maxfreq)


ymin=0
ymax=3000
ystep=100
#plt.yticks(range(ymin,ymax,ystep))
#plt.ylim(ymin,ymax)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) 
ax.legend(['Min','aVe','Max'])
ax.grid()

