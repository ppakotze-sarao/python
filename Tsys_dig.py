#!/usr/bin/python
#Rev. based on wbg_plot which used a spectrum analyzer to capture cold sky and coldsky + noise diode data
#now use digitiser to capture both
#Rev. 2 11/11/2019 updates to read HK CSV filenames
#                  capital M for receptor and no leading zeros
#                  reading digitiser serials instead of receivers serials as in the case of spectrum analyzer measurement

from numpy import *
import matplotlib.pyplot as plt
import sys

csv_cold=sys.argv[1]
csv_hot=sys.argv[2]
rx_serial=sys.argv[3]

receptor=csv_cold.split('_')[0]
dig_serial=csv_cold.split('_')[1]
csv_coldt=csv_cold.split('_')[-1]
csv_hott=csv_hot.split('_')[-1]

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
 #436
 
#Spectrum analyser data
# Inst = genfromtxt('Instrument.csv', delimiter=',')
Hpol = genfromtxt(receptor+'_'+dig_serial+'_H_Pol_sw_spec_dump_'+csv_coldt, delimiter=',')
Vpol = genfromtxt(receptor+'_'+dig_serial+'_V_Pol_sw_spec_dump_'+csv_coldt, delimiter=',')
Hpol_noise = genfromtxt(receptor+'_'+dig_serial+'_H_Pol_sw_spec_dump_'+csv_hott, delimiter=',')
Vpol_noise = genfromtxt(receptor+'_'+dig_serial+'_V_Pol_sw_spec_dump_'+csv_hott, delimiter=',')
#2048


#Moon receiver noise diode models
#Hpol_rx_ndmoon = genfromtxt('/home/pkotze/python/rx.'+serial+'.h.csv', delimiter=',')
#Vpol_rx_ndmoon = genfromtxt('/home/pkotze/python/rx.'+serial+'.v.csv', delimiter=',')

ymin=-70
ymax=-50
ystep=5

#plt.ion()
plt.figure(figsize=(20,10))
plt.subplot(311)
plt.plot(f_chn, Hpol,'r')
plt.plot(f_chn, Hpol_noise,'r.')
plt.yticks(range(ymin,ymax,ystep))
#plt.xticks(range(xmin,xmax,xstep))
plt.xticks(u_xticks)
plt.ylim(ymin,ymax)
plt.xlim(xmin,xmax)
plt.axvline(x=u_blow, color='b', linestyle='-')
plt.axvline(x=u_bhi, color='b', linestyle='-')
plt.title('Hpol'+rx_serial)
plt.ylabel('Amplitude [dB]')
#plt.xlabel('Frequency [MHz]')
plt.legend(['Hpol','Hpol_noise'])
plt.grid()

plt.subplot(312)
plt.plot(f_chn, Vpol,'g')
plt.plot(f_chn, Vpol_noise,'g.')
plt.yticks(range(ymin,ymax,ystep))
#plt.xticks(range(xmin,xmax,xstep))
plt.xticks(u_xticks)
plt.ylim(ymin,ymax)
plt.xlim(xmin,xmax)
plt.axvline(x=u_blow, color='b', linestyle='-')
plt.axvline(x=u_bhi, color='b', linestyle='-')
plt.title('Vpol'+rx_serial)
plt.ylabel('Amplitude [dB]')
#plt.xlabel('Frequency [MHz]')
plt.legend(['Vpol','Vpol_noise'])
plt.grid()

plt.subplot(313)
f_scale=1e6
plt.plot(Hpol_rx_ndmodel[:,0]/f_scale,Hpol_rx_ndmodel[:,1])
plt.plot(Vpol_rx_ndmodel[:,0]/f_scale,Vpol_rx_ndmodel[:,1])
#plt.plot(Hpol_rx_ndmoon[:,0]/f_scale,Hpol_rx_ndmoon[:,1])
#plt.plot(Vpol_rx_ndmoon[:,0]/f_scale,Vpol_rx_ndmoon[:,1])
plt.axhline(y=35, color='b', linestyle='-')
plt.axhline(y=14, color='b', linestyle='-')
ymin=10
ymax=40
ystep=5
plt.yticks(range(ymin,ymax,ystep))
#plt.xticks(range(xmin,xmax,xstep))
plt.xticks(u_xticks)
plt.xlim(xmin,xmax)
plt.title(rx_serial)
plt.ylabel('T_nd model [K]')
plt.xlabel('Frequency [MHz]')
plt.legend(['Hpol','Vpol'])
plt.grid()
plt.savefig('RAW '+receptor +'_RX'+ rx_serial + 'DIG' +dig_serial+'.png')

#Hpolf = [10**(item/10) for item in Hpol[60:]]
#fr for frequency response
Hpol_fr = asarray(f_chn)*1e6
Vpol_fr = Hpol_fr
Hpol_noise_fr = Hpol_fr
Vpol_noise_fr = Hpol_fr
#Get noise diode models frequency range
fh = Hpol_rx_ndmodel[:,0]  
fv = Vpol_rx_ndmodel[:,0]  

#calculate Y factor per pol, why interp?
# Yh = interp(fh,Hpol_noise_fr,10**(Hpol_noise_fr/10)) / interp(fh,Hpol_fr, 10**(Hpol_fr/10))
# Yv = interp(fv,Vpol_noise_fr,10**(Vpol_noise_fr/10)) / interp(fv,Vpol_fr, 10**(Vpol_fr/10))
Yh=10**((Hpol_noise-Hpol)/10)
Yv=10**((Vpol_noise-Vpol)/10)

Tsysh = interp(Hpol_fr,fh,Hpol_rx_ndmodel[:,1])/(Yh-1)
Tsysv = interp(Vpol_fr,fv,Vpol_rx_ndmodel[:,1])/(Yv-1)

#Plot Tsys (and save a png)
plt.figure(figsize=(20,10))
plt.ylabel('Tsys [K]')
plt.xlabel('Frequency [MHz]')
plt.title('Receptor: '+receptor +' * Receiver: '+ rx_serial + ' * Digitiser: ' +dig_serial)
#plt.xticks(range(xmin,xmax,xstep))
plt.xticks(u_xticks)
plt.xlim(xmin,xmax)
plt.plot(Hpol_fr/f_scale, Tsysh, label='Tsys h', color='red')
plt.plot(Vpol_fr/f_scale, Tsysv, label='Tsys v', color='green')
plt.axvline(x=u_blow, color='b', linestyle='-')
plt.axvline(x=u_bhi, color='b', linestyle='-')
plt.legend()
plt.grid()
ymin=10
ymax=40
ystep=5
plt.yticks(range(ymin,ymax,ystep))
plt.ylim([ymin,ymax])


plt.savefig('Tsys_'+receptor +'_RX'+ rx_serial + 'DIG' +dig_serial+'.png')

plt.show()

