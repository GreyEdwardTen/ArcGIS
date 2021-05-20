import os
import arcpy
from arcpy import env
import exceptions, sys, traceback

workspace = env.workspace = raw_input('Paste your workspace directory (path) here:  ')  # Set environment settings
output_shp_folder = raw_input('Specify output shapefile path here (OPTIONAL):  ') or workspace
output_raster_folder = raw_input('Paste your output raster path here:  ')


ascii_files = [x for x in os.listdir(workspace) if x.endswith('.xyzi')]
shape_files = [x for x in os.listdir(output_shp_folder) if x.endswith('.shp')]

# CONVERTING ASCII TO POINT FEATURE

try:
    arcpy.CheckOutExtension("3D")
    # Define the spatial reference using the name
    sr = arcpy.SpatialReference("WGS 1984 TM 6 NE")
    for ascii in ascii_files:
        outFeature = "{}\{}".format(output_shp_folder, ascii[:-5])
        # Create the elevation points
        arcpy.ddd.ASCII3DToFeatureClass("{}\\{}".format(workspace, ascii), "XYZ",
                                        "{}.shp".format(outFeature),
                                        "POINT", z_factor=1,
                                        input_coordinate_system=sr, file_suffix="xyzi")

except arcpy.ExecuteError:
    print arcpy.GetMessages()
except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # Concatenate error information into message string
    pymsg = 'PYTHON ERRORS:\nTraceback info:\n{0}\nError Info:\n{1}' \
        .format(tbinfo, str(sys.exc_info()[1]))
    msgs = 'ArcPy ERRORS:\n {0}\n'.format(arcpy.GetMessages(2))
    # Return python error messages for script tool or Python Window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)


# CONVERTING POINT FEATURE TO RASTER
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('WGS 1984 TM 6 NE')
valField = "Intensity"
assignmentType = "MEAN"
priorityField = ""
cellSize = 1

for files in shape_files:
    # noinspection SpellCheckingInspection
    for inFeatures in shape_files:
        outRaster = "{}\{}.tif".format(output_raster_folder, inFeatures[:-4])
        print('Working on {}.....'.format(inFeatures))
        arcpy.PointToRaster_conversion(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)
        # I used 'inFeatures[:-4}' to remove the '.shp' prefix from the output name, else, we would get 'IKPL01.shp.tif'
        print('Finished writing {}.tif to {}.'.format(inFeatures[:-4], env.workspace))
