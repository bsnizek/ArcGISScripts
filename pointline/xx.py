import arcpy
point = arcpy.Point(25282, 43770)
print point.X
ptGeometry = arcpy.PointGeometry(point)
print ptGeometry