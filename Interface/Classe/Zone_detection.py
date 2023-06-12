

class Detection_rect():
    def __init__(self, scale, topx, topy, botx, boty, translation_x, translation_y, n_img):
        self.scale = scale

        self.topx = topx - translation_x
        self.topy = topy - translation_y

        self.botx = botx - translation_x
        self.boty = boty - translation_y

        self.n_img = n_img


    def dimension(self):
        dimension = tuple((self.topx * (1 / self.scale), self.topy * (1 / self.scale), self.botx * (1 / self.scale),
               self.boty * (1 / self.scale)))
        return dimension


    def get_topx(self):
        topx = (self.topx / self.scale) * 0.25
        return topx


    def get_topy(self):
        topy = (self.topy / self.scale) * 0.25
        return topy


    def get_botx(self):
        botx = (self.botx / self.scale) * 0.25
        return botx


    def get_boty(self):
        boty = (self.boty / self.scale) * 0.25
        return boty


    def get_nimg(self):
        return self.n_img