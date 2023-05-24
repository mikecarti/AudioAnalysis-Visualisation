import pygame


class Surface:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.last_color = None

    def get_pygame_surface(self):
        return self.surface

    def get_color_of_surface(self):
        return self.surface.get_at((self.width // 10, self.height // 10))

    def change_color(self, color: tuple) -> None:
        """
        :param color: (x,y,z) RGB
        :return: None
        """
        if self.last_color == color:
            return

        self.surface.fill(color)
        pygame.display.update()
        self.last_color = color


class Renderer:
    def __init__(self):
        pygame.init()
        width = 400
        height = 300

        screen = pygame.display.set_mode((width, height))
        self.screen = screen
        self.left_surf = Surface(width // 2, height)
        self.right_surf = Surface(width // 2, height)
        self.left_pg_surf = self.left_surf.get_pygame_surface()
        self.right_pg_surf = self.right_surf.get_pygame_surface()
        self.left_pos =(0, 0)
        self.right_pos = (width // 2, 0)

        self.update('right')
        self.update('left')

    def change_left_color(self, color):
        self.left_surf.change_color(color)
        self.update(which_one='left')

    def change_right_color(self, color):
        self.right_surf.change_color(color)
        self.update(which_one='right')

    def update(self, which_one):
        if which_one == 'left':
            self.screen.blit(self.left_pg_surf, self.left_pos)
        elif which_one == 'right':
            self.screen.blit(self.right_pg_surf, self.right_pos)
        else:
            raise Exception("Invalid specification: ", which_one)
        pygame.display.update()
