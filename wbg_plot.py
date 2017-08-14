#!/usr/bin/python
#Rev. 15/04/2016
#added support for UHF rx, need to specify l or u before serial number.

#Open files and plot with mask
#usage eg: python wbg_plot.py receptor rx_serial

from numpy import *
import matplotlib.pyplot as plt
import sys

receptor=sys.argv[1] # e.g. 'm015'
serial=sys.argv[2] # e.g. 'l.4001'

f_scale=1e6
#mask
if serial[0] == 'l':
 ulim=-124.3+10*log10(3e6)
 mask_f = [0,200e6/f_scale,420e6/f_scale,2150e6/f_scale,2900e6/f_scale,3600e6/f_scale]
 mask_a = [ulim-21, ulim-21, ulim, ulim, ulim-21, ulim-21]
elif serial[0] == 'u':
 ulim=-124.3+10*log10(3e6)
 mask_f = [0,100e6/f_scale,300e6/f_scale,1200e6/f_scale,NaN,1620e6/f_scale,3600e6/f_scale]
 mask_a = [ulim-13, ulim-13, ulim, ulim,NaN, ulim-13, ulim-13]

#Spectrum analyser data
Inst = genfromtxt('Instrument.csv', delimiter=',')
Hpol = genfromtxt('Hpol.csv', delimiter=',')
Vpol = genfromtxt('Vpol.csv', delimiter=',')
Hpol_noise = genfromtxt('Hpol_noise.csv', delimiter=',')
Vpol_noise = genfromtxt('Vpol_noise.csv', delimiter=',')

#EMSS receiver noise diode models
Hpol_rx_ndmodel = genfromtxt('rx.'+serial+'.h.csv', delimiter=',')
Vpol_rx_ndmodel = genfromtxt('rx.'+serial+'.v.csv', delimiter=',')

#Hpolf = [10**(item/10) for item in Hpol[60:]]
#fr for frequency response
Hpol_fr = Hpol[60:]
Vpol_fr = Vpol[60:]
Hpol_noise_fr = Hpol_noise[60:]
Vpol_noise_fr = Vpol_noise[60:]
#Get noise diode models frequency range
fh = Hpol_rx_ndmodel[:,0]  
fv = Vpol_rx_ndmodel[:,0]  

#Hpol
Yh = interp( fh,Hpol_noise_fr[:,0],10**(Hpol_noise_fr[:,1]/10) ) / interp( fh,Hpol_fr[:,0], 10**(Hpol_fr[:,1]/10) )
Yv = interp( fv,Vpol_noise_fr[:,0],10**(Vpol_noise_fr[:,1]/10) ) / interp( fv,Vpol_fr[:,0], 10**(Vpol_fr[:,1]/10) )
Tsysh = Hpol_rx_ndmodel[:,1]/(Yh-1)
Tsysv = Vpol_rx_ndmodel[:,1]/(Yv-1)

#Plot Wide band gain (and save a png)
plt.close('all')
plt.figure(figsize=(20,10))
plt.ylabel('Amplitude [dBm]')
plt.xlabel('Frequency [MHz]')
plt.title(receptor)
plt.ion()
plt.plot(Inst[60:,0]/f_scale, Inst[60:,1], label='Instrument', color='blue')
plt.plot(Hpol[60:,0]/f_scale, Hpol[60:,1], label='Hpol', color='red')
plt.plot(Vpol[60:,0]/f_scale, Vpol[60:,1], label='Vpol', color='green')
#plt.plot(Hpol_noise_fr[:,0]/f_scale, Hpol_noise_fr[:,1], label='Hpol noise', linestyle='--', color='red')
#plt.plot(Vpol_noise_fr[:,0]/f_scale, Vpol_noise_fr[:,1], label='Vpol noise', linestyle='--', color='green')
plt.plot(mask_f, mask_a, label='Mask', color='black')
plt.grid()
plt.legend()
plt.ylim([-110,-50])
plt.xlim([0,3.6e9/f_scale])

#Plot Tsys (and save a png)
plt.savefig(receptor+'_wbg')

plt.figure(figsize=(20,10))
plt.ylabel('Tsys [K]')
plt.xlabel('Frequency [MHz]')
plt.title(receptor)
plt.plot(fh/f_scale, Tsysh, label='Tsys h', color='red')
plt.plot(fv/f_scale, Tsysv, label='Tsys v', color='green')
plt.legend()
plt.grid()
plt.ylim([10,50])
#plt.xlim([0,3.6e9])
plt.savefig(receptor+'_T_sys')

