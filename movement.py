import pygame


class Movement:
    gravity = 0.5  # Schwerkraftkonstante

    def move_robot(self, robot, screen_height, screen_width, x, arena):
        keys = pygame.key.get_pressed()
        robot.posx += x

        # Überprüfen, ob der Roboter die seitlichen Grenzen der Arena erreicht hat
        if robot.posx < robot.radius + arena.x_offset:
            robot.posx = robot.radius + arena.x_offset
            robot.change_velocity(0)
            robot.change_acceleration(0)
        elif robot.posx > screen_width - robot.radius - arena.x_offset:
            robot.posx = screen_width - robot.radius - arena.x_offset
            robot.change_velocity(0)
            robot.change_acceleration(0)

        # Tastatureingaben verarbeiten
        if keys[pygame.K_UP] and self.on_ground(robot, arena):
            robot.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen

        # Vertikale Bewegung
        robot.vertical_speed += self.gravity

        # Überprüfen, ob der Roboter die oberen und unteren Grenzen der Arena erreicht hat
        if robot.posy - robot.radius < arena.y_offset:
            robot.posy = robot.radius + arena.y_offset
            if robot.vertical_speed < 0:
                robot.vertical_speed = 0
        elif robot.posy + robot.radius > screen_height - arena.y_offset:
            robot.posy = screen_height - robot.radius - arena.y_offset
            if robot.vertical_speed > 0:
                robot.vertical_speed = 0
        else:
            robot.posy += robot.vertical_speed

        # Kollision mit dem Boden überprüfen
        if self.check_collision_y(robot, arena):
            robot.posy = ((robot.posy // arena.tile_size) + 1) * arena.tile_size - robot.radius
            robot.vertical_speed = 0

        if self.check_collision_x(robot, arena):
            robot.posx = ((robot.posx // arena.tile_size) + 1) * arena.tile_size - robot.radius
            robot.change_acceleration(0)
            robot.change_velocity(0)

    def move_bot(self, robot, screen_height, screen_width, x, arena, jump):
        robot.posx += x

        # Überprüfen, ob der Roboter die seitlichen Grenzen der Arena erreicht hat
        if robot.posx < robot.radius + arena.x_offset:
            robot.posx = robot.radius + arena.x_offset
            robot.change_velocity(0)
            robot.change_acceleration(0)
        elif robot.posx > screen_width - robot.radius - arena.x_offset:
            robot.posx = screen_width - robot.radius - arena.x_offset
            robot.change_velocity(0)
            robot.change_acceleration(0)

        # Tastatureingaben verarbeiten
        if jump and self.on_ground(robot, arena):
            robot.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen

        # Vertikale Bewegung
        robot.vertical_speed += self.gravity

        # Überprüfen, ob der Roboter die oberen und unteren Grenzen der Arena erreicht hat
        if robot.posy - robot.radius < arena.y_offset:
            robot.posy = robot.radius + arena.y_offset
            if robot.vertical_speed < 0:
                robot.vertical_speed = 0
        elif robot.posy + robot.radius > screen_height - arena.y_offset:
            robot.posy = screen_height - robot.radius - arena.y_offset
            if robot.vertical_speed > 0:
                robot.vertical_speed = 0
        else:
            robot.posy += robot.vertical_speed

        # Kollision mit dem Boden überprüfen
        if self.check_collision_y(robot, arena):
            robot.posy = (
                (((robot.posy - arena.y_offset) // arena.tile_size) + 1) * arena.tile_size
                - robot.radius
                + arena.y_offset
            )
            robot.vertical_speed = 0

        if self.check_collision_x(robot, arena):
            robot.posx = (
                (((robot.posx - arena.x_offset) // arena.tile_size) + 1) * arena.tile_size
                - robot.radius
                + arena.x_offset
            )
            robot.change_acceleration(0)
            robot.change_velocity(0)

    def on_ground(self, robot, arena):
        # Überprüfen, ob der Roboter auf dem Boden steht
        x_positions = (
            round((robot.posx + robot.radius - arena.x_offset) // arena.tile_size),
            round((robot.posx - robot.radius - arena.x_offset) // arena.tile_size),
            round((robot.posx - arena.x_offset) // arena.tile_size),
        )
        y_positions = (
            round((robot.posy + robot.radius - arena.y_offset) // arena.tile_size),
            round((robot.posy - robot.radius - arena.y_offset) // arena.tile_size),
            round((robot.posy - arena.y_offset) // arena.tile_size),
        )
        return arena.is_solid(x_positions, y_positions) or robot.vertical_speed > 0

    def check_collision_y(self, robot, arena):
        # Überprüfen, ob der Roboter mit einem festen Tile kollidiert auf y-Achse
        x_positions = [(round((robot.posx - arena.x_offset) // arena.tile_size))]
        y_positions = [
            round((robot.posy + robot.radius - arena.y_offset) // arena.tile_size),
            round((robot.posy - robot.radius - arena.y_offset) // arena.tile_size),
            round((robot.posy - arena.y_offset) // arena.tile_size),
        ]
        return arena.is_solid(x_positions, y_positions)

    def check_collision_x(self, robot, arena):
        # Überprüfen, ob der Roboter mit einem festen Tile kollidiert auf x-Achse
        x_positions = [
            round((robot.posx + robot.radius - arena.x_offset) // arena.tile_size),
            round((robot.posx - robot.radius - arena.x_offset) // arena.tile_size),
            round((robot.posx - arena.x_offset) // arena.tile_size),
        ]
        y_positions = [(round((robot.posy - arena.y_offset) // arena.tile_size))]
        return arena.is_solid(x_positions, y_positions)
