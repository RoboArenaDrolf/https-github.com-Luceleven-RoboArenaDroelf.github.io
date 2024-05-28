import pygame

class Movement:
    gravity = 0.5  # Schwerkraftkonstante
    vertical_speed = 0  # Anfangsgeschwindigkeit in der vertikalen Richtung

    def move_robot(self, robot, screen_height, screen_width, x, arena):
        keys = pygame.key.get_pressed()
        robot.posx += x

        # Überprüfen, ob der Roboter die seitlichen Grenzen der Arena erreicht hat
        if robot.posx < robot.radius:
            robot.posx = robot.radius
        elif robot.posx > screen_width - robot.radius:
            robot.posx = screen_width - robot.radius

        # Tastatureingaben verarbeiten
        if keys[pygame.K_UP] and self.on_ground(robot, arena):
            self.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen

        # Vertikale Bewegung
        self.vertical_speed += self.gravity

        # Überprüfen, ob der Roboter die oberen und unteren Grenzen der Arena erreicht hat
        if robot.posy - robot.radius < 0:
            robot.posy = robot.radius
            if self.vertical_speed < 0:
                self.vertical_speed = 0
        elif robot.posy + robot.radius > screen_height:
            robot.posy = screen_height - robot.radius
            if self.vertical_speed > 0:
                self.vertical_speed = 0
        else:
            robot.posy += self.vertical_speed

        # Kollision mit dem Boden überprüfen
        if self.check_collision(robot, arena):
            robot.posy = ((robot.posy // arena.tile_size) + 1) * arena.tile_size - robot.radius
            self.vertical_speed = 0

        # Grenzen für die vertikale Position (optional)
        if robot.posy > screen_height:
            robot.posy = screen_height
            self.vertical_speed = 0
        elif robot.posy < 0:
            robot.posy = 0


    def on_ground(self, robot, arena):
        # Überprüfen, ob der Roboter auf dem Boden steht
        x = int(robot.posx // arena.tile_size)
        y = int((robot.posy + robot.radius) // arena.tile_size)
        return arena.is_solid(x, y) or self.vertical_speed > 0


    def check_collision(self, robot, arena):
        # Überprüfen, ob der Roboter mit einem festen Tile kollidiert
        x = int(robot.posx // arena.tile_size)
        y = int((robot.posy + robot.radius) // arena.tile_size)
        return arena.is_solid(x, y)
