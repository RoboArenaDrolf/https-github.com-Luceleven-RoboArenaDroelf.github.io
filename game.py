import random

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
    text_resume = font.render("Resume", True, white)
    text_quit = font.render("Quit Game", True, white)


    resume_rect = text_resume.get_rect(center=(arena_size // 2, arena_size // 2 + 50))
    quit_rect = text_quit.get_rect(center=(arena_size // 2, arena_size // 2 + 100))

    pygame.draw.rect(screen, black, resume_rect)
    pygame.draw.rect(screen, black, quit_rect)


    screen.blit(text_resume, resume_rect)
    screen.blit(text_quit, quit_rect)

    pygame.display.update()

def start_screen():
    global one_player_rect, two_player_rect, three_player_rect, four_player_rect
    screen.fill(white)

    font = pygame.font.Font(None, 64)
    text = font.render("Wie viele Spieler?", True, black)
    screen.blit(text, (arena_size // 2 - text.get_width() // 2, arena_size // 2 - text.get_height() // 2 - 100))

    font = pygame.font.Font(None, 36)
    one_player = font.render("1", True, white)
    two_player = font.render("2", True, white)
    three_player = font.render("3", True, white)
    four_player = font.render("4", True, white)

    one_player_rect = one_player.get_rect(center=(arena_size // 2, arena_size // 2 + 50))
    two_player_rect = two_player.get_rect(center=(arena_size // 2, arena_size // 2 + 100))
    three_player_rect = three_player.get_rect(center=(arena_size // 2, arena_size // 2 + 150))
    four_player_rect = four_player.get_rect(center=(arena_size // 2, arena_size // 2 + 200))

    pygame.draw.rect(screen, black, one_player_rect.inflate(20, 20))
    pygame.draw.rect(screen, black, two_player_rect.inflate(20, 20))
    pygame.draw.rect(screen, black, three_player_rect.inflate(20, 20))
    pygame.draw.rect(screen, black, four_player_rect.inflate(20, 20))

    screen.blit(one_player, one_player_rect)
    screen.blit(two_player, two_player_rect)
    screen.blit(three_player, three_player_rect)
    screen.blit(four_player, four_player_rect)

    pygame.display.update()

movement = Movement()
arena = Arena("secondMap.json", pygame)

game_paused = False
run = True
start_game = True
player_count = 0
robots = []

# Zähler für die Anzahl der Frames, bevor die Richtung des Roboters geändert wird
change_direction_interval = 40  # Ändere die Richtung alle 40 Frames
frame_count = 0

jump = []

clock = pygame.time.Clock()
while run:
    pygame.time.delay(10)
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if start_game:
            start_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if one_player_rect.collidepoint(mouse_pos):
                    player_count = 1
                    robots = [Robot(100, arena_size - 100, 25, 45, 1, 1)]
                    start_game = False
                elif two_player_rect.collidepoint(mouse_pos):
                    player_count = 2
                    robots = [Robot(100, arena_size - 100, 25, 45, 1, 1), Robot(200, arena_size - 100, 25, 45, 1, 1)]
                    jump = [False]
                    start_game = False
                elif three_player_rect.collidepoint(mouse_pos):
                    player_count = 3
                    robots = [Robot(100, arena_size - 100, 25, 45, 1, 1), Robot(200, arena_size - 100, 25, 45, 1, 1), Robot(300, arena_size - 100, 25, 45, 1, 1)]
                    jump = [False, False]
                    start_game = False
                elif four_player_rect.collidepoint(mouse_pos):
                    player_count = 4
                    robots = [Robot(100, arena_size - 100, 25, 45, 1, 1), Robot(200, arena_size - 100, 25, 45, 1, 1), Robot(300, arena_size - 100, 25, 45, 1, 1), Robot(400, arena_size - 100, 25, 45, 1, 1)]
                    jump = [False, False, False]
                    start_game = False
                if robots:
                    min_x = robots[0].radius
                    max_x = arena_size - robots[0].radius
                    min_y = robots[0].radius
                    max_y = arena_size - robots[0].radius
                    
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
        
    if not game_paused and not start_game:
        screen.fill(white)
        frame_count += 1
        arena.paint_arena(pygame, screen)
        player_robot = robots[0]
        if keys[pygame.K_RIGHT]:
            player_robot.change_acceleration(player_robot.accel + 0.05)
        elif keys[pygame.K_LEFT]:
            player_robot.change_acceleration(player_robot.accel - 0.05)
        else:
            if player_robot.vel < 0:
                player_robot.change_acceleration(player_robot.accel + 0.025)
                if player_robot.vel + player_robot.accel >= 0:
                    player_robot.change_velocity_cap(0)
                    player_robot.change_acceleration(0)
            elif player_robot.vel > 0:
                player_robot.change_acceleration(player_robot.accel - 0.025)
                if player_robot.vel + player_robot.accel <= 0:
                    player_robot.change_velocity_cap(0)
                    player_robot.change_acceleration(0)
            else:
                player_robot.change_acceleration(0)

        if frame_count >= change_direction_interval:
            for i in range(1, len(robots)):
                # Zufällige Änderungen der Beschleunigung und der Drehgeschwindigkeit
                robots[i].change_acceleration(random.uniform(-1, 1))
                robots[i].change_turn_velocity(random.uniform(-0.1, 0.1))
                # Setze den Zähler zurück
                frame_count = 0
                jump[i-1] = random.choice([True, False])

        for i in range(1, len(robots)):
            # Bewegung des Roboters
            movement.move_bot(robots[i], arena_size, arena_size, robots[i].vel, arena, jump[i-1])
            robots[i].change_velocity_cap(robots[i].vel + robots[i].accel)
            jump[i-1] = False

            # Überprüfe die Grenzen und passe die Position an, wenn nötig
            robots[i].posx = max(min(robots[i].posx, max_x), min_x)
            robots[i].posy = max(min(robots[i].posy, max_y), min_y)
            robots[i].paint_robot(pygame, screen)

        player_robot.change_velocity_cap(player_robot.vel + player_robot.accel)
        movement.move_robot(player_robot, arena_size, arena_size, player_robot.vel, arena)
        player_robot.paint_robot(pygame, screen)
    elif game_paused:
        pause_screen()

    pygame.display.update()


pygame.quit()

