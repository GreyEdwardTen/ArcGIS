import math

def calculate_bearing(x1, y1, x2, y2):
    rad = math.atan2(y2 - y1, x2 - x1)
    deg = math.degrees(rad)
    bearing = (90 - deg + 360) % 360
    return bearing
  
