# Robo Arena Documentation

## Overview
1. [Robot](#robot-class-robotpy)
2. [Movement](#movement-class-movementpy)
3. [Game](#main-game-file-gamepy)
4. [ArenaBuilder](#arenabuilder-class-arenabuilderpy)
5. [Arena](#arena-class-arenapy)
6. [Usage](#usage)
7. [Dependencies](#dependencies)

This project is a simple 2D game called "Robo Arena" developed using Python and Pygame. The game features a robot that moves within an arena and interacts with different tile types. The project is organized into several modules, each responsible for different aspects of the game, such as robot control, movement, arena building, and game mechanics.<br>
<br>
File Structure:
- robot.py: Contains the Robot class, which handles the robot's properties and actions.
- movement.py: Contains the Movement class, which manages the robot's movement including gravity effects.
- game.py: The main game loop and interface, handling game initialization, event processing, and rendering.
- arenaBuilder.py: Contains the ArenaBuilder class, which allows creating and modifying the game arena.
- arena.py: Contains the Arena class, which represents the game arena and handles loading and rendering the tiles.


## Robot Class (robot.py)

This class defines a robot with properties such as position, radius, angle, and various types of acceleration and velocity. It also includes methods to change these properties and render the robot in the game.<br>
<br> Methods:

- \_\_init\_\_(self, x, y, r, a, am, aam): Initializes the robot with its position (x, y), radius r, angle a, and maximum accelerations am and aam.
- change_acceleration(self, a): Changes the linear acceleration of the robot, ensuring it does not exceed accel_max.
- change_rot_acceleration(self, aa): Changes the rotational acceleration, limited by accel_alpha_max.
- change_velocity(self, v): Directly sets the robot's velocity.
- change_velocity_cap(self, v): Changes the velocity but limits it to a range of -5 to 5.
- change_turn_velocity(self, va): Sets the rotational velocity.
- paint_robot(self, pygame, screen): Draws the robot on the screen using Pygame.


## Movement Class (movement.py)

This class handles the movement mechanics of the robot, including horizontal movement and vertical movement influenced by gravity.<br>
<br>Methods
- move_robot(self, robot, screen_height, x): Updates the robot's position based on user input and gravity, ensuring it stays within the screen boundaries.

## Main Game file (game.py)

This file contains the main game loop, handling initialization, event processing, and rendering. It sets up the game window, processes user inputs, and updates the game state accordingly.<br>
<br>Key Components:

- Global Variables: Defines constants and global variables for the game.
- pause_screen(): Displays the pause screen with options to resume or quit the game.
- Main Game Loop: Initializes objects for the robot, movement, and arena, and processes events to update the game state.


## ArenaBuilder Class (arenaBuilder.py)

This class extends the Arena class to provide functionality for creating and editing the game arena. It includes methods for setting up an empty map, handling user input, and saving/loading maps.<br>
<br>Methods:

- \_\_init\_\_(self, num_tiles_x, num_tiles_y, pygame): Initializes the arena builder with a specified number of tiles.
- _set_up_empty_map(self, num_tiles_x, num_tiles_y): Creates an empty map with "AIR" tiles.
- _set_up_basics(self, filename, pygame): Basic setup for the arena and screen.
- _set_up_paint_related(self): Sets up the interface elements for painting the arena builder.
- main(self): Main loop for the arena builder, handling events and rendering the interface.
- _paint_tile(self, current_tile): Paints a tile at the mouse position.
- _handle_key_down(self, current_tile, event): Handles key down events for changing tiles and text input.
- _handle_mouse_button_down(...): Handles mouse button down events for buttons and text input.
- _load_map(self): Loads a map from a file.
- _save_map(self): Saves the current map to a file.
- _paint_arena_builder(self, save_button_clicked, load_button_clicked): Paints the arena builder interface.
- _draw_buttons(self, load_button_clicked, save_button_clicked): Draws save and load buttons.
- _draw_input_fields(self): Draws input fields for saving and loading maps.
- _draw_legend(self): Draws the legend of tile types.
- _draw_grid(self): Draws grid lines. 
- set_tile(self, x, y, tile_type): Sets a tile at a specific position. 
- save_to_json(self, filename): Saves the map data to a JSON file.


## Arena Class (arena.py)

This class represents the game arena, managing the loading and rendering of tiles from a JSON file.<br>
<br>Methods:

- \_\_init\_\_(self, filename, pygame): Initializes the arena by loading a map from a JSON file. 
- load_map_from_json(self, filename): Loads map data from a JSON file. 
- paint_arena(self, pygame, screen): Paints the arena on the screen using Pygame.

TileType Enum:

An enumeration of different tile types, each associated with a specific image file. The images are loaded and used to render the tiles in the arena.

## Usage

To run the game, execute the game.py file. This will initialize the game window and start the main game loop. Use the arrow keys to move the robot and interact with the arena.

To use the arena builder, execute the main function of an ArenaBuilder object. This will open the arena builder interface, allowing you to create and modify the game map. Use the number keys to select different tile types and the mouse to place tiles. You can save and load maps using the input fields and buttons provided.

## Dependencies

- Python 3.x 
- Pygame

Install the required dependencies using pip:

```sh
pip install pygame
```