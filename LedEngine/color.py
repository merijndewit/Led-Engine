class Color():
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
    
    def get_position_tup(self):
        return (self.pixel)
    
    def get_color_tup(self):
        return ((self.r, self.g, self.b))
    
    def set_color_rgb_tup(self, rgb):
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]
        
    def set_color_hex(self, hex_string):
        string = hex_string.lstrip("#")
        self.set_color_rgb_tup((int(string[:2], 16), int(string[2:4], 16), int(string[4:6], 16)))
        