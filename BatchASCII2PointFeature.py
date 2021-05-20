"""****************************************************************************
Name: ASCII3D_to_Feature_Class Example
Description: Creates a TIN surface using XYZI files in a folder and breaklines
             imported from ASCII files.
****************************************************************************"""
# Import system modules`
import os
import arcpy
from arcpy import env
import exceptions, sys, traceback


workspace = env.workspace = raw_input('Paste your workspace directory (path) here:  ')  # Set environment settings
output_folder = raw_input('Specify output shapefile path here (OPTIONAL):   ') or workspace
ascii_ext = raw_input('Specify extension of ascii here: .')
ascii_files = [x for x in os.listdir(workspace) if x.endswith('.{}'.format(ascii_ext))]
shape_files = [x for x in os.listdir(output_folder) if x.endswith('.shp')]

try:
    arcpy.CheckOutExtension("3D")
    # Define the spatial reference using the name
    sr = arcpy.SpatialReference("WGS 1984 TM 6 NE")
    for inFile in ascii_files:
        outRaster = "{}\{}".format(output_folder, inFile[:-5])
        # Create the elevation points
        arcpy.ddd.ASCII3DToFeatureClass("{}\\{}".format(workspace, inFile), "XYZI",
                                        "{}.shp".format(outRaster),
                                        "POINT", z_factor=1,
                                        input_coordinate_system=sr, file_suffix=ascii_ext)

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
