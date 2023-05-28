import pygame as pg


class StickRenderer:
    def __init__(self, number_of_windows):
        pg.init()
        self.number_of_windows = number_of_windows
        self.global_width = 300 * number_of_windows
        self.global_height = 300
        self.window_width = 300
        self.window_height = 300

        self.surfaces = self.create_surfaces()
        self.screen_color = (0, 0, 0)
        self.line_color = (255, 0, 255)

    def set_stick_levels(self, left_level: float, right_level: float, window_number: int):
        """
        :param left_level: Normalized value of left stick
        :param right_level: Normalized value of right stick
        :return:
        """

        y1 = (1 - left_level) * self.window_height
        y2 = (1 - right_level) * self.window_height
        left_end = (0, y1)
        right_end = (self.window_height, y2)

        self.draw_line(left_end, right_end, window_number)

    def draw_line(self, left_end: tuple, right_end: tuple, window_number):
        surface = self.surfaces[window_number]
        surface.fill(self.screen_color)
        pg.draw.line(surface, color=self.line_color, start_pos=left_end, end_pos=right_end, width=7)
        self.screen.blit(surface, (self.window_width * window_number, 0))


    def update(self):
        pg.display.update()

    def create_surfaces(self):
        self.screen = pg.display.set_mode((self.global_width, self.global_height))

        surfaces = []
        for i in range(self.number_of_windows):
            surface = pg.Surface((self.window_width, self.window_height))
            surfaces.append(surface)
            self.screen.blit(surface, (self.window_width * i, 0))
        pg.display.flip()
        return surfaces
