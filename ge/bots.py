#!/usr/bin/python
#Rev. 13/02/2017
#Open text files and create KML
#also write in HH MM SS format

from numpy import *
import geMap

#Some constants
bots_border='''
<b>Name:</b> Botswana
</div>]]></description>
			<styleUrl>#Style0-polygon-3-map</styleUrl>
			<ExtendedData>
				<Data name='Name'>
					<value>Botswana</value>
				</Data>
			</ExtendedData><Polygon><outerBoundaryIs><LinearRing><coordinates>26.95919,-23.75207 26.845276,-24.264446 25.871387,-24.744446 25.50972,-25.67778 24.6772,-25.82782 23.014832,-25.29972 22.624809,-26.11156 21.667221,-26.86444 20.642498,-26.82806 20.811386,-25.88333 20.000942,-24.765408 19.996666,-22.005001 20.991943,-21.996948 20.993286,-18.318417 23.297108,-17.99595 23.615578,-18.485069 24.3625,-17.94861 25.264431,-17.80225 26.166111,-19.527779 27.22,-20.09167 27.287453,-20.494965 27.713165,-20.50643 28.015831,-21.56611 29.060555,-21.79806 29.373623,-22.19241 28.298332,-22.60945 26.95919,-23.75207</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>
		<Placemark>
			<snippet></snippet>
			<description><![CDATA[<div class="googft-info-window" style="font-family:sans-serif">
			'''
			
fkml = open('botswana.kml', 'w')
fkml.write(geMap.kml_header)
#fkml.write(bots_border)

#FIR

#TMA

#TMA
#Kasane TMA: 
#50nm arc on VOR 174957.88S 0251011.51E stop at border
#alt FL 245 - 5500alt
#class A/C
#127.2 Kasane APP
KSV='174957.88S 0251011.51E'
KSVd=50*geMap.nm #50 nm to meters
KSValt=5500/geMap.m_to_ft
#def genArc(centreLat, centreLon, arcRadius, arcAlt, LL, RL, DL)
#fkml.write(geMap.genLineString("Kasane TMA", geMap.genArc(geMap.aipDecDeg(KSV)[0], geMap.aipDecDeg(KSV)[1], KSVd, 5500, 0, 0, 0)) )
fkml.write(geMap.genLineString("Kasane TMA", geMap.genCircle(geMap.aipDecDeg(KSV)[0], geMap.aipDecDeg(KSV)[1], KSVd, 5500 )) )
 
fkml.write((geMap.kml_footer))
fkml.close()

