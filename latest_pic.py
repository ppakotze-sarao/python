#!/usr/bin/python
import urllib
import urllib2
import ftplib
import time

work_dir = '/home/pkotze/tmp/'

ftp_host = 'www.qsl.net'
ftp_user = 'zs1pk'
ftp_pass = 'hxh4fp24'

image_file = 'oneshotimage.jpg'
high = '10.97.242.9'
webcam1 = 'http://asc-webcam1.karoo.kat.ac.za/cgi-bin/camera'
webcam2 = 'http://asc-webcam2.karoo.kat.ac.za/cgi-bin/camera?resolution=1280'
url = 'http://' + high + '/' + image_file

image = urllib.URLopener()
image.retrieve(webcam1, work_dir + image_file)

ftp_image=open(work_dir + image_file, 'rb')
ftp_session2 = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
ftp_session2.storbinary('STOR ' + image_file, ftp_image)
ftp_session2.quit()
ftp_image.close()
