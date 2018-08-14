from scipy.constants import *


#3C273 has a source brightness of about 50 Jansky at 800MHz
# dumb engineer needs Noise temperature to do Y factor measurement
# for point source simplification

#S_V A = 2 k T_A 5.7 BAARS book

SV=50 * 1e-26 # in Jansky http://isdc.unige.ch/3c273/

r=13.5/2 #13.5m effective diameter 

A=pi*r**2 * 0.8 #used aperture efficiency here

T_A=SV*A/(2*k)

print(T_A)

#Performed some accelerated drift scans on 3C273 with the band 1 receiver
 
T_h=T_A   #what other elements do I need to consider? #aha unless T_c includes all these

Y_Hpol_old = 0.15
Y_Vpol_old = 0.44

Y_Hpol = 0.43
Y_Vpol = 0.4

Y_db=Y_Hpol

Y=10**(Y_db/10)

Tsys=T_h/(Y-1)

print(Tsys)


