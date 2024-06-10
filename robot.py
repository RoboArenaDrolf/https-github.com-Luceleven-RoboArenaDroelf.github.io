import math
from itertools import count

player_count = 0

class Robot:
    posx: int
    posy: int
    radius = 0
    alpha = 0
    accel = 0
    accel_max = 1
    accel_alpha = 0     # this might just be useless for us
    accel_alpha_max = 1  # this feels VERY useless
    vel = 0
    vel_alpha = 0
    vertical_speed = 0  # Anfangsgeschwindigkeit in der vertikalen Richtung
    health_max: int
    health: int
    color: ""
    player_number = count(0)

    def __init__(self, x, y, r, a, am, aam, hm, c):
        self.posx = x
        self.posy = y
        self.radius = r
        self.alpha = a % 360  # thanks to mod 360 this will no longer break
        self.accel_max = am
        self.accel_alpha_max = aam
        self.health_max = hm
        self.health = self.health_max  # we start at full health
        self.color = c
        self.player_number = next(self.player_number)

    def change_acceleration(self, a):
        if abs(a) <= self.accel_max:
            self.accel = a
        else:
            if a < 0:
                self.accel = -self.accel_max
            else:
                self.accel = self.accel_max

    def change_rot_acceleration(self, aa):
        if abs(aa) < self.accel_alpha_max:
            self.accel_alpha = aa
        else:
            self.accel_alpha = self.accel_alpha_max

    def change_velocity(self, v):
        self.vel = v

    def change_velocity_cap(self, v):
        if abs(v) < 5:  # for now, I have 5 as a static cap we might want to change it to va v_max variable
            self.vel = v
        else:
            if v < 0:
                self.vel = -5
            else:
                self.vel = 5
        self.alpha = 270+(90/5)*self.vel

    def change_turn_velocity(self, va):
        self.vel = va

    def take_damage_debug(self, d):
        if d <= self.health:
            self.health = self.health-d
        else:
            self.health = 0

    def paint_robot(self, pygame, screen):
        # robot
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        new_x = self.radius * (math.cos(math.radians(self.alpha)))
        new_y = self.radius * (math.sin(math.radians(self.alpha)))
        pygame.draw.line(screen, "black", (self.posx, self.posy), (self.posx+new_x, self.posy+new_y))
        # corresponding health ui
        health_font = pygame.font.Font(None, 20)
        player_health = health_font.render(f'{self.health}', True, f'{self.color}')
        player_rect = player_health.get_rect(center=(200 + 200*self.player_number, 1000 - 100))
        pygame.draw.rect(screen, "black", player_rect.inflate(20, 20))
        screen.blit(player_health, player_rect)
