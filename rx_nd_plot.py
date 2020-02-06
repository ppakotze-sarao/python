#!/usr/bin/python
#Rev. 0 6/2/2020 
# From earlier work, plot noise diode values only 

from numpy import *
import matplotlib.pyplot as plt
import sys

rx_serial=sys.argv[1]


f_scale=1e6
#mask
if rx_serial[0] == 'l':
 ulim=-124.3+10*log10(3e6)
 mask_f = [0,200e6/f_scale,420e6/f_scale,2150e6/f_scale,2900e6/f_scale,3600e6/f_scale]
 mask_a = [ulim-21, ulim-21, ulim, ulim, ulim-21, ulim-21]
 dlim=-134.6+10*log10(3e6)
 dmask_f = [900e6/f_scale,1670e6/f_scale]
 dmask_a = [dlim,dlim]
 #frequency calc
 #2048 points, 856MHz sample to 2*856MHz = 1712MHz
 f_chn=[856+856*(x/2048.0) for x in range(0,2048)]
 xmin=855
 xmax=1722
 xstep=100
 u_xticks=[855,900,1000,1100,1200,1300,1400,1500,1600,1670,1712]
 u_blow=900
 u_bhi=1670
 #EMSS receiver noise diode models
 Hpol_rx_ndmodel = genfromtxt('/home/pkotze/checkouts/katconfig/user/noise-diode-models/mkat/rx.'+rx_serial+'.h.csv', delimiter=',')
 Vpol_rx_ndmodel = genfromtxt('/home/pkotze/checkouts/katconfig/user/noise-diode-models/mkat/rx.'+rx_serial+'.v.csv', delimiter=',')
 #436

elif rx_serial[0] == 'u':
 ulim=-122.7+10*log10(3e6)
 mask_f = [0,100e6/f_scale,300e6/f_scale,1200e6/f_scale,NaN,1610e6/f_scale,3600e6/f_scale]
 mask_a = [ulim-13, ulim-13, ulim, ulim,NaN, ulim-13, ulim-13]
 dlim=-137.3+10*log10(3e6)
 dmask_f = [580e6/f_scale,1015e6/f_scale]
 dmask_a = [dlim,dlim]
 #frequency calc
 #2048 points, 544MHz sample to 2*544MHz = 1088MHz
 f_chn=[544+544*(x/2048.0) for x in range(0,2048)]
 xmin=544
 xmax=1088
 xstep=100
 u_xticks=[544,580, 600,700,800,900,1000,1015,1088]
 u_blow=580
 u_bhi=1015
 #EMSS receiver noise diode models
 Hpol_rx_ndmodel = genfromtxt('/home/pkotze/checkouts/katconfig/user/noise-diode-models/mkat/rx.'+rx_serial+'.h.csv', delimiter=',',skip_header=3)
 Vpol_rx_ndmodel = genfromtxt('/home/pkotze/checkouts/katconfig/user/noise-diode-models/mkat/rx.'+rx_serial+'.v.csv', delimiter=',',skip_header=3)


plt.figure(figsize=(20,10))
plt.plot(Hpol_rx_ndmodel[:,0]/f_scale,Hpol_rx_ndmodel[:,1])
plt.plot(Vpol_rx_ndmodel[:,0]/f_scale,Vpol_rx_ndmodel[:,1])
plt.axhline(y=35, color='b', linestyle='-')
plt.axhline(y=14, color='b', linestyle='-')
ymin=10
ymax=40
ystep=5
plt.yticks(range(ymin,ymax,ystep))
plt.xticks(u_xticks)
plt.xlim(xmin,xmax)
plt.title(rx_serial)
plt.ylabel('T_nd model [K]')
plt.xlabel('Frequency [MHz]')
plt.legend(['Hpol','Vpol'])
plt.grid()
plt.savefig('RX'+ rx_serial + '.png')

plt.show()

