import os
import arcpy
from arcpy import management, ddd, env
import exceptions
import sys
import traceback


station_type = raw_input('Enter instrument/sensor or station type:     ')
workspace = env.workspace = raw_input('Paste your workspace directory (path) here:  ')  # Set environment settings
ascii_folder = raw_input('Input ASCII Folder (OPTIONAL, Default = Workspace):   ') or workspace
out_shp_folder = raw_input('Output Shapefile Folder (OPTIONAL, Default = Workspace):   ') or workspace
ascii_ext = (raw_input('Input new ascii file extension:    .'))
merged_shp_folder = (workspace or out_shp_folder) + '\\MERGED'
if not os.path.exists(merged_shp_folder):
    os.makedirs(merged_shp_folder)
merged_shp_file = merged_shp_folder + '\\' + raw_input('Enter merged output shapefile name:    ') + '.shp'

print('\nNOW TO ADD A FIELD')
fieldName = raw_input('Input your Field Name (no spaces):  ')
fieldPrecision = raw_input('Input Field Precision '
                           '(FOR NUMERIC: The number of digits that can be stored in the field):  ')
FieldType = raw_input('What field type would you like to create (pick letter)?'
                      '\nText           ----> T'
                      '\nDouble         ----> D'
                      '\nShort Integer  ----> S'
                      '\nLong Integer   ----> L'
                      '\nFloating Point ----> F'
                      '\n')
field_dict = {'T': 'TEXT', 'D': 'DOUBLE', 'S': 'SHORT', 'L': 'LONG', 'F': 'FLOAT'}
fieldLength = raw_input('Input your Field Length (Default <Text> = 250, <others> = 50):  ')\
              or [50 if FieldType != 'T' else 250]

# expression_input = raw_input('Input ARCGIS FIELD CALCULATOR python expression here (or skip to use ordinary py code):'
#                              '\nNOTE: Field names must be enclosed in exclamation points (e.g. !fieldname!)\n')
# code = raw_input('Input python code here (or press enter to use ARCGIS based python code):   ')

spatial_ref = input('Define spatial ref or EPSG code (Default = WGS 1984 TM 6 NE or 2311 <EPSG>):   ') or 2311
sr = arcpy.SpatialReference(spatial_ref)


# CONVERTING ALL ASCII TO NEW ASCII EXTENSION (.txt)
print('\nChanging files extension to ".{}".....'.format(ascii_ext.lower()))

file_list = [x for x in os.listdir(ascii_folder) if x.endswith('.xyz')]
for xyz_file in file_list:
    my_file = str(ascii_folder + '\\' + xyz_file)
    base = os.path.splitext(my_file)[0]  # Splits the path into a pair (root, ext) & [0] takes the first value (root)
    os.rename(my_file, base + '.' + ascii_ext.lower())

print('\nFiles extension has been changed to ".{}"'.format(ascii_ext.lower()))

ascii_files = [x for x in os.listdir(ascii_folder) if x.endswith('.{}'.format(ascii_ext.lower()))]


# CONVERTING ASCII TO POINT FEATURE
print('\nCreating Point Features from ASCII.....')

try:
    arcpy.CheckOutExtension("3D")
    # Define the spatial reference using the name
    sr = arcpy.SpatialReference("WGS 1984 TM 6 NE")
    for inFile in ascii_files:
        outFeature = "{}\{}".format(out_shp_folder, inFile[:-4])
        # Create the elevation points
        arcpy.ddd.ASCII3DToFeatureClass("{}\{}".format(ascii_folder, inFile), "XYZ",
                                        "{}.shp".format(outFeature),
                                        "POINT", z_factor=1,
                                        input_coordinate_system=sr, file_suffix=ascii_ext.lower())

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

print('\nDone Creating Point Feature Classes.'
      '\nSee results in {}.'.format(out_shp_folder))


# ADD FIELD TO TABLE
shp_files = [x for x in os.listdir(out_shp_folder) if x.endswith('.shp')]

print('\nAdding {} field to shapefiles.....'.format(fieldName))

for x in shp_files:
    inFeatures = out_shp_folder + '\\' + x
    arcpy.AddField_management(inFeatures, fieldName, field_dict[FieldType.upper()],
                              field_length=fieldLength)
    # Add additional 'SHOT_POINT_ID' field automatically
    arcpy.AddField_management(inFeatures, 'SHOT_PT_ID', "LONG", "", "", "", "", "NULLABLE")
    # CALCULATE FIELDS
    # # expression = ("{}".format(expression_input)) or code
    expression = "'{}'".format(x.split('_', 1)[0])
    arcpy.CalculateField_management(inFeatures, fieldName, expression, "PYTHON_9.3")
    arcpy.CalculateField_management(inFeatures, 'SHOT_PT_ID', "!FID!+1", "PYTHON_9.3")

print('\nDone adding and calculating fields')


# MERGE SHAPEFILES

print('\nMerging shapefiles....')

# Merge shapefiles
in_Merge = [(out_shp_folder + '\\' + x) for x in os.listdir(out_shp_folder) if x.endswith('.shp')]
arcpy.Merge_management(in_Merge, merged_shp_file)
# Add Instrument/Sensor Name Field
arcpy.AddField_management(merged_shp_file, 'Instrument', field_type='TEXT', field_length='250')
# Calculate Instrument Field
instrument = "'{}'".format(station_type)
arcpy.CalculateField_management(merged_shp_file, 'Instrument', expression=instrument, expression_type="PYTHON_9.3")

print('\nDone merging shapefiles.'
      '\nSee result in {}.'.format(merged_shp_file))


input('Press Enter to Exit')
