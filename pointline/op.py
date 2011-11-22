'''
Created on 18/11/2011

@author: besn
'''
# Import arcpy module
import arcpy
from arcpy import env

searchRadius = "200 Meters"

# find location & angle of nearest features
        ocation = "true"
        angle = "true"
  
# set workspace environment
env.workspace = "C:/arc/gdp.gdb"
arcpy.Near_analysis("one_line", "one_point", searchRadius, location, angle)