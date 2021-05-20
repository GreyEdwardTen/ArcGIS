import os
import arcpy
from arcpy import env


workspace = env.workspace = raw_input('Paste your workspace directory (path) here:  ')
Output_Folder = raw_input('Paste your output file path here:  ')
shape_files = [x for x in os.listdir(workspace) if x.endswith('.shp')]
# arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 TM 6 NE') #NOT REALLY NEEDED FOR THIS TOOL
valField = raw_input('Input the field whose values are to be used to populate the cells (Maintain field case)'
                     '(Default = Intensity):') or "Intensity"
assignmentType = raw_input("Type in cell assignment OR press 'Enter' to skip (Default = MEAN)\n(Use any of: "
                           "MEAN, MOST_FREQUENT, SUM, STANDARD_DEVIATION, MAXIMUM, MINIMUM, RANGE, COUNT):  ") or 'MEAN'
priorityField = ""
cellSize = int(raw_input('Input Cell Size for your Raster:  ')) or 1

for files in shape_files:
    # noinspection SpellCheckingInspection
    for inFeatures in shape_files:
        outRaster = r"{}\{}.tif".format(Output_Folder, inFeatures[:-4])
        print('Working on {}.....'.format(inFeatures))
        arcpy.PointToRaster_conversion(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)
        # I used 'inFeatures[:-4}' to remove the '.shp' prefix from the output name, else, we would get 'IKPL01.shp.tif'
        print('Finished writing {}.tif to {}.'.format(inFeatures[:-4], env.workspace))

