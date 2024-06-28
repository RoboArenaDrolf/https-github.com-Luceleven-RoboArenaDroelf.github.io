import os
import random
import pygame
from pygame._sdl2.video import Window
from screeninfo import get_monitors
import sys

from movement import Movement
from arena import Arena
from arenaBuilder import ArenaBuilder
from robot import Robot
from screens import Screens

pygame.init()
pygame.joystick.init()

# Controller initialisieren
joysticks = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
    print(f"Joystick {i}: {joystick.get_name()} initialized.")

display_resolution = (720, 720)
available_resolutions = [(720, 720), (1280, 720), (1280, 1080), (1920, 1080)]
monitor = get_monitors()[0]
fullscreen_res = (monitor.width, monitor.height)
fullscreen = False

screen = pygame.display.set_mode(display_resolution)
pygame.display.set_caption("Robo Arena")

white = (255, 255, 255)

map_filename = "secondMap.json"
maps = []
movement = Movement(display_resolution[1] / 2000)
arena = Arena(map_filename, pygame)

robot_radius = arena.tile_size * 0.5
robot_spawn_distance = display_resolution[0] / 10

game_paused = False
run = True
start_game = False
menu = True
build_arena = False
settings = False
playing = False
map = False
death = False
robots = []
direction_left = False
use_controller = True

input_active_x = False
input_active_y = False
x_tiles = ""
y_tiles = ""
menu_items = []
selected_item_index = 0
recently_switched_item = False

# Zähler für die Anzahl der Frames, bevor die Richtung des Roboters geändert wird
change_direction_interval = 100  # Ändere die Richtung alle 120 Frames
frame_count = 0
# Initiale Fensterposition
window = Window.from_display_module()
initial_window_pos = window.position

jump = []

clock = pygame.time.Clock()


def get_json_filenames(directory):
    json_files = []
    # Gehe durch alle Dateien im angegebenen Verzeichnis
    for filename in os.listdir(directory):
        # Überprüfe, ob die Datei die Endung .json hat
        if filename.endswith(".json"):
            # Überprüfe, ob es nicht die emptyMap ist, denn diese wird ausgeschlossen
            if filename != "emptyMap.json":
                # Füge den Dateinamen ohne die Endung .json der Liste hinzu
                json_files.append(filename[:-5])
    return json_files


def get_png_filenames(directory):
    png_files = []
    # Gehe durch alle Dateien im angegebenen Verzeichnis
    for filename in os.listdir(directory):
        # Überprüfe, ob die Datei die Endung .png hat
        if filename.endswith(".png"):
            # Füge den Dateinamen der Liste hinzu
            png_files.append(filename)
    return png_files


def update_maps(map_names):
    global maps
    for name in map_names:
        maps.append(name + ".json")


map_names = get_json_filenames(arena.maps_base_path)
update_maps(map_names)
screens = Screens(pygame, available_resolutions, map_names)


def recalculate_robot_values():
    global robots, robot_radius, robot_spawn_distance
    robot_radius = min(display_resolution) / 40
    robot_spawn_distance = display_resolution[0] / 10
    if robots:
        for i, robot in enumerate(robots):
            robot.radius = robot_radius
            robot.posx = (i + 1) * robot_spawn_distance + arena.x_offset
            robot.posy = display_resolution[1] - 1.5 * arena.tile_size - arena.y_offset
            robot.accel_max = arena.map_size[0] / float(1000)
            robot.accel_alpha_max = arena.map_size[0] / float(1000)
            robot.vel_max = arena.map_size[0] / float(200)


def reset_selected_item():
    global selected_item_index
    menu_items[selected_item_index].selected = False
    selected_item_index = 0


def handle_main_menu_events():
    global robots, start_game, menu, build_arena, settings, run

    if play_item.pressed:
        robots = []
        start_game = True
        menu = False
    elif build_arena_item.pressed:
        build_arena = True
        menu = False
        reset_selected_item()
    elif settings_item.pressed:
        settings = True
        menu = False
        reset_selected_item()
    elif exit_item.pressed:
        run = False


def handle_build_arena_menu_events(event):
    global input_active_x, input_active_y, build_arena, menu, x_tiles, y_tiles, screens

    if event.type == pygame.MOUSEBUTTONDOWN:
        if input_rect_x_tiles.collidepoint(mouse_pos):
            input_active_x = True
            input_active_y = False
        elif input_rect_y_tiles.collidepoint(mouse_pos):
            input_active_y = True
            input_active_x = False
        elif start_building_item.pressed:
            try:
                num_x = int(x_tiles)
                num_y = int(y_tiles)
                if num_x <= 0 or num_y <= 0:
                    raise ValueError
                build_arena = False
                menu = True
                arenaBuilder = ArenaBuilder(num_x, num_y, pygame)
                arenaBuilder.main()
                map_names = get_json_filenames(arena.maps_base_path)
                update_maps(map_names)
                screens = Screens(pygame, available_resolutions, map_names)
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


def handle_settings_menu_events():
    global display_resolution, fullscreen, menu, settings, screen, arena, movement, screens, use_controller

    dis_res_changed = False

    if controller_on_off_item.pressed:
        use_controller = not use_controller
        if use_controller:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
    elif fullscreen_item.pressed:
        display_resolution = fullscreen_res
        fullscreen = True
        dis_res_changed = True
    elif back_item.pressed:
        menu = True
        settings = False
        reset_selected_item()

    for i, res_item in enumerate(resolution_items):
        if res_item.pressed:
            display_resolution = available_resolutions[i]
            fullscreen = False
            dis_res_changed = True
            break

    if dis_res_changed:
        if fullscreen:
            screen = pygame.display.set_mode(display_resolution, pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(display_resolution)
        screens = Screens(pygame, available_resolutions, get_json_filenames(arena.maps_base_path))
        arena = Arena(map_filename, pygame)
        movement = Movement(display_resolution[1] / 2000)
        recalculate_robot_values()


def handle_start_game_menu_events():
    global robots, jump, start_game, map

    robot1 = Robot(
        robot_spawn_distance + arena.x_offset,
        display_resolution[1] - 1.5 * arena.tile_size - arena.y_offset,
        robot_radius,
        0,
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(200),
        100,
        "blue",
        0,
    )
    robot2 = Robot(
        2 * robot_spawn_distance + arena.x_offset,
        display_resolution[1] - 1.5 * arena.tile_size - arena.y_offset,
        robot_radius,
        0,
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(200),
        100,
        "red",
        1,
    )
    robot3 = Robot(
        3 * robot_spawn_distance + arena.x_offset,
        display_resolution[1] - 1.5 * arena.tile_size - arena.y_offset,
        robot_radius,
        0,
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(200),
        100,
        "green",
        2,
    )
    robot4 = Robot(
        4 * robot_spawn_distance + arena.x_offset,
        display_resolution[1] - 1.5 * arena.tile_size - arena.y_offset,
        robot_radius,
        0,
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(1000),
        arena.map_size[0] / float(200),
        100,
        "yellow",
        3,
    )

    if one_player_item.pressed:
        robots = [robot1]
    elif two_player_item.pressed:
        robots = [robot1, robot2]
        jump = [False]
        start_game = False
    elif three_player_item.pressed:
        robots = [robot1, robot2, robot3]
        jump = [False, False]
        start_game = False
    elif four_player_item.pressed:
        robots = [robot1, robot2, robot3, robot4]
        jump = [False, False, False]
    if robots:
        start_game = False
        map = True
        reset_selected_item()


def handle_death_screen_events():
    global menu, death

    if main_menu_item.pressed:
        menu = True
        death = False
    elif quit_item.pressed:
        pygame.quit()
        sys.exit()


def handle_pause_screen_events():
    global game_paused, menu, playing

    if resume_item.pressed:
        game_paused = False
    elif main_menu_item.pressed:
        menu = True
        playing = False
        game_paused = False
        reset_selected_item()
    elif quit_item.pressed:
        pygame.quit()
        sys.exit()


def handle_map_screen_events():
    global map, playing, arena, map_filename

    for i, level_item in enumerate(level_items):
        if level_item.pressed:
            map_filename = maps[i]
            arena = Arena(map_filename, pygame)
            arena.render_arena(pygame)
            map = False
            playing = True
            reset_selected_item()
            break


def game_loop():
    global player_robot, frame_count

    screen.fill(white)
    arena.paint_arena(screen)
    frame_count += 1
    player_robot = robots[0]
    # Handling of player robot
    player_robot_handling(player_robot)
    # Handling of bots
    bots_handling()


def bots_handling():
    global frame_count

    # Setup bots random movement
    if frame_count >= change_direction_interval:
        for i in range(1, len(robots)):
            # Zufällige Änderungen der Beschleunigung und der Drehgeschwindigkeit
            robots[i].change_acceleration(robots[i].accel + random.uniform(-1, 1))
            # Setze den Zähler zurück
            frame_count = 0
            jump[i - 1] = random.choice([True, False])
    # Move and paint bots
    for i in range(1, len(robots)):
        robots[i].change_velocity_cap(robots[i].vel + robots[i].accel)
        robots[i].decrease_hit_cooldown()
        if robots[i].vel < 0:
            robots[i].change_acceleration(robots[i].accel + arena.map_size[0] / 40000)
            if robots[i].vel + robots[i].accel >= 0:
                robots[i].change_velocity_cap(0)
                robots[i].change_acceleration(0)
        elif robots[i].vel > 0:
            robots[i].change_acceleration(robots[i].accel - arena.map_size[0] / 40000)
            if robots[i].vel + robots[i].accel <= 0:
                robots[i].change_velocity_cap(0)
                robots[i].change_acceleration(0)
        else:
            robots[i].change_acceleration(0)
        # Bewegung des Roboters
        movement.move_bot(
            robots[i], display_resolution[1], display_resolution[0], robots[i].vel, arena, jump[i - 1], dt
        )
        jump[i - 1] = False
        robots[i].paint_robot(pygame, screen, direction_left)


def player_robot_handling(player_robot):
    global playing, death

    # Überprüfen, ob player die seitlichen Grenzen der Arena erreicht hat
    if player_robot.posx + player_robot.radius - arena.x_offset < 0:
        player_robot.health = 0
    elif player_robot.posx - player_robot.radius + arena.x_offset > display_resolution[0]:
        player_robot.health = 0
    # Überprüfen, ob player die oberen und unteren Grenzen der Arena erreicht hat
    if player_robot.posy + player_robot.radius < arena.y_offset:
        player_robot.health = 0
    elif player_robot.posy - player_robot.radius > display_resolution[1] - arena.y_offset:
        player_robot.health = 0
    # Check if player is dead:
    if player_robot.health <= 0:
        playing = False
        death = True
    # attack will stay for a certain duration
    if player_robot.melee_cd < 30 and player_robot.melee_cd != 0:
        player_robot.melee_attack(pygame, screen, robots, arena)
        player_robot.melee_cd += 1
    # Player melee attack cooldown
    elif player_robot.melee_cd != 0:
        if player_robot.melee_cd == 60:
            player_robot.melee_cd = 0
        else:
            player_robot.melee_cd += 1
    # second ranged attack at ranged_cd == 10
    if player_robot.ranged_cd < 11 and player_robot.ranged_cd != 0:
        player_robot.ranged_attack()
        player_robot.ranged_cd += 1
    # Player ranged attack cooldown
    elif player_robot.ranged_cd != 0:
        if player_robot.ranged_cd == 60:
            player_robot.ranged_cd = 0
        else:
            player_robot.ranged_cd += 1

    # Player movement
    if use_controller:
        joystick = joysticks[0]
        moved = move_player_controller(player_robot, joystick)
    else:
        keys = pygame.key.get_pressed()
        moved = move_player_keys(player_robot, keys)
    if not moved:
        if player_robot.vel < 0:
            player_robot.change_acceleration(player_robot.accel + arena.map_size[0] / 40000)
            if player_robot.vel + player_robot.accel >= 0:
                player_robot.change_velocity_cap(0)
                player_robot.change_acceleration(0)
        elif player_robot.vel > 0:
            player_robot.change_acceleration(player_robot.accel - arena.map_size[0] / 40000)
            if player_robot.vel + player_robot.accel <= 0:
                player_robot.change_velocity_cap(0)
                player_robot.change_acceleration(0)
        else:
            player_robot.change_acceleration(0)
    player_robot.change_velocity_cap(player_robot.vel + player_robot.accel)
    movement.move_robot(player_robot, player_robot.vel, arena, dt)
    player_robot.paint_robot(pygame, screen, direction_left)
    player_robot.ranged_hit_reg(robots, display_resolution[1], display_resolution[0], arena)


def move_player_keys(player_robot, keys):
    global direction_left
    if keys[pygame.K_LEFT]:
        player_robot.change_acceleration(player_robot.accel - arena.map_size[0] / 20000)
        player_robot.change_alpha(180)
        direction_left = True
    elif keys[pygame.K_RIGHT]:
        player_robot.change_acceleration(player_robot.accel + arena.map_size[0] / 20000)
        player_robot.change_alpha(0)
        direction_left = False
    elif keys[pygame.K_DOWN]:
        player_robot.change_alpha(90)
        return False
    elif keys[pygame.K_UP]:
        player_robot.change_alpha(270)
        return False
    else:
        return False
    return True


def move_player_controller(player_robot, joystick):
    global direction_left
    value_x = joystick.get_axis(0)
    value_y = joystick.get_axis(1)
    if value_x < -0.2:
        player_robot.change_acceleration(player_robot.accel - arena.map_size[0] / 20000)
        player_robot.change_alpha(180)
        direction_left = True
    elif value_x > 0.2:
        player_robot.change_acceleration(player_robot.accel + arena.map_size[0] / 20000)
        player_robot.change_alpha(0)
        direction_left = False
    elif value_y > 0.2:
        player_robot.change_alpha(90)
        return False
    elif value_y < -0.2:
        player_robot.change_alpha(270)
        return False
    else:
        return False
    return True


while run:
    pygame.time.delay(0)
    dt = clock.tick(120)

    current_window_pos = window.position
    if playing:
        if current_window_pos != initial_window_pos:
            game_paused = True
            initial_window_pos = current_window_pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not playing or game_paused:
                for item in menu_items:
                    if item.rect.collidepoint(mouse_pos):
                        item.pressed = True
                if build_arena:
                    handle_build_arena_menu_events(event)
                elif start_game:
                    handle_start_game_menu_events()

        elif event.type == pygame.KEYDOWN:
            if playing and not game_paused:
                player_robot = robots[0]
                key = event.key
                if key == pygame.K_ESCAPE:
                    game_paused = True
                elif (
                    key == pygame.K_g and player_robot.melee_cd == 0
                ):  # we can attack if we have no cooldown and press the button
                    player_robot.melee_attack(pygame, screen, robots, arena)
                    player_robot.melee_cd += 1
                elif key == pygame.K_r and (player_robot.ranged_cd == 0 or player_robot.ranged_cd == 10):
                    player_robot.ranged_attack()
                    player_robot.ranged_cd += 1
                elif key == pygame.K_f:
                    player_robot.take_damage_debug(10)
                elif key == pygame.K_SPACE:
                    if player_robot.jump_counter <= 1:
                        player_robot.jump = True
            elif build_arena:
                handle_build_arena_menu_events(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            if playing and not game_paused:
                player_robot = robots[0]
                if event.button == 0:
                    if player_robot.jump_counter <= 1:
                        player_robot.jump = True
                elif event.button == 7:
                    game_paused = True
            else:
                if event.button == 1:
                    menu_items[selected_item_index].pressed = True
                if start_game:
                    handle_start_game_menu_events()

        elif event.type == pygame.JOYAXISMOTION:
            if playing and not game_paused:
                player_robot = robots[0]
                if (
                    event.axis == 5 and event.value > 0.2 and player_robot.melee_cd == 0
                ):  # we can attack if we have no cooldown and press the button
                    player_robot.melee_attack(pygame, screen, robots, arena)
                    player_robot.melee_cd += 1
                if (
                    event.axis == 4
                    and event.value > 0.2
                    and (player_robot.ranged_cd == 0 or player_robot.ranged_cd == 10)
                ):
                    player_robot.ranged_attack()
                    player_robot.ranged_cd += 1
            else:
                if event.axis == 1:
                    if event.value > 0.2 and not recently_switched_item:
                        menu_items[selected_item_index].selected = False
                        selected_item_index += 1
                        if selected_item_index >= len(menu_items):
                            selected_item_index = 0
                        recently_switched_item = True
                    elif event.value < -0.2 and not recently_switched_item:
                        menu_items[selected_item_index].selected = False
                        selected_item_index -= 1
                        if selected_item_index < 0:
                            selected_item_index = len(menu_items) - 1
                        recently_switched_item = True
                    elif -0.2 <= event.value <= 0.2:
                        recently_switched_item = False

    if playing and not game_paused:
        game_loop()
    # Painting the screens:
    elif game_paused:
        menu_items = screens.pause_screen(pygame, screen)
        resume_item, main_menu_item, quit_item = menu_items[0], menu_items[1], menu_items[2]
        handle_pause_screen_events()
    elif death:
        menu_items = screens.death_screen(pygame, screen)
        main_menu_item, quit_item = menu_items[0], menu_items[1]
        handle_death_screen_events()
    elif menu:
        menu_items = screens.main_menu_screen(pygame, screen)
        play_item, build_arena_item, settings_item, exit_item = (
            menu_items[0],
            menu_items[1],
            menu_items[2],
            menu_items[3],
        )
        handle_main_menu_events()
    elif settings:
        menu_items = screens.settings_screen(pygame, screen)
        controller_on_off_item = menu_items[0]
        resolution_items = []
        for i in range(1, 5):
            resolution_items.append(menu_items[i])
        fullscreen_item, back_item = menu_items[5], menu_items[6]
        handle_settings_menu_events()
    elif build_arena:
        input_rect_x_tiles, input_rect_y_tiles, menu_items = screens.build_arena_screen(
            pygame, screen, x_tiles, y_tiles
        )
        start_building_item = menu_items[0]
    elif start_game:
        menu_items = screens.start_screen(pygame, screen)
        one_player_item, two_player_item, three_player_item, four_player_item = (
            menu_items[0],
            menu_items[1],
            menu_items[2],
            menu_items[3],
        )
    elif map:
        menu_items = screens.maps_screen(pygame, screen)
        level_items = menu_items
        handle_map_screen_events()

    # Check mouse pos and select menu items
    if (not playing or game_paused) and not use_controller:
        mouse_pos = pygame.mouse.get_pos()
        for i, item in enumerate(menu_items):
            if item.rect.collidepoint(mouse_pos):
                selected_item_index = i
                item.selected = True
            else:
                item.selected = False
    # If using controller: Check selected item index and set it to True
    elif (not playing or game_paused) and use_controller:
        menu_items[selected_item_index].selected = True

    # Reset pressed items
    for item in menu_items:
        item.pressed = False

    pygame.display.update()


pygame.quit()
