#!/usr/bin/python
#log_smy.py
#Rev. 24/4/2018

#Opens logbook.csv and calculate totals to be configurable per past 12 months, etc.
#usage eg: python log_smy.py logbook.csv 

import csv     # imports the csv module
import sys      # imports the sys module
import datetime  #want to go back to the future
import re        #for fancier text matching

#files to read
logbook_f  = sys.argv[1] # e.g 'logbook.csv'
input_date = sys.argv[2] if len(sys.argv[2]) > 0 else [1903,12,17] # e.g. '12'for number of months
output_f   = sys.argv[3] # e.g. '12month.txt'
ac_type    = sys.argv[4]

ifile1 = open(logbook_f,'rb')

#could write to file the results
ofile = open(output_f, 'w')
# my_list = list(ifile1)
# my_dict = dict(ifile1)
input_dlist=input_date.split('-')
[y,m,d] = [int(item) for item in input_dlist]
start_date = datetime.datetime(y,m,d,0,0,0)


hrs = [0.0] * 24
hours = 0.0 
phours = 0.0
with open(logbook_f, 'rb') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
	    [ry,rm,rd] = [int(x) for x in (row[0].split(' ')[0].split('-'))]
            #if datetime.datetime(ry,rm,rd) > start_date and row[1] == ac_type:
	    if datetime.datetime(ry,rm,rd) > start_date and bool(re.search(ac_type, row[1])):
		print(row)
		rhrs = [float(cell) if cell != '' else 0.0 for cell in row[7:31]] # if row[i]!='' else row[i]]
		print(rhrs)
		hrs = [hrs[i]+rhrs[i] for i in range(24)] 
		print (hrs)
		if row[13] != '':
			print (row[13])
			hours=hours+float(row[13])
#			print('Dual Hours:', hours)
 		if row[14] != '':
			print (row[14])
			phours=phours+float(row[14])
#			print('Pic Hours:', phours)
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

totals=0
actual=0
for i in range(2,22):
	totals=totals+hrs[i] 
for i in range(6,22):
	actual=actual+hrs[i]
print('dual: ', hours, 'pic ', phours, 'combined: ', actual, 'all totals: ', totals)

#n [84]: duh=[(row.split(',')[13].strip('\"')) for row in my_list if row.split(',')[1] == '"C77R"']

#In [85]: duh
#Out[85]: ['1.1', '1.3', '1.4', '0.8', '1.4', 'None', '0.7', 'None']
