# ---------------------------------------------------------------------------
# fornext.py
# Created on: 2011-11-18 11:13:22.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# \
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
from arcpy import env
  
# set workspace environment
out_path = "C:/arc/work/"

env.workspace = out_path

# indata
lines_c = "C:/Documents and Settings/besn/My Documents/Dropbox/PhD/Papers/1 - The Good, The Bad and The Evil/geodata/PolylinesMatched.shp"
points_base = "C:/Documents and Settings/besn/My Documents/Dropbox/PhD/Papers/1 - The Good, The Bad and The Evil/geodata/good_bad_reclassified"
points_c = points_base+ ".shp"

point_prefix = "p"
line_prefix = "l"
datatable_prefix = "d"

out_name = "matched_points.shp"
rows = arcpy.SearchCursor(lines_c)
fields = arcpy.ListFields(lines_c, None, "All")

# Set local variables

geometry_type = "MULTIPOINT"
template = points_c
has_m = "DISABLED"
has_z = "DISABLED"

# Creating a spatial reference object
spatial_reference = arcpy.SpatialReference(points_base+ ".prj")


point_files = []
counter = 0
line_files = []
line_ids = []

# we loop over the polygons
for row in rows:
    
    rspdid = row.getValue("respondent")
    rspdid = str(rspdid).split(".")[0]
    
    line_ids.append(rspdid)
    
    print "row" + str(rspdid)
    
    # we start a query and get the point beloning to the polyline
    p_rows = arcpy.SearchCursor(points_c, "rspdid=" + str(rspdid),"","","")
    pline = row.getValue("Shape")
    
    polylineGeometryList = []
    polylineGeometryList.append(pline)
    line_filename = out_path + line_prefix + str(rspdid) + ".shp"
    # arcpy.CopyFeatures_management(polylineGeometryList, line_filename) 
    
    arcpy.CreateFeatureclass_management(out_path, line_prefix + str(rspdid), "Polyline", lines_c)
    target_pline_rows = arcpy.InsertCursor(line_filename) 
    target_pline_row = target_pline_rows.newRow()
    target_pline_row.shape = pline
    target_pline_rows.insertRow(target_pline_row)
    
    del target_pline_rows
    del target_pline_row

    pointGeometryList = []
    point_filename = out_path + point_prefix + str(rspdid) + ".shp"
    
    arcpy.CreateFeatureclass_management(out_path, point_prefix + str(rspdid) + ".shp", "Point", template)
    
    target_rows = arcpy.InsertCursor(point_filename) 
    
    for p_row in p_rows:
        p_id = p_row.getValue("rspdid")
        OBJECTID = p_row.getValue("OBJECTID")
        
        print "Point: " + str(p_id)
        print "OBJECTID: " + str(OBJECTID)
        
        point = p_row.getValue("Shape")
        
        y = point.centroid.Y
        x = point.centroid.X
        
        p = arcpy.Point(x, y)
        
        ptGeometry = arcpy.PointGeometry(p)
        
        # print "Size of geometry list now : " + str(len(pointGeometryList))
        
        target_row = target_rows.newRow() 
        target_row.shape = point # ptGeometry 
        target_row.rspdid = rspdid
        target_row.OBJECTID = OBJECTID
       
        target_row.type = p_row.getValue("type")
        target_row.t_nmbr = p_row.getValue("t_nmbr")
        target_row.dropdown = p_row.getValue("dropdown")
        target_row.text = p_row.getValue("text")
        target_row.distance = p_row.getValue("distance")
        target_row.reclass = p_row.getValue("reclass")
        # target_row.FID = p_row.getValue("FID")
        target_row.wrong_assi = p_row.getValue("wrong_assi")
        
        target_rows.insertRow(target_row)
        
        del target_row
        
    del target_rows
    
    searchRadius = ""
    location = "true"
    angle = "true"
    
    print "Written " + point_filename + " to " + line_filename
    # arcpy.Near_analysis(point_filename, line_filename, searchRadius, location, angle)
    # arcpy.GenerateNearTable_analysis(point_filename, line_filename, "c:/arc/gdb.gdb/table_" + str(rspdid), searchRadius, location, angle, "ALL", 3)
    
    point_files.append(point_filename)
    
    del point_filename

    print "Finished " + str(rspdid) + "."
    
    if counter > 0:
        print "appending..."
        
    counter = counter +1
    
    if counter == 5:
        break
    
    
del p_rows
del p_row
del row
    
tables = []
for line_id in line_ids:


    env.workspace = out_path
    arcpy.Near_analysis(out_path + point_prefix + line_id + ".shp", 
                        out_path + line_prefix + line_id + ".shp", 
                        );
                        #searchRadius, 
                        #location, 
                        #angle)
    print line_id
    
    arcpy.GenerateNearTable_analysis(out_path + point_prefix + line_id + ".shp", 
                                     out_path + line_prefix + line_id + ".shp", 
                                     out_path + datatable_prefix + line_id,
                                     searchRadius, 
                                     "LOCATION", 
                                     "ANGLE", 
                                     "ALL", 
                                     3)
    tables.append(out_path + datatable_prefix + line_id)
    
print "Merging ..."
        
arcpy.Merge_management(tables, "c:/arc/work/tables") 
arcpy.Merge_management(point_files, "c:/arc/work/points") 

# dbase = arcpy.TableToDBASE_conversion("c:/arc/work/points", "c:/arc/results/points.dbf")
# print dbase

print "FINISHED"