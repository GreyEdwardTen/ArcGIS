def ChartIndex(id):
    """to populate chart index from objectid"""
  if id % 5 == 0:
    return "Sheet 005 of 005"
  else:
    return "Sheet 00" + str(id % 5) + " of 005"



# DRAWING NUMBER
# Select all the features of the same area and input their common names e.g., "GOSL-ZETR-KON-DWG-CL5"
# Then we'll use it to recreate the full number by adding and the sheet number.
# For example if we have already inputted DRAWING_NO = "GOSL-ZETR-KON-DWG-CL5" and for "Sheet 002 of 005":
!DRAWING_NO! + "/" + !CHART_INDEX![-10:-7]
#This should give you "GOSL-ZETR-KON-DWG-CL5/002"


# DRAWING URL
# First input your common hyperlink path to the folder in the Drawing URL field
# e.g., "..\..\Document_Reports\Charts\CLUSTER 5\"
# Then we'll use it to recreate the full URL by ading
!DRAWING_URL! + "\\" + !DRAWING_NO!.replace("/", "-") + " - " + !DRAWING_NAME! + ".pdf"
