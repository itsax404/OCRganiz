
class Detection_rect():
    def __init__(self, scale, topx, topy, botx, boty, translation_x, translation_y, n_img, id):
        self.scale = scale
        print(f"topx= {topx} botx={botx} topy = {topy} boty = {boty}")
        if botx < topx:
            tmp = botx
            botx = topx
            topx = tmp
        if boty < topy:
            tmp = boty
            boty = topy
            topy = tmp

        self.topx = topx - translation_x
        self.topy = topy - translation_y

        self.botx = botx - translation_x
        self.boty = boty - translation_y

        self.n_img = n_img
        self.id = id


    def dimension(self):
        dimension = tuple((self.topx * (1 / self.scale), self.topy * (1 / self.scale), self.botx * (1 / self.scale),
               self.boty * (1 / self.scale)))
        return dimension


    def get_topx(self):
        topx = (self.topx / self.scale)
        return topx


    def get_topy(self):
        topy = (self.topy / self.scale)
        return topy


    def get_botx(self):
        botx = (self.botx / self.scale)
        return botx


    def get_boty(self):
        boty = (self.boty / self.scale)
        return boty


    def get_nimg(self):
        return self.n_img


    def get_id(self):
        return self.id