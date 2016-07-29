#!/usr/bin/python
#Rev. 23/12/2015

#split_in_two
#usage eg: python csvsplit.py m025.csv 4002

import csv     # imports the csv module
import sys      # imports the sys module

ifile = open(sys.argv[1], 'rb') # opens the csv file

serial=sys.argv[2] # e.g. '4001'

ofile_h  = open('rx.l.'+serial+'.h.csv', "w")

ofile_v  = open('rx.l.'+serial+'.v.csv', "w")

writer_h = csv.writer(ofile_h, delimiter=',', quotechar='"')
writer_v = csv.writer(ofile_v, delimiter=',', quotechar='"')

try:
    reader = csv.reader(ifile)  # creates the reader object
    writer_h.writerow(["#RxL_SN" + serial + "_calculated_noise_H_chan"])
    writer_h.writerow(["# f (Hz)",   "T_e_cal (K)"])
    writer_v.writerow(["#RxL_SN" + serial + "_calculated_noise_V_chan"])
    writer_v.writerow(["# f (Hz)",   "T_e_cal (K)"])
    reader.next()
    for row in reader:   # iterates the rows of the file in orders
         writer_h.writerow([row[0], row[1]])
         writer_v.writerow([row[0], row[2]])
finally:
    ifile.close()      # closing
    ofile_h.close()      # closing
    ofile_v.close()      # closing


