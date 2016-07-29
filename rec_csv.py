#!/usr/bin/python
#Rev. 14/01/2016
#Rev. 29/07/2016

#split_in_two, make robust for l or u band receivers (or any)
#usage eg: python rec_csv.py rxl_RecGain.csv rxl_RecNoise.csv 4002

import csv     # imports the csv module
import sys      # imports the sys module

#files to read
gain_files=sys.argv[1] # e.g. 'rxl_RecGain.csv'
noise_files=sys.argv[2] # e.g. 'rxl_RecNoise.csv'
rx_band=gain_files[2]
ifile1 = open('rx' +rx_band+ '_RecGain.csv','rb')
ifile2 = open('rx' +rx_band+ '_RecNoise.csv','rb')

serial=sys.argv[3] # e.g. '4001'

#files to be written
ofile_h = open('Rx' +rx_band.upper()+ '_SN' + serial + '_calculated_noise_H_chan.dat', 'w')
ofile_v = open('Rx' +rx_band.upper()+ '_SN' + serial + '_calculated_noise_V_chan.dat', 'w')

writer_h = csv.writer(ofile_h, delimiter=',', quotechar='"')
writer_v = csv.writer(ofile_v, delimiter=',', quotechar='"')

try:
    reader_gain = csv.reader(ifile1)  # creates the reader object
    reader_noise = csv.reader(ifile2) 
    writer_h.writerow(["% f (Hz)",   "G_rec (dB)", "T_e_rec (K)"])
    writer_v.writerow(["% f (Hz)",   "G_rec (dB)", "T_e_rec (K)"])
    reader_gain.next()
    reader_noise.next()
    for row_g in reader_gain:   # iterates the rows of the file in orders
    # for row_n in reader_noise:
         row_n = reader_noise.next()
         writer_h.writerow([row_g[0], row_g[1], row_n[1]])
         writer_v.writerow([row_g[0], row_g[2], row_n[2]])
finally:
    ifile1.close()      # closing
    ifile2.close()
    ofile_h.close()      # closing
    ofile_v.close()      # closing


