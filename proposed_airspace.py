from polycircles import polycircles
import simplekml
import geMap
import numpy


MKT = (geMap.ToDecDeg(-30,42,46.53), geMap.ToDecDeg(21,26,37.69))
NE = (geMap.ToDecDeg(-30,27,59.12), geMap.ToDecDeg(21,52,56.02))
SW = (geMap.ToDecDeg(-31,4,8.89), geMap.ToDecDeg(21,7,25.94))

R50_sect=geMap.genArcSeg(MKT, 50*1000, 20001*.3, SW, NE)
R50_sectu=geMap.genArcSeg(MKT, 50*1000, 65000*.3, SW, NE)
R50_sect3d=geMap.gen3D(R50_sect,65000*.3)

#R30_low = polycircles.Polycircle(latitude=MKT[0],
#			longitude=MKT[1],
#			radius=30*1000,
#			number_of_vertices=36)

R30_circ = geMap.genCircle(MKT[0], MKT[1], 30*1000, 20000*.3)

kml = simplekml.Kml()
r50_sect = kml.newpolygon(name='Interim', description='Interim restricted airspace', outerboundaryis=geMap.coordStr2Tuparr(R50_sect))
r50_sect.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.cyan)
r50_sect.style.linestyle.width = 5
r50_sect.style.linestyle.color = simplekml.Color.cyan
r50_sect.altitudemode = 'absolute'

r50_sect = kml.newpolygon(name='Interim', description='Interim restricted airspace', outerboundaryis=geMap.coordStr2Tuparr(R50_sect)+(geMap.coordStr2Tuparr(R50_sectu)))
r50_sect.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.cyan)
r50_sect.style.linestyle.width = 5
r50_sect.style.linestyle.color = simplekml.Color.cyan
r50_sect.altitudemode = 'absolute'


r50_sectu = kml.newpolygon(name='Interim', description='Interim restricted airspace', outerboundaryis=geMap.coordStr2Tuparr(R50_sectu))
r50_sectu.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.cyan)
r50_sectu.style.linestyle.width = 5
r50_sectu.style.linestyle.color = simplekml.Color.cyan
r50_sectu.altitudemode = 'absolute'

r50_sect3d = kml.newpolygon(name='3d', description='3d Interim restricted airspace', outerboundaryis=geMap.coordStr2Tuparr(R50_sect3d))
r50_sect3d.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.cyan)
r50_sect3d.style.linestyle.width = 5
r50_sect3d.style.linestyle.color = simplekml.Color.cyan
r50_sect3d.altitudemode = 'absolute'





#r30_low = kml.newpolygon(name="Area above MeerKAT telescope Core", outerboundaryis=R30_low.to_kml() )

r30_low = kml.newpolygon(name="Area above MeerKAT telescope Core", outerboundaryis=geMap.coordStr2Tuparr(R30_circ) )
r30_low.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.yellow)
r30_low.style.linestyle.width = 5
r30_low.style.linestyle.color = simplekml.Color.yellow
r30_low.altitudemode = 'absolute'
r30_low.extrude = 1
r30_low.tesselate = 1

kml.save("Proposed.kml")

