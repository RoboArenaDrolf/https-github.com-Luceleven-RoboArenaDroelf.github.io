import math


class Robot:
    posx: int
    posy: int
    radius = 0
    alpha = 0

    def __init__(self, x, y, r, a):
        self.posx = x
        self.posy = y
        self.radius = r
        self.alpha = a % 360  # thanks to mod 360 this will no longer break

    def paint_robot(self, pygame, screen):
        pygame.draw.circle(screen, "blue", (self.posx, self.posy), self.radius)
        # now to get the orientation
        new_x = self.radius * (math.cos(self.alpha))
        new_y = self.radius * (math.sin(self.alpha))
        pygame.draw.line(screen, "black", (self.posx, self.posy),
                         (self.posx+new_x, self.posy+new_y))
