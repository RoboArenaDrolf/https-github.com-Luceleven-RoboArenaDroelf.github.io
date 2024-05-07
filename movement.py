import pygame

class Movement:
    gravity = 0.5  # Schwerkraftkonstante
    vertical_speed = 0  # Anfangsgeschwindigkeit in der vertikalen Richtung

    def move_robot(self, robot, screen_height):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            robot.posx += 5
        if keys[pygame.K_LEFT]:
            robot.posx -= 5

        if keys[pygame.K_UP]:
            self.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen
        
        # Vertikale Bewegung mit Schwerkraft
        self.vertical_speed += self.gravity
        robot.posy += self.vertical_speed

        # Grenzen für die vertikale Position (optional)
        if robot.posy > screen_height:
            robot.posy = screen_height
            self.vertical_speed = 0
        elif robot.posy < 0:
            robot.posy = 0
