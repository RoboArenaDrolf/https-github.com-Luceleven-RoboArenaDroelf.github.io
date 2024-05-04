import json

import pygame
from enum import Enum

class ArenaBuilder:
    class TileType(Enum):
        """
        Enum of different tile types, value of tile represents it's color.
        """
        CONCRETE = (178, 190, 181)
        AIR = (255, 255, 255)
        GRASS = (0, 107, 60)
        ICE = (113, 166, 210)
        SAND = (237, 201, 175)
        LAVA = (207, 16, 32)

    _CO = TileType.CONCRETE
    _GR = TileType.GRASS
    _IC = TileType.ICE
    _AI = TileType.AIR
    _SA = TileType.SAND
    _LA = TileType.LAVA

    tile_size = 50

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[self._AI for _ in range(width)] for _ in range(height)]

    def paint_arena_builder(self, pygame, screen):
        """
        Paints an empty arena with a grid with help of parameters pygame and screen.

        :param pygame: pygame instance
        :param screen: screen element of pygame initialized with pygame.display.set_mode()
        """
        y = 0
        for row in self.tiles:
            x = 0
            for tile in row:
                pygame.draw.rect(screen, tile.value, [x, y, self.tile_size, self.tile_size])
                x += self.tile_size
            y += self.tile_size

        for x in range(0, screen.get_width(), self.tile_size):
            pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, screen.get_height()))
        for y in range(0, screen.get_height(), self.tile_size):
            pygame.draw.line(screen, (100, 100, 100), (0, y), (screen.get_width(), y))

    def set_tile(self, x, y, tile_type):
        self.tiles[y][x] = tile_type

    # Speichere die Daten in einer JSON-Datei
    def save_to_json(self, filename):
        data = {'width': self.width, 'height': self.height, 'tiles': [[tile.name for tile in row] for row in self.tiles]}
        with open(filename, 'w') as f:
            json.dump(data, f)


pygame.init()

# Set up the screen
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Map Builder")
screen_width = 1000

# Initialize the arenaBuilder
arenaBuilder = ArenaBuilder(screen_width // ArenaBuilder.tile_size, screen_height // ArenaBuilder.tile_size)

# Main loop
running = True
current_tile = arenaBuilder.TileType.CONCRETE
mouse_pressed = False
button_clicked = False
button_click_time = 0

# Set up font
font = pygame.font.SysFont(None, 24)

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)

# Set up save button
save_button_rect = pygame.Rect(screen_width + 20, 300, 160, 40)
save_button_text = font.render('Save to JSON', True, WHITE)

# Set up text input field
input_rect = pygame.Rect(screen_width + 20, 250, 160, 30)
input_text = ''
input_active = False
text_color = WHITE

clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pressed = True
            mouse_pos = pygame.mouse.get_pos()
            if save_button_rect.collidepoint(mouse_pos):
                button_clicked = True
                button_click_time = current_time
                arenaBuilder.save_to_json(input_text + '.json')
            if input_rect.collidepoint(mouse_pos):
                input_active = True
            else:
                input_active = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button released
            mouse_pressed = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    arenaBuilder.save_to_json(input_text + '.json')
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif event.key == pygame.K_1:
                current_tile = arenaBuilder.TileType.CONCRETE
            elif event.key == pygame.K_2:
                current_tile = arenaBuilder.TileType.AIR
            elif event.key == pygame.K_3:
                current_tile = arenaBuilder.TileType.GRASS
            elif event.key == pygame.K_4:
                current_tile = arenaBuilder.TileType.ICE
            elif event.key == pygame.K_5:
                current_tile = arenaBuilder.TileType.SAND
            elif event.key == pygame.K_6:
                current_tile = arenaBuilder.TileType.LAVA


    if mouse_pressed:
        x, y = pygame.mouse.get_pos()
        x //= arenaBuilder.tile_size
        y //= arenaBuilder.tile_size
        if x < arenaBuilder.width and y < arenaBuilder.height:
            arenaBuilder.set_tile(x, y, current_tile)

    # Clear the screen
    screen.fill(BLACK)

    # Paint the arenaBuilder
    arenaBuilder.paint_arena_builder(pygame, screen)

    # Draw legend
    legend_surface = pygame.Surface((200, screen_height))
    legend_surface.fill((0, 0, 0))
    legend_pos = (screen_width + 20, 10)
    legend_spacing = 20
    for idx, tile_type in enumerate(ArenaBuilder.TileType):
        legend_text = f"{idx + 1}: {tile_type.name}"
        text_surface = font.render(legend_text, True, tile_type.value)
        legend_surface.blit(text_surface, (10, legend_pos[1] + idx * legend_spacing))
    screen.blit(legend_surface, (screen_width, 0))

    # Draw save button
    if button_clicked:
        pygame.draw.rect(screen, DARK_GREEN, save_button_rect)
    else:
        pygame.draw.rect(screen, GREEN, save_button_rect)
    screen.blit(save_button_text, (save_button_rect.x + 10, save_button_rect.y + 10))

    if button_clicked and current_time - button_click_time >= 200:
        button_clicked = False

    # Draw text input field
    pygame.draw.rect(screen, BLACK, input_rect)
    pygame.draw.rect(screen, text_color, input_rect, 2)
    text_surface = font.render(input_text, True, text_color)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Update the display
    pygame.display.flip()

pygame.quit()
