

class Projectile:
    x: int
    y: int
    radius: int
    color: str
    x_speed: int
    y_speed: int
    # type: str

    def __init__(self, x, y, c, r, xs, ys):
        self.x = x
        self.y = y
        self.color = c
        self.radius = r
        self.x_speed = xs
        self.y_speed = ys
        # self.type = t

    def paint_projectile(self, pygame, screen):
        # if self.type == "small":
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # if self.type == "big":
