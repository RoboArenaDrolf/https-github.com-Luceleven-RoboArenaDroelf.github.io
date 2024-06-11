import pygame

class Movement:
    gravity = 0.5  # Schwerkraftkonstante

    def __init__(self):
        self.can_double_jump = False
        self.jump_count = 0  # Sprungzähler initialisieren

    def move_robot(self, robot, screen_height, screen_width, x, arena):
        keys = pygame.key.get_pressed()
        robot.posx += x

        # Überprüfen, ob der Roboter die seitlichen Grenzen der Arena erreicht hat
        if robot.posx < robot.radius:
            robot.posx = robot.radius
            robot.change_velocity(0)
            robot.change_acceleration(0)
        elif robot.posx > screen_width - robot.radius:
            robot.posx = screen_width - robot.radius
            robot.change_velocity(0)
            robot.change_acceleration(0)

        # Tastatureingaben verarbeiten
        if keys[pygame.K_UP]:
            if self.on_ground(robot, arena) and self.jump_count == 0:
                robot.vertical_speed = -10  # Vertikale Geschwindigkeit für den ersten Sprung setzen
                self.can_double_jump = True  # Doppelsprung verfügbar machen
                self.jump_count = 1  # Der erste Sprung wurde ausgeführt
            elif self.can_double_jump and self.jump_count == 1:
                robot.vertical_speed = -10  # Vertikale Geschwindigkeit für den Doppelsprung setzen
                self.can_double_jump = False  # Doppelsprung wurde benutzt
                self.jump_count = 2  # Der zweite Sprung wurde ausgeführt
        
        # Vertikale Bewegung
        robot.vertical_speed += self.gravity

        # Überprüfen, ob der Roboter die oberen und unteren Grenzen der Arena erreicht hat
        if robot.posy - robot.radius < 0:
            robot.posy = robot.radius
            if robot.vertical_speed < 0:
                robot.vertical_speed = 0
        elif robot.posy + robot.radius > screen_height:
            robot.posy = screen_height - robot.radius
            if robot.vertical_speed > 0:
                robot.vertical_speed = 0
        else:
            robot.posy += robot.vertical_speed

        # Kollision mit dem Boden überprüfen
        if self.check_collision_y(robot, arena):
            robot.posy = ((robot.posy // arena.tile_size) + 1) * arena.tile_size - robot.radius
            robot.vertical_speed = 0
            self.can_double_jump = True  # Doppelsprung erlauben, wenn der Boden berührt wird
            self.jump_count = 0  # Sprungstatus zurücksetzen, wenn der Boden berührt wird

        if self.check_collision_x(robot, arena):
            robot.posx = ((robot.posx // arena.tile_size) + 1) * arena.tile_size - robot.radius
            robot.change_acceleration(0)
            robot.change_velocity(0)

        # Grenzen für die vertikale Position (optional)
        if robot.posy > screen_height:
            robot.posy = screen_height - robot.radius
            robot.vertical_speed = 0
        elif robot.posy < 0:
            robot.posy = robot.radius

    def move_bot(self, robot, screen_height, screen_width, x, arena, jump):
        robot.posx += x

        # Überprüfen, ob der Roboter die seitlichen Grenzen der Arena erreicht hat
        if robot.posx < robot.radius:
            robot.posx = robot.radius
            robot.change_velocity(0)
            robot.change_acceleration(0)
        elif robot.posx > screen_width - robot.radius:
            robot.posx = screen_width - robot.radius
            robot.change_velocity(0)
            robot.change_acceleration(0)

        # Sprung logik
        if jump:
            if self.on_ground(robot, arena) and not self.has_jumped:
                robot.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen
                self.can_double_jump = True  # Doppelsprung verfügbar machen
                self.has_jumped = False  # Spieler hat einmal gesprungen

        # Vertikale Bewegung
        robot.vertical_speed += self.gravity

        # Überprüfen, ob der Roboter die oberen und unteren Grenzen der Arena erreicht hat
        if robot.posy - robot.radius < 0:
            robot.posy = robot.radius
            if robot.vertical_speed < 0:
                robot.vertical_speed = 0
        elif robot.posy + robot.radius > screen_height:
            robot.posy = screen_height - robot.radius
            if robot.vertical_speed > 0:
                robot.vertical_speed = 0
        else:
            robot.posy += robot.vertical_speed

        # Kollision mit dem Boden überprüfen
        if self.check_collision_y(robot, arena):
            robot.posy = ((robot.posy // arena.tile_size) + 1) * arena.tile_size - robot.radius
            robot.vertical_speed = 0
            self.can_double_jump = True  # Doppelsprung erlauben, wenn der Boden berührt wird
            self.has_jumped = False  # Sprungstatus zurücksetzen, wenn der Boden berührt wird

        if self.check_collision_x(robot, arena):
            robot.posx = ((robot.posx // arena.tile_size) + 1) * arena.tile_size - robot.radius
            robot.change_acceleration(0)
            robot.change_velocity(0)

        # Grenzen für die vertikale Position (optional)
        if robot.posy > screen_height:
            robot.posy = screen_height - robot.radius
            robot.vertical_speed = 0
        elif robot.posy < 0:
            robot.posy = robot.radius

    def on_ground(self, robot, arena):
        # Überprüfen, ob der Roboter auf dem Boden steht
        x_positions = (round((robot.posx + robot.radius) // arena.tile_size),
                       round((robot.posx - robot.radius) // arena.tile_size), round(robot.posx // arena.tile_size))
        y_positions = (round((robot.posy + robot.radius) // arena.tile_size),
                       round((robot.posy - robot.radius) // arena.tile_size), round(robot.posy // arena.tile_size))
        return arena.is_solid(x_positions, y_positions)

    def check_collision_y(self, robot, arena):
        # Überprüfen, ob der Roboter mit einem festen Tile kollidiert auf y-Achse
        x_positions = [(round(robot.posx // arena.tile_size))]
        y_positions = [round((robot.posy + robot.radius) // arena.tile_size),
                       round((robot.posy - robot.radius) // arena.tile_size), round(robot.posy // arena.tile_size)]
        return arena.is_solid(x_positions, y_positions)

    def check_collision_x(self, robot, arena):
        # Überprüfen, ob der Roboter mit einem festen Tile kollidiert auf x-Achse
        x_positions = [round((robot.posx + robot.radius) // arena.tile_size),
                       round((robot.posx - robot.radius) // arena.tile_size), round(robot.posx // arena.tile_size)]
        y_positions = [(round(robot.posy // arena.tile_size))]
        return arena.is_solid(x_positions, y_positions)
