import math


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

    def __init__(self, x, y, r, a, am, aam):
        # Initialisiert die Roboterposition, Radius, Winkel und Beschleunigungsgrenzen
        self.posx = x
        self.posy = y
        self.radius = r
        self.alpha = a % 360  # Winkel wird auf 0-359 Grad begrenzt
        self.accel_max = am
        self.accel_alpha_max = aam

    def change_acceleration(self, a):
        # Ändert die Beschleunigung, begrenzt sie jedoch auf accel_max
        if abs(a) <= self.accel_max:
            self.accel = a
        else:
            if a < 0:
                self.accel = -self.accel_max
            else:
                self.accel = self.accel_max

    def change_rot_acceleration(self, aa):
        # Ändert die Rotationsbeschleunigung, begrenzt sie jedoch auf accel_alpha_max
        if abs(aa) < self.accel_alpha_max:
            self.accel_alpha = aa
        else:
            self.accel_alpha = self.accel_alpha_max

    def change_velocity(self, v):
        # Ändert die Geschwindigkeit direkt
        self.vel = v

    def change_velocity_cap(self, v):
        # Ändert die Geschwindigkeit, begrenzt sie jedoch auf +/- 5
        if abs(v) < 5:  # 5 ist ein statisches Limit; könnte in Zukunft eine Variable sein
            self.vel = v
        else:
            if v < 0:
                self.vel = -5
            else:
                self.vel = 5

    def change_turn_velocity(self, va):
        # Ändert die Drehgeschwindigkeit
        self.vel = va

    def paint_robot(self, pygame, screen):
        # Zeichnet den Roboter als blauen Kreis
        pygame.draw.circle(screen, "blue", (self.posx, self.posy), self.radius)
        # Berechnet und zeichnet eine Linie für die Orientierung des Roboters
        new_x = self.radius * (math.cos(self.alpha))
        new_y = self.radius * (math.sin(self.alpha))
        pygame.draw.line(screen, "black", (self.posx, self.posy),
                         (self.posx+new_x, self.posy+new_y))
