

class Projectile:
    x: int
    y: int
    radius: int
    color: str
    x_speed: int
    y_speed: int
    # type: str
    player_number:int

    def __init__(self, x, y, c, r, xs, ys, pn):
        self.x = x
        self.y = y
        self.color = c
        self.radius = r
        self.x_speed = xs
        self.y_speed = ys
        self.player_number = pn
        # self.type = t

    def move_projectile(self):
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed

    def paint_projectile(self, pygame, screen):
        # if self.type == "small":
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # if self.type == "big":
