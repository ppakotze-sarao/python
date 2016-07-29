#!/usr/bin/python
#Rev. 14/01/2016

#split_in_two
#usage eg: python rec_csv.py 4002

import csv     # imports the csv module
import sys      # imports the sys module

ifile1 = open('rxl_RecGain.csv','rb')
ifile2 = open('rxl_RecNoise.csv','rb')

serial=sys.argv[1] # e.g. '4001'

ofile_h = open('RxL_SN' + serial + '_calculated_noise_H_chan.dat', 'w')
ofile_v = open('RxL_SN' + serial + '_calculated_noise_V_chan.dat', 'w')

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


