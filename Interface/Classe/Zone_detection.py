

class Detection_rect():
    def __init__(self, scale, topx, topy, botx, boty, offsetx, offsety):
        self.scale = scale

        self.topx = topx
        self.topy = topy

        self.botx = botx
        self.boty = boty

        self.offsetx = offsetx
        self.offsety = offsety


    def dimension(self):
        dimension = tuple((self.topx * (1 / self.scale), self.topy * (1 / self.scale), self.botx * (1 / self.scale),
               self.boty * (1 / self.scale)))
        return dimension
