import json
from arena import Arena

class ArenaBuilder(Arena):

    # Set up colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 200, 0)
    GREY = (100, 100, 100)

    def __init__(self, num_tiles_x, num_tiles_y, pygame, screen):
        self.num_tiles_x = num_tiles_x
        self.num_tiles_y = num_tiles_y
        self.tiles = [[self.TileType.AIR for _ in range(self.num_tiles_x)] for _ in range(self.num_tiles_y)]
        filename = "emptyMap.json"
        self.save_to_json(filename)
        super().__init__(filename)

        self.pygame = pygame
        self.screen = screen

        self.x_placing_of_legend = num_tiles_x * self.tile_size

        # Set up font
        self.font = self.pygame.font.SysFont(None, 24)
        self.text_color = self.WHITE

        # Set up text input field for saving
        self.input_text_saving = ''
        self.input_active_saving = False
        self.input_rect_saving = self.pygame.Rect(self.x_placing_of_legend + 20, 250, 160, 30)

        # Set up save button
        self.save_button_text = self.font.render('Save Map', True, self.WHITE)
        self.save_button_rect = self.pygame.Rect(self.x_placing_of_legend + 20, 300, 160, 40)

        # Set up text input field for loading
        self.input_text_loading = ''
        self.input_active_loading = False
        self.input_rect_loading = self.pygame.Rect(self.x_placing_of_legend + 20, 350, 160, 30)

        # Set up load button
        self.load_button_text = self.font.render('Load Map', True, self.WHITE)
        self.load_button_rect = self.pygame.Rect(self.x_placing_of_legend + 20, 400, 160, 40)

    def main(self):
        running = True
        current_tile = self.TileType.CONCRETE
        mouse_pressed = False
        save_button_clicked = False
        load_button_clicked = False
        button_click_time_saving = 0
        button_click_time_loading = 0

        # Main loop
        while running:
            current_time = self.pygame.time.get_ticks()

            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                elif event.type == self.pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    mouse_pressed = True
                    mouse_pos = self.pygame.mouse.get_pos()
                    if self.save_button_rect.collidepoint(mouse_pos):
                        save_button_clicked = True
                        button_click_time_saving = current_time
                        self.save_to_json(self.input_text_saving + '.json')
                    elif self.load_button_rect.collidepoint(mouse_pos):
                        load_button_clicked = True
                        button_click_time_loading = current_time
                        self.num_tiles_x, self.num_tiles_y, self.tiles = self.load_map_from_json(self.input_text_loading + '.json')
                        self.input_text_saving = self.input_text_loading
                    if self.input_rect_saving.collidepoint(mouse_pos):
                        self.input_active_saving = True
                    else:
                        self.input_active_saving = False
                    if self.input_rect_loading.collidepoint(mouse_pos):
                        self.input_active_loading = True
                    else:
                        self.input_active_loading = False
                elif event.type == self.pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button released
                    mouse_pressed = False
                elif event.type == self.pygame.KEYDOWN:
                    if self.input_active_saving:
                        if event.key == self.pygame.K_RETURN:
                            self.input_active_saving = False
                            self.save_to_json(self.input_text_saving + '.json')
                        elif event.key == self.pygame.K_BACKSPACE:
                            self.input_text_saving = self.input_text_saving[:-1]
                        else:
                            self.input_text_saving += event.unicode
                    elif self.input_active_loading:
                        if event.key == self.pygame.K_RETURN:
                            self.input_active_loading = False
                            self.num_tiles_x, self.num_tiles_y, self.tiles = self.load_map_from_json(self.input_text_loading + '.json')
                            self.input_text_saving = self.input_text_loading
                        elif event.key == self.pygame.K_BACKSPACE:
                            self.input_text_loading= self.input_text_loading[:-1]
                        else:
                            self.input_text_loading += event.unicode
                    elif event.key == self.pygame.K_1:
                        current_tile = self.TileType.CONCRETE
                    elif event.key == self.pygame.K_2:
                        current_tile = self.TileType.AIR
                    elif event.key == self.pygame.K_3:
                        current_tile = self.TileType.GRASS
                    elif event.key == self.pygame.K_4:
                        current_tile = self.TileType.ICE
                    elif event.key == self.pygame.K_5:
                        current_tile = self.TileType.SAND
                    elif event.key == self.pygame.K_6:
                        current_tile = self.TileType.LAVA

            if mouse_pressed:
                x, y = self.pygame.mouse.get_pos()
                x //= self.tile_size
                y //= self.tile_size
                if x < self.num_tiles_x and y < self.num_tiles_y:
                    self.set_tile(x, y, current_tile)

            # Clear the self.screen
            self.screen.fill(self.BLACK)

            # Paint the arenaBuilder
            self.paint_arena_builder(save_button_clicked, load_button_clicked)

            if save_button_clicked and current_time - button_click_time_saving >= 200:
                save_button_clicked = False

            if load_button_clicked and current_time - button_click_time_loading >= 200:
                load_button_clicked = False

            # Update the display
            self.pygame.display.flip()


    def paint_arena_builder(self, save_button_clicked, load_button_clicked):
        """
        Paints an empty arena with a grid and a legend of possible tiles
        """
        self.paint_arena(self.pygame, self.screen)

        for x in range(0, self.x_placing_of_legend, self.tile_size):
            self.pygame.draw.line(self.screen, self.GREY, (x, 0), (x, self.screen.get_height()))
        for y in range(0, self.screen.get_height(), self.tile_size):
            self.pygame.draw.line(self.screen, self.GREY, (0, y), (self.screen.get_width(), y))

        # Draw legend
        legend_surface = self.pygame.Surface((200, self.screen.get_height()))
        legend_surface.fill((0, 0, 0))
        legend_pos = (self.x_placing_of_legend + 20, 10)
        legend_spacing = 20
        for idx, tile_type in enumerate(self.TileType):
            legend_text = f"{idx + 1}: {tile_type.name}"
            text_surface = self.font.render(legend_text, True, tile_type.value)
            legend_surface.blit(text_surface, (10, legend_pos[1] + idx * legend_spacing))
        self.screen.blit(legend_surface, (self.x_placing_of_legend, 0))

        # Draw text input field saving
        self.pygame.draw.rect(self.screen, self.BLACK, self.input_rect_saving)
        self.pygame.draw.rect(self.screen, self.text_color, self.input_rect_saving, 2)
        text_surface = self.font.render(self.input_text_saving, True, self.text_color)
        self.screen.blit(text_surface, (self.input_rect_saving.x + 5, self.input_rect_saving.y + 5))

        # Draw save button
        if save_button_clicked:
            self.pygame.draw.rect(self.screen, self.DARK_GREEN, self.save_button_rect)
        else:
            self.pygame.draw.rect(self.screen, self.GREEN, self.save_button_rect)
        self.screen.blit(self.save_button_text, (self.save_button_rect.x + 10, self.save_button_rect.y + 10))

        # Draw text input field loading
        self.pygame.draw.rect(self.screen, self.BLACK, self.input_rect_loading)
        self.pygame.draw.rect(self.screen, self.text_color, self.input_rect_loading, 2)
        text_surface = self.font.render(self.input_text_loading, True, self.text_color)
        self.screen.blit(text_surface, (self.input_rect_loading.x + 5, self.input_rect_loading.y + 5))

        # Draw load button
        if load_button_clicked:
            self.pygame.draw.rect(self.screen, self.DARK_GREEN, self.load_button_rect)
        else:
            self.pygame.draw.rect(self.screen, self.GREEN, self.load_button_rect)
        self.screen.blit(self.load_button_text, (self.load_button_rect.x + 10, self.load_button_rect.y + 10))

    def set_tile(self, x, y, tile_type):
        self.tiles[y][x] = tile_type

    # Speichere die Daten in einer JSON-Datei
    def save_to_json(self, filename):
        data = {'num_tiles_x': self.num_tiles_x, 'num_tiles_y': self.num_tiles_y, 'tiles': [[tile.name for tile in row] for row in self.tiles]}
        with open(filename, 'w') as f:
            json.dump(data, f)

