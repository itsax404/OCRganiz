class Detection_rect():
    def __init__(self, scale: float, topx: float, topy: float, botx: float, boty: float, translation_x: float,
                 translation_y: float, n_img: int, id: str):
        """
        Classe pour conserver les coordonnées, transaltion et zoom du rectangle
        :param scale: scale actuel de l'imag
        :param topx: coordonnée x du point en haut à gauche du rectangle
        :param topy: coordonnée y du point en haut à gauche du rectangle
        :param botx: coordonnée x du point en bas à droite du rectangle
        :param boty: coordonnée y du point en bas à droite du rectangle
        :param translation_x: translation x dans le canvas
        :param translation_y: translation y dans le canvas
        :param n_img: numero de la page
        :param id: identifiant du rectangle
        """
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

    def dimension(self) -> tuple:
        """
        retourne un les coordonnées sans le zoom et en considérant la translation
        :return: coordonnées normalisées
        """
        dimension = tuple((self.topx * (1 / self.scale), self.topy * (1 / self.scale), self.botx * (1 / self.scale),
                           self.boty * (1 / self.scale)))
        return dimension

    def get_topx(self) -> float:
        """
        :return: topx coordonnée x du point en haut à gauche du rectangle
        """
        topx = (self.topx / self.scale)
        return topx

    def get_topy(self) -> float:
        """
        :return: topy coordonnée y du point en haut à gauche du rectangle
        """
        topy = (self.topy / self.scale)
        return topy

    def get_botx(self) -> float:
        """
        :return: botx coordonnée x du point en bas à droite du rectangle
        """
        botx = (self.botx / self.scale)
        return botx

    def get_boty(self) -> float:
        """
        :return: boty coordonnée y du point en bas à droite du rectangle
        """
        boty = (self.boty / self.scale)
        return boty

    def get_nimg(self) -> int:
        """
        :return: n_img, le numero de la page du padf
        """
        return self.n_img

    def get_id(self) -> str:
        """
        :return: identifiant de la zone de détection
        """
        return self.id
