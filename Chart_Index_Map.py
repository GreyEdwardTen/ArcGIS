def ChartIndex(id):
    """
    to populate chart index from objectid
    """
  if id % 5 == 0:
    return "Sheet 005 of 005"
  else:
    return "Sheet 00" + str(id % 5) + " of 005"



# DRAWING NUMBER
# Select all the features of the same area and input their common names e.g., "GOSL-ZETR-KON-DWG-CL5"
# Then we'll use it to recreate the full number by adding and the sheet number.
# For example if we have already inputted DRAWING_NO = "GOSL-ZETR-KON-DWG-CL5" and for "Sheet 002 of 005":
!DRAWING_NO! = !DRAWING_NO! + "/" + !CHART_INDEX![-10:-7]
#This should give you "GOSL-ZETR-KON-DWG-CL5/002"



# SYMBOLOGY CODE
# Here I'm using the !DRAWING_NO! field as a control.
def Symb(ref,*outputs):
    """
    list all your symbology codes in the order of their drawing numbers in *outputs
    E.g., "IOGP3803", "IOGP3806","IOGP3814", "IOGP3805", "IOGP3804" for singlebeam, seabed features, ... because their drawing numbers end in 001,002,003... in that order 
    """
    return outputs[int(ref[-1:])-1]    
    #This picks the last digit of the number subtracts 1 (for python positioning) and returns the value at that position in the *args 
    
Symb(!DRAWING_NO!, "IOGP3803", "IOGP3806","IOGP3814", "IOGP3805", "IOGP3804")
# For !DRAWING_NO! = "GOSL-ZETR-KON-DWG-CL5/002", this picks 2 subtracts 1 => 1, and returns the value at 1 in the *args => "IOGP3806"


# DRAWING URL
# First input your common hyperlink path to the folder in the Drawing URL field
# e.g., "..\..\Document_Reports\Charts\CLUSTER 5\"
# Then we'll use it to recreate the full URL by ading
!DRAWING_URL! = !DRAWING_URL! + "\\" + !DRAWING_NO!.replace("/", "-") + " - " + !DRAWING_NAME! + ".pdf"
