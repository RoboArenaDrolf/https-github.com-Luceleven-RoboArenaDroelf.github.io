import pygame
import Robot

class Movement: 
    gravity = 0.5  # Schwerkraftkonstante
    vertical_speed = 0  # Anfangsgeschwindigkeit in der vertikalen Richtung

    @staticmethod
    def move_robot(screen_height):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            Robot.posx += 5
        if keys[pygame.K_LEFT]:
            Robot.posx -= 5
        
        # Vertikale Bewegung mit Schwerkraft
        Movement.vertical_speed += Movement.gravity
        Robot.posy += Movement.vertical_speed
        
        if keys[pygame.K_UP]:
            Movement.vertical_speed = -10  # Vertikale Geschwindigkeit für Sprung setzen

        # Grenzen für die vertikale Position (optional)
        if Robot.posy > screen_height:
            Robot.posy = screen_height
            Movement.vertical_speed = 0
        elif Robot.posy < 0:
            Robot.posy = 0
