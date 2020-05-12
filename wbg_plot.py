Skip to content
Why GitHub? 
Team
Enterprise
Explore 
Marketplace
Pricing 
Search

Sign in
Sign up
ppakotze
/
python
100
 Code
 Issues 0
 Pull requests 0 Actions
 Projects 0
 Security 0
 Insights
Join GitHub today
GitHub is home to over 50 million developers working together to host and review code, manage projects, and build software together.

python/wbg_plot.py /
@adriaanph adriaanph Changed the code into a function so that it can be imported & re-used…
2528b9a on 13 Sep 2018
@ppakotze@adriaanph
112 lines (99 sloc)  4.57 KB
 
#!/usr/bin/python
#Rev. 15/04/2016
#added support for UHF rx, need to specify l or u before serial number.
#Rev. 14/12/2017
#added UHF minimum signal level (also for L-band)
#Open files and plot with mask
#usage eg: python wbg_plot.py receptor rx_serial

from numpy import *
import matplotlib.pyplot as plt
import sys


def analyze(receptor, serial, root="./"):
    """
        @param receptor: string identifying receptor number e.g. "m013" for figures
        @param serial: string serial number of receiver e.g. "l.4021" to load calibration tables
        @param root: folder where the dataset, consisting of standard named csv files, can be found, must end with "/"
        @return: ((fh,fv), (Hoff,Voff), (Hon,Von), (Tsysh,Tsysv)) in [Hz], [dB], [dB], [K]
    """
    f_scale=1e6
    #mask
    if serial[0] == 'l':
     ulim=-124.3+10*log10(3e6)
     mask_f = [0,200e6/f_scale,420e6/f_scale,2150e6/f_scale,2900e6/f_scale,3600e6/f_scale]
     mask_a = [ulim-21, ulim-21, ulim, ulim, ulim-21, ulim-21]
     dlim=-134.6+10*log10(3e6)
     dmask_f = [900e6/f_scale,1670e6/f_scale]
     dmask_a = [dlim,dlim]
    elif serial[0] == 'u':
     ulim=-122.7+10*log10(3e6)
     mask_f = [0,100e6/f_scale,300e6/f_scale,1200e6/f_scale,NaN,1610e6/f_scale,3600e6/f_scale]
     mask_a = [ulim-13, ulim-13, ulim, ulim,NaN, ulim-13, ulim-13]
     dlim=-137.3+10*log10(3e6)
     dmask_f = [580e6/f_scale,1015e6/f_scale]
     dmask_a = [dlim,dlim]

    #Spectrum analyser data
    Inst = genfromtxt(root+'Instrument.csv', delimiter=',')
    Hpol = genfromtxt(root+'Hpol.csv', delimiter=',')
    Vpol = genfromtxt(root+'Vpol.csv', delimiter=',')
    Hpol_noise = genfromtxt(root+'Hpol_noise.csv', delimiter=',')
    Vpol_noise = genfromtxt(root+'Vpol_noise.csv', delimiter=',')

    #EMSS receiver noise diode models
    Hpol_rx_ndmodel = genfromtxt(root+'rx.'+serial+'.h.csv', delimiter=',')
    Vpol_rx_ndmodel = genfromtxt(root+'rx.'+serial+'.v.csv', delimiter=',')

    #Hpolf = [10**(item/10) for item in Hpol[60:]]
    #fr for frequency response
    Hpol_fr = Hpol[60:]
    Vpol_fr = Vpol[60:]
    Hpol_noise_fr = Hpol_noise[60:]
    Vpol_noise_fr = Vpol_noise[60:]
    # If ND resolution is poor, resample it to uniform resolution approximately matching that of the S/A
    if (mean(diff(Hpol_rx_ndmodel[:,0])) > 10e6): # > 10 MHz qualifies as "poor"
        fh = linspace(Hpol_rx_ndmodel[0,0], Hpol_rx_ndmodel[-1,0], mean(diff(Hpol_fr[:,0])))
        Hpol_rx_ndmodel_1 = interp( fh, Hpol_rx_ndmodel[:,0] , Hpol_rx_ndmodel[:,1])
        Hpol_rx_ndmodel = c_[fh, Hpol_rx_ndmodel_1]
        Vpol_rx_ndmodel_1 = interp( fh, Vpol_rx_ndmodel[:,0] , Vpol_rx_ndmodel[:,1])
        Vpol_rx_ndmodel = c_[fh, Vpol_rx_ndmodel_1]
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
    plt.plot(dmask_f, dmask_a, label='Mask', color='orange', linestyle=':')
    plt.grid()
    plt.legend()
    plt.ylim([-110,-50])
    plt.xlim([0,3.6e9/f_scale])

    #Plot Tsys (and save a png)
    plt.savefig(root+receptor+'_wbg')

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
    plt.savefig(root+receptor+'_T_sys')
    
    return ([fh,fv], [Hpol_,Vpol_], [Hpol_noise_,Vpol_noise_], [Tsysh,Tsysv])

    
if __name__ == "__main__":
    receptor=sys.argv[1] # e.g. 'm015'
    serial=sys.argv[2] # e.g. 'l.4001'
    analyze(receptor, serial)
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About

