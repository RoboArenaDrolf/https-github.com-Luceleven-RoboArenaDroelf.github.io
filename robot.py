import math


class Robot:
    posx: int
    posy: int
    radius = 0
    alpha = 0  # must be between 0 and 360

    def __int__(self, x, y, r, a):
        self.posx = x
        self.posy = y
        self.radius = r
        self.alpha = a

    def paint_robot(self, pygame, screen):
        pygame.draw.circle(screen, "blue", (self.posx, self.posy), self.radius)  # draws the circle

        # now to get the orientation
        new_x = self.radius*math.cos(self.alpha)
        new_y = self.radius*math.sin(self.alpha)
        pygame.draw.line(screen, "black", (self.posx, self.posy), (new_x, new_y))  # draws the line



