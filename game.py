import random

import pygame
import sys

from robot import Robot
from movement import Movement
from arena import Arena
from arenaBuilder import ArenaBuilder

pygame.init()

display_resolution = (720, 720)

screen = pygame.display.set_mode(display_resolution)
pygame.display.set_caption("Robo Arena")

black = (0, 0, 0)
white = (255, 255, 255)

resume_rect = pygame.Rect(0, 0, 0, 0)
quit_rect = pygame.Rect(0, 0, 0, 0)

dist_between_elements = display_resolution[1] / 20
robot_radius = min(display_resolution) / 40
input_fields_x_size = display_resolution[0] / 12
input_fields_y_size = display_resolution[1] / 33
input_text_offset_x = display_resolution[0] / 200
input_text_offset_y = display_resolution[1] / 200
rect_inflate_x = display_resolution[0] / 50
rect_inflate_y = display_resolution[1] / 50
font_size_big = int(display_resolution[1] / 16)
font_size_small = int(display_resolution[1] / 25)
robot_spawn_distance = display_resolution[0] / 10


def pause_screen():
    global resume_rect, quit_rect, main_menu_rect
    font = pygame.font.Font(None, font_size_big)
    text = font.render("Paused Game", True, black)
    screen.blit(
        text, (display_resolution[0] // 2 - text.get_width() // 2, display_resolution[1] // 2 - text.get_height() // 2)
    )

    font = pygame.font.Font(None, font_size_small)
    text_resume = font.render("Resume", True, white)
    text_main_menu = font.render("Main Menu", True, white)
    text_quit = font.render("Quit Game", True, white)

    resume_rect = text_resume.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + dist_between_elements)
    )
    main_menu_rect = text_main_menu.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 2 * dist_between_elements)
    )
    quit_rect = text_quit.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 3 * dist_between_elements)
    )

    pygame.draw.rect(screen, black, resume_rect)
    pygame.draw.rect(screen, black, main_menu_rect)
    pygame.draw.rect(screen, black, quit_rect)

    screen.blit(text_resume, resume_rect)
    screen.blit(text_main_menu, main_menu_rect)
    screen.blit(text_quit, quit_rect)

def main_menu():
    global play_rect, build_arena_rect, exit_rect
    screen.fill(white)

    font = pygame.font.Font(None, font_size_small)
    play_text = font.render("Play", True, white)
    build_arena_text = font.render("Build Arena", True, white)
    exit_text = font.render("Exit", True, white)

    play_rect = play_text.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + dist_between_elements)
    )
    build_arena_rect = build_arena_text.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 2 * dist_between_elements)
    )
    exit_rect = exit_text.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 3 * dist_between_elements)
    )

    pygame.draw.rect(screen, black, play_rect.inflate(rect_inflate_x, rect_inflate_y))
    pygame.draw.rect(screen, black, build_arena_rect.inflate(rect_inflate_x, rect_inflate_y))
    pygame.draw.rect(screen, black, exit_rect.inflate(rect_inflate_x, rect_inflate_y))

    screen.blit(play_text, play_rect)
    screen.blit(build_arena_text, build_arena_rect)
    screen.blit(exit_text, exit_rect)

def build_arena_menu():
    global input_rect_x_tiles, input_rect_y_tiles, start_building_rect
    screen.fill(white)

    font = pygame.font.Font(None, font_size_big)
    text = font.render("Number x tiles:", True, black)
    screen.blit(
        text,
        (
            display_resolution[0] // 2 - text.get_width() // 2,
            display_resolution[1] // 2 - text.get_height() // 2 - 2 * dist_between_elements,
        ),
    )

    # Set up text input field for number x tiles
    input_rect_x_tiles = pygame.Rect(
        display_resolution[0] // 2 - text.get_width() // 2,
        display_resolution[1] // 2 - text.get_height() // 2 - dist_between_elements,
        input_fields_x_size,
        input_fields_y_size,
    )

    pygame.draw.rect(screen, black, input_rect_x_tiles)
    text_surface = pygame.font.SysFont(None, 24).render(x_tiles, True, white)
    screen.blit(text_surface, (input_rect_x_tiles.x + input_text_offset_x, input_rect_x_tiles.y + input_text_offset_y))

    font = pygame.font.Font(None, font_size_big)
    text = font.render("Number y tiles:", True, black)
    screen.blit(
        text, (display_resolution[0] // 2 - text.get_width() // 2, display_resolution[1] // 2 - text.get_height() // 2)
    )

    # Set up text input field for number y tiles
    input_rect_y_tiles = pygame.Rect(
        display_resolution[0] // 2 - text.get_width() // 2,
        display_resolution[1] // 2 - text.get_height() // 2 + dist_between_elements,
        input_fields_x_size,
        input_fields_y_size,
    )

    pygame.draw.rect(screen, black, input_rect_y_tiles)
    text_surface = pygame.font.SysFont(None, 24).render(y_tiles, True, white)
    screen.blit(text_surface, (input_rect_y_tiles.x + input_text_offset_x, input_rect_y_tiles.y + input_text_offset_y))

    font = pygame.font.Font(None, font_size_small)
    start_building_text = font.render("Start Building", True, white)

    start_building_rect = start_building_text.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 3 * dist_between_elements)
    )

    pygame.draw.rect(screen, black, start_building_rect.inflate(rect_inflate_x, rect_inflate_y))

    screen.blit(start_building_text, start_building_rect)

def start_screen():
    global one_player_rect, two_player_rect, three_player_rect, four_player_rect
    screen.fill(white)

    font = pygame.font.Font(None, font_size_big)
    text = font.render("Wie viele Spieler?", True, black)
    screen.blit(
        text,
        (
            display_resolution[0] // 2 - text.get_width() // 2,
            display_resolution[1] // 2 - text.get_height() // 2 - 2 * dist_between_elements,
        ),
    )

    font = pygame.font.Font(None, font_size_small)
    one_player = font.render("1", True, white)
    two_player = font.render("2", True, white)
    three_player = font.render("3", True, white)
    four_player = font.render("4", True, white)

    one_player_rect = one_player.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + dist_between_elements)
    )
    two_player_rect = two_player.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 2 * dist_between_elements)
    )
    three_player_rect = three_player.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 3 * dist_between_elements)
    )
    four_player_rect = four_player.get_rect(
        center=(display_resolution[0] // 2, display_resolution[1] // 2 + 4 * dist_between_elements)
    )

    pygame.draw.rect(screen, black, one_player_rect.inflate(rect_inflate_x, rect_inflate_y))
    pygame.draw.rect(screen, black, two_player_rect.inflate(rect_inflate_x, rect_inflate_y))
    pygame.draw.rect(screen, black, three_player_rect.inflate(rect_inflate_x, rect_inflate_y))
    pygame.draw.rect(screen, black, four_player_rect.inflate(rect_inflate_x, rect_inflate_y))

    screen.blit(one_player, one_player_rect)
    screen.blit(two_player, two_player_rect)
    screen.blit(three_player, three_player_rect)
    screen.blit(four_player, four_player_rect)


movement = Movement()
arena = Arena("secondMap.json", pygame)

game_paused = False
run = True
start_game = False
menu = True
build_arena = False
player_count = 0
robots = []

input_active_x = False
input_active_y = False
x_tiles = ""
y_tiles = ""

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
        if menu:
            main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    start_game = True
                    menu = False
                elif build_arena_rect.collidepoint(mouse_pos):
                    build_arena = True
                    menu = False
                elif exit_rect.collidepoint(mouse_pos):
                    run = False
        elif build_arena:
            build_arena_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if input_rect_x_tiles.collidepoint(mouse_pos):
                    input_active_x = True
                    input_active_y = False
                elif input_rect_y_tiles.collidepoint(mouse_pos):
                    input_active_y = True
                    input_active_x = False
                elif start_building_rect.collidepoint(mouse_pos):
                    try:
                        num_x = int(x_tiles)
                        num_y = int(y_tiles)
                        if num_x <= 0 or num_y <= 0:
                            raise ValueError
                        build_arena = False
                        menu = True
                        arenaBuilder = ArenaBuilder(num_x, num_y, pygame)
                        arenaBuilder.main()
                        screen = pygame.display.set_mode(display_resolution)
                    except ValueError:
                        print("There should only be positive numbers in the fields!")
            elif event.type == pygame.KEYDOWN:
                if input_active_x:
                    if event.key == pygame.K_BACKSPACE:
                        x_tiles = x_tiles[:-1]
                    else:
                        x_tiles += event.unicode
                elif input_active_y:
                    if event.key == pygame.K_BACKSPACE:
                        y_tiles = y_tiles[:-1]
                    else:
                        y_tiles += event.unicode
        elif start_game:
            start_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if one_player_rect.collidepoint(mouse_pos):
                    player_count = 1
                    robots = [
                        Robot(
                            arena.x_offset + 100,
                            display_resolution[1] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        )
                    ]
                    start_game = False
                elif two_player_rect.collidepoint(mouse_pos):
                    player_count = 2
                    robots = [
                        Robot(
                            robot_spawn_distance,
                            display_resolution[1] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                        Robot(2 * robot_spawn_distance, display_resolution[0] - 100, 25, 45, 1, 1),
                    ]
                    jump = [False]
                    start_game = False
                elif three_player_rect.collidepoint(mouse_pos):
                    player_count = 3
                    robots = [
                        Robot(
                            robot_spawn_distance,
                            display_resolution[1] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                        Robot(
                            2 * robot_spawn_distance,
                            display_resolution[1] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                        Robot(
                            3 * robot_spawn_distance,
                            display_resolution[1] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                    ]
                    jump = [False, False]
                    start_game = False
                elif four_player_rect.collidepoint(mouse_pos):
                    player_count = 4
                    robots = [
                        Robot(
                            robot_spawn_distance,
                            display_resolution[0] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                        Robot(
                            2 * robot_spawn_distance,
                            display_resolution[0] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                        Robot(
                            3 * robot_spawn_distance,
                            display_resolution[0] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                        Robot(
                            4 * robot_spawn_distance,
                            display_resolution[0] - 2 * dist_between_elements,
                            robot_radius,
                            45,
                            1,
                            1,
                        ),
                    ]
                    jump = [False, False, False]
                    start_game = False
                if robots:
                    min_x = robots[0].radius + arena.x_offset
                    max_x = display_resolution[0] - robots[0].radius - arena.x_offset
                    min_y = robots[0].radius + arena.y_offset
                    max_y = display_resolution[1] - robots[0].radius - arena.y_offset

        elif event.type == pygame.MOUSEBUTTONDOWN and game_paused:
            mouse_pos = pygame.mouse.get_pos()
            if resume_rect.collidepoint(mouse_pos):
                game_paused = False
            elif main_menu_rect.collidepoint(mouse_pos):
                menu = True
                game_paused = False
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] and not menu and not start_game and not build_arena:
        game_paused = True

    if not game_paused and not start_game and not menu and not build_arena:
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
                jump[i - 1] = random.choice([True, False])

        for i in range(1, len(robots)):
            # Bewegung des Roboters
            movement.move_bot(
                robots[i], display_resolution[1], display_resolution[1], robots[i].vel, arena, jump[i - 1]
            )
            robots[i].change_velocity_cap(robots[i].vel + robots[i].accel)
            jump[i - 1] = False

            # Überprüfe die Grenzen und passe die Position an, wenn nötig
            # robots[i].posx = max(min(robots[i].posx, max_x), min_x)
            # robots[i].posy = max(min(robots[i].posy, max_y), min_y)
            robots[i].paint_robot(pygame, screen)

        player_robot.change_velocity_cap(player_robot.vel + player_robot.accel)
        movement.move_robot(player_robot, display_resolution[1], display_resolution[0], player_robot.vel, arena)
        player_robot.paint_robot(pygame, screen)
    elif game_paused:
        pause_screen()

    pygame.display.update()


pygame.quit()
