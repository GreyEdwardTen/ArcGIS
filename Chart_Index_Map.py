def ChartIndex(id):
    """to populate chart index from objectid"""
  if id % 5 == 0:
    return "Sheet 005 of 005"
  else:
    return "Sheet 00" + str(id % 5) + " of 005"
