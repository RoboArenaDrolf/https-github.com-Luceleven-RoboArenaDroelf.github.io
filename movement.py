import pygame


class Movement:
    gravity = 0.5  # Schwerkraftkonstante

    def move_robot(self, robot, screen_height, x):
        keys = pygame.key.get_pressed()
        robot.posx += x

        if keys[pygame.K_UP]:
            robot.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen

        # Vertikale Bewegung mit Schwerkraft
        robot.vertical_speed += self.gravity
        robot.posy += robot.vertical_speed

        # Grenzen für die vertikale Position (optional)
        if robot.posy > screen_height:
            robot.posy = screen_height
            robot.vertical_speed = 0
        elif robot.posy < 0:
            robot.posy = 0

    def move_bot(self, robot, screen_height, x, jump):
        robot.posx += x

        if jump:
            robot.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen

        # Vertikale Bewegung mit Schwerkraft
        robot.vertical_speed += self.gravity
        robot.posy += robot.vertical_speed

        # Grenzen für die vertikale Position (optional)
        if robot.posy > screen_height:
            robot.posy = screen_height
            robot.vertical_speed = 0
        elif robot.posy < 0:
            robot.posy = 0
