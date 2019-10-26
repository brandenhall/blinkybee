def hex_to_rgb(hex):
    h = hex[1:]
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_float(rgb):
    r, g, b = rgb
    return (r/255.0, g/255.0, b/255.0)

def float_to_rgb(values):
    r, g, b = values
    return (round(r * 255.0), round(g * 255.0), round(b * 255.0))