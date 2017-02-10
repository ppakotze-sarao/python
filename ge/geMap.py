#%example simple restricted area
#clear all;
#close all;
#%Date 2008/09/08

#%conversion factors
#%1 meter = 3.2808399feet 

nm = 1852 #1nm = 1852 meters 
m_to_ft=3.2808399

#KML header used before - origin?
kml_header="""
<kml>
<Document>
	<Style id="sh_ylw-pushpin">
		<IconStyle>
			<scale>1.2</scale>
		</IconStyle>
		<LineStyle>
			<color>ff0000ff</color>
			<width>5</width>
		</LineStyle>
	</Style>
	<StyleMap id="msn_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_ylw-pushpin</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="sn_ylw-pushpin">
		<LineStyle>
			<color>ff0000ff</color>
			<width>5</width>
		</LineStyle>
	</Style>
     
     <Placemark>
      <styleUrl>#msn_ylw-pushpin</styleUrl>
        <LineString>
        			<extrude>1</extrude>
			<tessellate>1</tessellate>
			<altitudeMode>absolute</altitudeMode>       
               <coordinates>
 """

kml_header2="""
<kml>
<Document>
	<Style id="sh_ylw-pushpin">
		<IconStyle>
			<scale>1.2</scale>
		</IconStyle>
		<LineStyle>
			<color>ff0000ff</color>
			<width>5</width>
		</LineStyle>
	</Style>
	<StyleMap id="msn_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_ylw-pushpin</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="sn_ylw-pushpin">
		<LineStyle>
			<color>ff0000ff</color>
			<width>5</width>
		</LineStyle>
	</Style>
     
     <Placemark>
      <styleUrl>#msn_ylw-pushpin</styleUrl>
        <LineString>
        			<extrude>1</extrude>
			<tessellate>1</tessellate>
			<altitudeMode>clampToGround</altitudeMode>       
               <coordinates>
 """
 
#KML footer used before - origin?
kml_footer="""
        
        </coordinates>
        
        </LineString>
    </Placemark>

</Document>
</kml>

"""
#kml lines of coordinates
kml_line_start="""

<!--Separate line of coordinates start-->
"""
#kml lines of coordinates

kml_line_stop="""

<!--Separate line of coordinates stop-->"""

#%Convert to Decimal degrees
#from math import pi, floor, sqrt, sin, cos, asin, atan2
#from math import asin, atan2
from numpy import pi, floor, sqrt, sin, cos
from numpy import arcsin as asin
from numpy import arctan2 as atan2

def coordStr2Arr(coordText):
    rowText=''
    coordArray=[]
    for coordChar in coordText:
        if coordChar == ' ':
            coordArray.append(rowText)
            rowText=''
        else:
            rowText=rowText+coordChar
    return(coordArray)

def coordArr2Str(coordArray):
    coordText=''
    for arrayItem in coordArray:
        coordText=coordText+str(arrayItem)+' '
    return(coordText)

def ToDecDeg(LatH, LatM, LatS):
    """
        Convert to decimal degrees from HMS
        """
    if LatH > 0:
        LatDec = float(LatH)+float(LatM)/60+float(LatS)/3600
    else:
        LatDec = float(LatH)-float(LatM)/60-float(LatS)/3600
    return(LatDec)

def ToHMSDeg(LatDec):
    """
    Convert to HMS from decimal degrees
    For the Python 2.x series / does "floor division" for integers and longs (e.g. 5/2=2) 
    but "true division" for floats and complex (e.g. 5.0/2.0=2.5). 
    For Python 3.x, / does "true division" for all types.
    """
    LatH = floor(LatDec)
    LatM = floor((LatDec-LatH)*60)
    LatS = round((LatDec-LatH-LatM/60)*3600)
    return(LatH, LatM, LatS)
    
def caaDecDeg(caaStr):
    """
    Takes CAA string format e.g. S341740.00 E0193130.00
    and returns (-34,17,40)
    (deg,min,seconds)
    """
    if caaStr[0]=='S':
        lat_deg='-'+caaStr[1:3]
        lat_min=caaStr[3:5]
        lat_sec=caaStr[5:10]
    elif caaStr[0]=='N':
        lat_deg=caaStr[1:3]
        lat_min=caaStr[3:5]
        lat_sec=caaStr[5:10]
    else:
        print 'Fault processing CAA lat string'
    
    if caaStr[11]=='E':
        long_deg=(caaStr[12:15])
        long_min=(caaStr[15:17])
        long_sec=(caaStr[17:22])
    elif caaStr[11]=='W':
        long_deg='-'+caaStr[12:15]
        long_min=caaStr[15:17]
        long_sec=caaStr[17:22]
    else:
        print 'Fault processing CAA long string'
    return (ToDecDeg(long_deg, long_min, long_sec)),(ToDecDeg(lat_deg, lat_min, lat_sec )) 
    
def coordsFrom((lat1deg),(lon1deg),(thetadeg),d):
    """
        Returns co-ordinates at an offset and bearing from a reference coordinate point
         d     = distance in meters from Lat1,Lon1
         Theta = true angle in degrees from Lat1,Lon1
         lat2 = asin(sin(lat1)*cos(d/R) + cos(lat1)*sin(d/R)*cos(?)) 
         lon2 = lon1 + atan2(sin(?)*sin(d/R)*cos(lat1), cos(d/R)-sin(lat1)*sin(lat2)) 
         d/R is the angular distance (in radians), where d is the distance travelled 
         and R is the earth's radius
         JavaScript: 
            var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) + 
                              Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng) );
            var lon2 = lon1 + Math.atan2(Math.sin(brng)*Math.sin(d/R)*Math.cos(lat1), 
                                     Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2)); 
         Excel: lat2: =ASIN(SIN(lat1)*COS(d/ER) + COS(lat1)*SIN(d/ER)*COS(brng))
                lon2: =lon1 + ATAN2(COS(d/ER)-SIN(lat1)*SIN(lat2), SIN(brng)*SIN(d/ER)*COS(lat1)) %
         For b bearing, simply take the A bearing from the end point to the start point 
         and reverse it (using ? = (?+180) % 360).
         returns [Lat2,Lon2]
         """
    lat1=((lat1deg)/180*pi)
    lon1=((lon1deg)/180*pi)
     #thetadeg is bearing in degrees, convet to radians
    theta=(thetadeg)/180*pi
    #print theta
    
    # Radius of the earth a=equatorial radius, b=polar radius
    a=6378.137e3; 
    b=6356.7523e3;
    phi=lat1
    R=sqrt( ( pow(pow(a,2)*cos(phi),2) + pow(pow(b,2)*sin(phi),2) )/( pow(a*cos(phi),2) + pow(b*sin(phi),2) ))
    #R=6371e3

    lat2 = (asin(sin(lat1)*cos(d/R) + cos(lat1)*sin(d/R)*cos(theta)) )
    #print lat2
    lat2deg = lat2/pi*180
    lon2 = (lon1 + atan2(sin(theta)*sin(d/R)*cos(lat1), cos(d/R)-sin(lat1)*sin(lat2)) )
    #print lon2
    #lon2 = (lon1 + atan2( cos(d/R)-sin(lat1)*sin(lat2), sin(theta)*sin(d/R)*cos(lat1) ))
    lon2deg = lon2/pi*180
    return([lat2deg, lon2deg])
    #%52deg58'52?N, 000deg53'15?E

def genCirclePoint(centreLat, centreLon, circleAngle, circleRadius, circleAlt):
    """
    Gen coordinates for a circle point
    expect decimal lat longs
    """
    newLatLon=coordsFrom( float(centreLat), float(centreLon) , float(circleAngle), float(circleRadius) )
    newLat=newLatLon[0]
    newLon=newLatLon[1] 
    newLine = [newLon] + [newLat] + [float(circleAlt)]
    return(newLine)

def genCircle(centreLat, centreLon, circleRadius, circleAlt):
    """
    Gen coordinates for a circle point
    expect decimal lat longs
    """
    circleText=''   
    for angle in range(360):
        circleLine=genCirclePoint( float(centreLat), float(centreLon) , float(angle), float(circleRadius), float(circleAlt))
        #for l in circleLine: circleText=circleText+str(l)+', '
        circleText=circleText+str(circleLine[0])+','+str(circleLine[1])+','+str(circleLine[2])+' '
    return circleText       
       
def genCircleComp(centreLL, circleRadius, circleAlt):
    """
    Gen coordinates for a circle point
    expect decimal lat longs
    """
    circleText=''   
    for angle in range(360):
        circleLine=genCirclePoint( float(centreLL[1]), float(centreLL[0]) , float(angle), float(circleRadius), float(circleAlt))
        #for l in circleLine: circleText=circleText+str(l)+', '
        circleText=circleText+str(circleLine[0])+','+str(circleLine[1])+','+str(circleLine[2])+' '
    return circleText       

def genArc(centreLat, centreLon, arcRadius, arcAlt, LL, RL, DL):
    """
    Gen coordinates for a circle
    expect decimal lat longs
    """
    arcText=''
    for angle in range(0,360):
        circleLine=genCirclePoint( float(centreLat), float(centreLon) , float(angle), float(arcRadius), float(arcAlt))     
        newLon=circleLine[0]
        newLat=circleLine[1]
        if newLat>=DL and newLon>=LL and newLon<=RL: 
            #for l in circleLine: arcText=arcText+str(l)+' '
             arcText=arcText+str(circleLine[0])+','+str(circleLine[1])+','+str(circleLine[2])+' '
    return arcText

def encapPlace(coordStr):
    """
    Gen coordinates for a circle
    expect decimal lat longs
    """
    placeTxt=kml_line_start + str(coordStr) + kml_line_stop
    return placeTxt

def genCoordStr(coordDecTuple, coordAlt):
    """
    Gen coordStr from Tuple and coordAlt floats returns string
    """
    return (str(coordDecTuple[0]) +',' +str(coordDecTuple[1]) +',' +str(coordAlt) +' ' )

	
def calcHeading(lat1deg, lon1deg, lat2deg, lon2deg):
    """
    http://www.movable-type.co.uk/scripts/latlong.html
    var R = 6371; // km
    var dLat = (lat2-lat1).toRad();
    var dLon = (lon2-lon1).toRad();
    var lat1 = lat1.toRad();
    var lat2 = lat2.toRad();
    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    var d = R * c;

    var y = Math.sin(dLon) * Math.cos(lat2);
    var x = Math.cos(lat1)*Math.sin(lat2) -
            Math.sin(lat1)*Math.cos(lat2)*Math.cos(dLon);
    var brng = Math.atan2(y, x).toDeg();
    """
    R = 6371 # km
    lat1=((lat1deg)/180*pi)
    lon1=((lon1deg)/180*pi)
    lat2=((lat2deg)/180*pi)
    lon2=((lon2deg)/180*pi)

    dLat = (lat2-lat1)
    dLon = (lon2-lon1)

    a = sin(dLat/2) * sin(dLat/2) + sin(dLon/2) * sin(dLon/2) * cos(lat1) * cos(lat2) 
    b = 2 * atan2(sqrt(a), sqrt(1-a)) 
    distance = R * b * 1000

    y = sin(dLon) * cos(lat2)
    x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon)
    brng = atan2(y, x) 


    lat2=((lat1deg)/180*pi)
    lon2=((lon1deg)/180*pi)
    lat1=((lat2deg)/180*pi)
    lon1=((lon2deg)/180*pi)

    dLat = (lat2-lat1)
    dLon = (lon2-lon1)

    y = sin(dLon) * cos(lat2)
    x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon)
    final = (atan2(y, x)+ pi) % (2*pi)
 
    return [brng/pi*180, final/pi*180, distance]
