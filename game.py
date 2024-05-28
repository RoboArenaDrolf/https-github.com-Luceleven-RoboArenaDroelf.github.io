import pygame
import sys

from robot import Robot
from movement import Movement
from arena import Arena

pygame.init()

arena_size = 1000

screen = pygame.display.set_mode((arena_size, arena_size))
pygame.display.set_caption("Robo Arena")

black = (0, 0, 0)
white = (255, 255, 255)

resume_rect = pygame.Rect(0, 0, 0, 0)
quit_rect = pygame.Rect(0, 0, 0, 0)


def pause_screen():
    global resume_rect, quit_rect
    font = pygame.font.Font(None, 64)
    text = font.render("Paused Game", True, black)
    screen.blit(text, (arena_size // 2 - text.get_width() // 2, arena_size // 2 - text.get_height() // 2))

    font = pygame.font.Font(None, 36)
    text_retry = font.render("Resume", True, white)
    text_quit = font.render("Quit Game", True, white)

    resume_rect = text_retry.get_rect(center=(arena_size // 2, arena_size // 2 + 50))
    quit_rect = text_quit.get_rect(center=(arena_size // 2, arena_size // 2 + 100))

    pygame.draw.rect(screen, black, resume_rect)
    pygame.draw.rect(screen, black, quit_rect)

    screen.blit(text_retry, resume_rect)
    screen.blit(text_quit, quit_rect)

    pygame.display.update()


robot = Robot(300, 100, 25, 45, 1, 1)
movement = Movement()
arena = Arena("secondMap.json", pygame)

game_paused = False
run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_paused:
            mouse_pos = pygame.mouse.get_pos()
            if resume_rect.collidepoint(mouse_pos):
                game_paused = False
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game_paused = True

    if not game_paused:
        screen.fill(white)
        arena.paint_arena(pygame, screen)
        if keys[pygame.K_RIGHT]:
            robot.change_acceleration(robot.accel + 0.05)
        elif keys[pygame.K_LEFT]:
            robot.change_acceleration(robot.accel - 0.05)
        else:
            if robot.vel < 0:
                robot.change_acceleration(robot.accel + 0.025)
                if robot.vel + robot.accel >= 0:
                    robot.change_velocity_cap(0)
                    robot.change_acceleration(0)
            elif robot.vel > 0:
                robot.change_acceleration(robot.accel - 0.025)
                if robot.vel + robot.accel <= 0:
                    robot.change_velocity_cap(0)
                    robot.change_acceleration(0)
            else:
                robot.change_acceleration(0)

        robot.change_velocity_cap(robot.vel + robot.accel)

        movement.move_robot(robot, arena_size, arena_size, robot.vel, arena)  # Hier wurde das Argument screen_width hinzugefügt
        robot.paint_robot(pygame, screen)
    else:
        pause_screen()

    pygame.display.update()


pygame.quit()

