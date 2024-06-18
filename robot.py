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
    recoil_percent = 0.1
    hit_cooldown = 0

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

    def take_damage_debug(self, d):
        if d <= self.health:
            self.health = self.health - d
        else:
            self.health = 0

    def attack(self, pygame, screen, robots, arena, movement):
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
                if robots[i].hit_cooldown <= 0:
                    robots[i].hit_cooldown = 20 # setting this so the robot doesn't get launched into space
                    # cause recoil
                    robots[i].vertical_speed +=  -arena.map_size[1] / 40 * robots[i].recoil_percent # recoil up
                    # check if we face left, right or upwards
                    if self.alpha > 315: # facing right
                        robots[i].change_acceleration(
                            robots[i].accel + (arena.map_size[0] / 40) * robots[i].recoil_percent)
                    elif self.alpha < 225: # facing left
                        robots[i].change_acceleration(
                            robots[i].accel - (arena.map_size[0] / 40) * robots[i].recoil_percent)
                    else: # facing upwards
                        robots[i].vertical_speed += -arena.map_size[1] / 100 * robots[i].recoil_percent  # recoil up again

                    #robots[i].change_velocity_cap(robots[i].vel + robots[i].accel)
                    #display_resolution = pygame.display.get_window_size()
                    #movement.move_robot(robots[i], display_resolution[1], display_resolution[0], robots[i].vel, arena)
                    robots[i].recoil_percent += 0.05

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

    def decrease_hit_cooldown(self):
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

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
