#!/usr/bin/python
#Rev. 23/12/2015
#Rev. 29/07/2016

#split_in_two, handle both rxl and rxu files
#usage eg: python csvsplit.py rxl_CalNoise.csv 4002

import csv     # imports the csv module
import sys      # imports the sys module

cal_file=sys.argv[1]
rx_band=cal_file[2]

ifile = open(cal_file, 'rb') # opens the csv file

serial=sys.argv[2] # e.g. '4001'

ofile_h  = open('rx.' +rx_band+ '.' +serial+ '.h.csv', "w")

ofile_v  = open('rx.' +rx_band+ '.' +serial+ '.v.csv', "w")

writer_h = csv.writer(ofile_h, delimiter=',', quotechar='"')
writer_v = csv.writer(ofile_v, delimiter=',', quotechar='"')

try:
    reader = csv.reader(ifile)  # creates the reader object
    writer_h.writerow(["#Rx" + rx_band.upper() + "_SN" + serial + "_calculated_noise_H_chan"])
    writer_h.writerow(["# f (Hz)",   "T_e_cal (K)"])
    writer_v.writerow(["#Rx" + rx_band.upper() + "_SN" + serial + "_calculated_noise_V_chan"])
    writer_v.writerow(["# f (Hz)",   "T_e_cal (K)"])
    reader.next()
    for row in reader:   # iterates the rows of the file in orders
         writer_h.writerow([row[0], row[1]])
         writer_v.writerow([row[0], row[2]])
finally:
    ifile.close()      # closing
    ofile_h.close()      # closing
    ofile_v.close()      # closing


