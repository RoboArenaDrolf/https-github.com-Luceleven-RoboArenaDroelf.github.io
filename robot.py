import math

from projectiles import Projectile


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
    projectiles = []

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

    def change_alpha(self, a):
        self.alpha = a

    def change_velocity_cap(self, v):
        if abs(v) < self.vel_max:  # for now, I have 5 as a static cap we might want to change it to va v_max variable
            self.vel = v
        else:
            if v < 0:
                self.vel = -self.vel_max
            else:
                self.vel = self.vel_max
        # self.alpha = 270 + (90 / self.vel_max) * self.vel

    def change_turn_velocity(self, va):
        self.vel = va

    def take_damage_debug(self, d):
        if d <= self.health:
            self.health = self.health - d
        else:
            self.health = 0

    def melee_attack(self, pygame, screen, robots):
        new_x = self.radius * (math.cos(math.radians(self.alpha)))
        new_y = self.radius * (math.sin(math.radians(self.alpha)))
        line_start = (self.posx + new_x, self.posy + new_y)
        line_end = (self.posx + new_x * 2, self.posy + new_y * 2)
        pygame.draw.line(screen, "red", line_start, line_end, width=4)

        for i in range(1, len(robots)):
            # now I will use https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line:
            # Line defined by two points
            if (self.distance_from_segment(line_start[0], line_start[1], line_end[0], line_end[1],
                                           robots[i].posx, robots[i].posy)
                    <= robots[i].radius):  # if the distance from this line to the center of a robot
                # is smaller than it's radius, we have a hit and that robot takes some damage
                # print(i, "hit")
                robots[i].take_damage_debug(1)

    def distance_from_segment(self, x1, y1, x2, y2, x3, y3):
        # Vektoren berechnen
        px, py = x2 - x1, y2 - y1
        norm = px * px + py * py

        # Punkt auf die Linie projizieren
        u = ((x3 - x1) * px + (y3 - y1) * py) / norm

        # Überprüfen, ob die Projektion innerhalb der Strecke liegt
        if u < 0:
            # Nächster Punkt ist P1
            closest_x, closest_y = x1, y1
        elif u > 1:
            # Nächster Punkt ist P2
            closest_x, closest_y = x2, y2
        else:
            # Projektion auf die Strecke
            closest_x = x1 + u * px
            closest_y = y1 + u * py

        # Abstand zwischen P3 und dem nächstgelegenen Punkt berechnen
        dx, dy = x3 - closest_x, y3 - closest_y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance

    def ranged_attack(self):
        r = self.radius/4
        if self.alpha == 0:  # right
            xs = self.vel_max
            ys = 0
            x = self.posx + self.radius + r
            y = self.posy
        elif self.alpha == 90:  # down
            xs = 0
            ys = self.vel_max
            x = self.posx
            y = self.posy + self.radius + r
        elif self.alpha == 180:  # left
            xs = -self.vel_max
            ys = 0
            x = self.posx - self.radius - r
            y = self.posy
        elif self.alpha == 270:  # up
            xs = 0
            ys = -self.vel_max
            x = self.posx
            y = self.posy - self.radius - r
        else:  # failsafe
            print(f"how did you do this?, alpha=", self.alpha)
        c = "black"
        self.projectiles.append(Projectile(x, y, c, r, xs, ys))

    def ranged_hit_reg(self, robots):
        for i in range(0, len(robots)):
            to_delete = []
            if i != self.player_number:
                for j in range(0, len(self.projectiles)):
                    distance = abs(robots[i].posx-self.projectiles[j].x)+abs(robots[i].posy-self.projectiles[j].y)
                    if distance < (robots[i].radius + self.projectiles[j].radius):
                        robots[i].take_damage_debug(1)
                        print("hit", i, self.player_number, "robot(x,y,r)", robots[i].posx, robots[i].posy, robots[i].radius,
                              "projectile(x,y,r)", self.projectiles[j].x, self.projectiles[j].y, self.projectiles[j].radius)
                        # self.projectiles.pop(j)  # delete the projectile that hit a robot
                        # DO NOT REMOVE IT INSIDE THE LOOP instead
                        to_delete.append(j)  # save the index (might be multiple)
                to_delete = reversed(to_delete)
                for n in to_delete:  # after the j loop we delete them from back to front
                    self.projectiles.pop(n)


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
        # projectiles
        for i in self.projectiles:
            i.paint_projectile(pygame, screen)
            i.move_projectile()
