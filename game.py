import pygame
# import random
import sys
# from screeninfo import get_monitors

from robot import Robot
from movement import Movement
from arena import Arena

pygame.init()

# # Commenting these out for now, maybe introduce them later for full-screen support
# monitor = get_monitors()[0]
# windowWidth = monitor.width
# windowHeight = monitor.height

arena_size = 1000

screen = pygame.display.set_mode((arena_size, arena_size))
pygame.display.set_caption("Robo Arena")

black = (0, 0, 0)
white = (255, 255, 255)

# # Event-Timer für die Erzeugung der Quadrate
# ADD_SQUARE = pygame.USEREVENT + 1
# pygame.time.set_timer(ADD_SQUARE, 1000) # Event alle 1000 Millisekunden

# Rechtecke für die Schaltflächen "Resume" und "Quit Game"
resume_rect = pygame.Rect(0, 0, 0, 0)
quit_rect = pygame.Rect(0, 0, 0, 0)


def pause_screen():
    global resume_rect, quit_rect
    # "Paused Game" anzeigen
    font = pygame.font.Font(None, 64)
    text = font.render("Paused Game", True, black)
    screen.blit(text, (arena_size // 2 - text.get_width() // 2, arena_size // 2 - text.get_height() // 2))

    # "Resume" und "Quit Game" anzeigen
    font = pygame.font.Font(None, 36)
    text_retry = font.render("Resume", True, white)
    text_quit = font.render("Quit Game", True, white)

    # Positionen der Texte festlegen
    resume_rect = text_retry.get_rect(center=(arena_size // 2, arena_size // 2 + 50))
    quit_rect = text_quit.get_rect(center=(arena_size // 2, arena_size // 2 + 100))

    # Rechtecke zeichnen
    pygame.draw.rect(screen, black, resume_rect)
    pygame.draw.rect(screen, black, quit_rect)

    # Texte zeichnen
    screen.blit(text_retry, resume_rect)
    screen.blit(text_quit, quit_rect)

    pygame.display.update()

robot = Robot(300, 100, 25, 45)
movement = Movement()
arena = Arena("secondMap.json", pygame)

game_paused = False
run = True
while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # elif event.type == ADD_SQUARE and not game_over:
        #     # Zufällige X-Position generieren und zur Liste hinzufügen
        #     random_x_position = random.randint(0, windowWidth - square_size)
        #     black_squares.append([random_x_position, 0, 5])  # [x, y, speed]
        #     random_x_position = random.randint(0, windowWidth - square_size)
        #     white_squares.append([random_x_position, 0, 5])

        elif event.type == pygame.MOUSEBUTTONDOWN and game_paused:
            # Mausklick-Ereignis verarbeiten, wenn das Spiel vorbei ist
            mouse_pos = pygame.mouse.get_pos()
            if resume_rect.collidepoint(mouse_pos):
                # Weiter spielen
                game_paused = False
            elif quit_rect.collidepoint(mouse_pos):
                # Spiel beenden
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game_paused = True

    if not game_paused:  # Das Spiel läuft nur weiter, wenn es nicht vorbei ist
        # # Überprüfen, ob das rote Rechteck mit einem schwarzen Rechteck kollidiert
        # for square in black_squares:
        #     square[1] += square[2]  # Update y-coordinate using speed
        #     if y < square[1] + square_size and y + playerSize > square[1] and x < square[0] + square_size and x + playerSize > square[0]:
        #         game_paused = True
        # # Überprüfen, ob das rote Rechteck mit einem weißen Rechteck kollidiert
        # for square in white_squares:
        #     square[1] += square[2]  # Update y-coordinate using speed
        #     if y < square[1] + square_size and y + 50 > square[1] and x < square[0] + square_size and x + 50 > square[0]:
        #         #update des Punktecounters
        #         points = points+1
        #         #weißes Rechteck wird außerhalb des spielbereichs gepusht
        #         square[1] = square[1] + 200

        arena.paint_arena(pygame, screen)
        movement.move_robot(robot, arena_size)
        robot.paint_robot(pygame, screen)
    else:
        pause_screen()

    # # Text für den Punkte-counter
    # font = pygame.font.Font(None, 64)
    # text_points = font.render(f"Deine Punkte {points} " , True, black)
    # # Position des Counters
    # points_rect = text_points.get_rect(center=(200 , 50))
    # screen.blit(text_points, points_rect)

    pygame.display.update()

pygame.quit()
