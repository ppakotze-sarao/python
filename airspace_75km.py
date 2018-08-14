from polycircles import polycircles
import simplekml
import geMap

MKT = (geMap.ToDecDeg(-30,42,46.53), geMap.ToDecDeg(21,26,37.69))

above_MKT = polycircles.Polycircle(latitude=MKT[0],
			longitude=MKT[1],
			radius=75*1000,
			number_of_vertices=360)

kml = simplekml.Kml()
pol = kml.newpolygon(name="Area above MeerKAT telescope Core", outerboundaryis=above_MKT.to_kml() )
pol.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.green)

kml.save("Above MKT 90.kml")

