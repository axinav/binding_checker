from qgis.core import QgsGeometry, QgsPoint

def getUniquePnts(geom:QgsGeometry)->list[QgsPoint]:
    pntsLst = list(geom.vertices())
    uniquePntsLst = []
    uniqueWkbSet = set()
    for p in (pntsLst):
        if not (p.asWkb() in uniqueWkbSet):
            uniquePntsLst.append(p)
            uniqueWkbSet.add(p.asWkb())
    return uniquePntsLst

if __name__ == "__main__":
    geometry = QgsGeometry.fromWkt( "MultiPolygon((( 0 0, 0 10, 10 10, 10 0, 0 0 ),( 5 5, 5 6, 6 6, 6 5, 5 5)),((20 2, 22 2, 22 4, 20 4, 20 2)))" )
    for p in geometry.vertices():
        print(p)
    for p in getUniquePnts(geometry):
        print(p)

