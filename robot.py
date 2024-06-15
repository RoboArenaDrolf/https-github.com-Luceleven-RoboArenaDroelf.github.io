import math


class Robot:
    posx: int
    posy: int
    radius = 0
    alpha = 0
    accel = float(0)
    # accel_max = 1
    accel_alpha = float(0)  # this might just be useless for us
    # accel_alpha_max = 1  # this feels VERY useless
    vel = float(0)
    vel_alpha = float(0)
    vertical_speed = float(0)  # Anfangsgeschwindigkeit in der vertikalen Richtung
    health_max: int
    health: int
    color: str
    can_jump_again = False
    jump_counter = 0

    def __init__(self, x, y, r, a, am, aam, vm, hm, c, pn):
        self.posx = x
        self.posy = y
        self.radius = r
        self.alpha = a % 360  # thanks to mod 360 this will no longer break
        self.accel_max = am
        self.accel_alpha_max = aam
        self.vel_max = vm
        self.health_max = hm
        self.health = self.health_max  # we start at full health
        self.color = c
        self.player_number = pn

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
        if abs(v) < self.vel_max:  # for now, I have 5 as a static cap we might want to change it to va v_max variable
            self.vel = v
        else:
            if v < 0:
                self.vel = -self.vel_max
            else:
                self.vel = self.vel_max
        self.alpha = 270 + (90 / self.vel_max) * self.vel

    def change_turn_velocity(self, va):
        self.vel = va

    def attack(self, pygame, screen):
        new_x = self.radius * (math.cos(math.radians(self.alpha)))
        new_y = self.radius * (math.sin(math.radians(self.alpha)))
        pygame.draw.line(screen, "red", (self.posx, self.posy), (self.posx + new_x * 2, self.posy + new_y * 2), width=4)

    def take_damage_debug(self, d):
        if d <= self.health:
            self.health = self.health - d
        else:
            self.health = 0

    def paint_robot(self, pygame, screen):
        # robot
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        new_x = self.radius * (math.cos(math.radians(self.alpha)))
        new_y = self.radius * (math.sin(math.radians(self.alpha)))
        pygame.draw.line(screen, "black", (self.posx, self.posy), (self.posx + new_x, self.posy + new_y))
        # corresponding health ui
        health_font = pygame.font.Font(None, int(pygame.display.get_window_size()[1] / 25))
        player_health = health_font.render(f"{self.health}", True, f"{self.color}")
        player_rect = player_health.get_rect(
            center=(
                pygame.display.get_window_size()[0] / 5
                + (pygame.display.get_window_size()[0] / 5) * self.player_number,
                pygame.display.get_window_size()[1] / 20,
            )
        )
        pygame.draw.rect(
            screen,
            (0, 30, 50, 0.5),
            player_rect.inflate(pygame.display.get_window_size()[0] / 33, pygame.display.get_window_size()[1] / 50),
        )
        screen.blit(player_health, player_rect)
