def line_prefix(layer, objectid):
    if layer == "Parallel Lines":
        return "PL" + str(51 - objectid).zfill(3)
    elif layer == "Cross Lines":
        return f"XL{str(62 - objectid).zfill(3)}"
