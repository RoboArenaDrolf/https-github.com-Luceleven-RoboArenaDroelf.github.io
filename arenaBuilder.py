import json
from arena import Arena


class ArenaBuilder(Arena):

    # Set up colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 200, 0)
    GREY = (100, 100, 100)

    def __init__(self, num_tiles_x, num_tiles_y, pygame):
        filename = self._set_up_empty_map(num_tiles_x, num_tiles_y)
        self._set_up_basics(filename, pygame)
        self._set_up_paint_related()

    def _set_up_empty_map(self, num_tiles_x, num_tiles_y):
        self.num_tiles_x = num_tiles_x
        self.num_tiles_y = num_tiles_y
        self.tiles = [
            [self.TileType.AIR for _ in range(self.num_tiles_x)]
            for _ in range(self.num_tiles_y)
        ]
        filename = "emptyMap.json"
        self.save_to_json(filename)
        return filename

    def _set_up_basics(self, filename, pygame):
        super().__init__(filename, pygame)
        self.pygame = pygame
        self.screen = self.pygame.display.set_mode(
            (self.num_tiles_x * self.tile_size + 200, self.num_tiles_y * self.tile_size)
        )

    def _set_up_paint_related(self):
        self._x_placing_of_legend = self.num_tiles_x * self.tile_size
        # Set up font
        self._font = self.pygame.font.SysFont(None, 24)
        self._text_color = self.WHITE
        # Set up text input field for saving
        self._input_text_saving = ""
        self._input_active_saving = False
        self._input_rect_saving = self.pygame.Rect(
            self._x_placing_of_legend + 20, 250, 160, 30
        )
        # Set up save button
        self._save_button_text = self._font.render("Save Map", True, self.WHITE)
        self._save_button_rect = self.pygame.Rect(
            self._x_placing_of_legend + 20, 300, 160, 40
        )
        # Set up text input field for loading
        self._input_text_loading = ""
        self._input_active_loading = False
        self._input_rect_loading = self.pygame.Rect(
            self._x_placing_of_legend + 20, 350, 160, 30
        )
        # Set up load button
        self._load_button_text = self._font.render("Load Map", True, self.WHITE)
        self._load_button_rect = self.pygame.Rect(
            self._x_placing_of_legend + 20, 400, 160, 40
        )

    def main(self):
        running = True
        current_tile = self.TileType.GRASS
        mouse_pressed = False
        save_button_clicked = False
        load_button_clicked = False
        button_click_time_saving = 0
        button_click_time_loading = 0

        # Main loop
        while running:
            # Clear the self.screen
            self.screen.fill(self.BLACK)

            # Paint the arenaBuilder
            self._paint_arena_builder(save_button_clicked, load_button_clicked)

            # Update the display
            self.pygame.display.flip()

            current_time = self.pygame.time.get_ticks()

            # Handle events
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                elif (
                    event.type == self.pygame.MOUSEBUTTONDOWN and event.button == 1
                ):  # Left mouse button
                    (
                        button_click_time_loading,
                        button_click_time_saving,
                        load_button_clicked,
                        mouse_pressed,
                        save_button_clicked,
                    ) = self._handle_mouse_button_down(
                        button_click_time_loading,
                        button_click_time_saving,
                        current_time,
                        load_button_clicked,
                        save_button_clicked,
                    )
                elif (
                    event.type == self.pygame.MOUSEBUTTONUP and event.button == 1
                ):  # Left mouse button released
                    mouse_pressed = False
                elif event.type == self.pygame.KEYDOWN:
                    current_tile = self._handle_key_down(current_tile, event)

            if mouse_pressed:
                self._paint_tile(current_tile)

            if save_button_clicked and current_time - button_click_time_saving >= 200:
                save_button_clicked = False

            if load_button_clicked and current_time - button_click_time_loading >= 200:
                load_button_clicked = False

    def _paint_tile(self, current_tile):
        x, y = self.pygame.mouse.get_pos()
        x //= self.tile_size
        y //= self.tile_size
        if x < self.num_tiles_x and y < self.num_tiles_y:
            self.set_tile(x, y, current_tile)

    def _handle_key_down(self, current_tile, event):
        if self._input_active_saving:
            if event.key == self.pygame.K_RETURN:
                self._input_active_saving = False
                self._save_map()
            elif event.key == self.pygame.K_BACKSPACE:
                self._input_text_saving = self._input_text_saving[:-1]
            else:
                self._input_text_saving += event.unicode
        elif self._input_active_loading:
            if event.key == self.pygame.K_RETURN:
                self._input_active_loading = False
                self._load_map()
            elif event.key == self.pygame.K_BACKSPACE:
                self._input_text_loading = self._input_text_loading[:-1]
            else:
                self._input_text_loading += event.unicode
        elif event.key == self.pygame.K_1:
            current_tile = self.TileType.AIR
        elif event.key == self.pygame.K_2:
            current_tile = self.TileType.GRASS
        elif event.key == self.pygame.K_3:
            current_tile = self.TileType.ICE
        elif event.key == self.pygame.K_4:
            current_tile = self.TileType.SAND
        elif event.key == self.pygame.K_5:
            current_tile = self.TileType.LAVA
        elif event.key == self.pygame.K_6:
            current_tile = self.TileType.BIRCH
        elif event.key == self.pygame.K_7:
            current_tile = self.TileType.LEAVES
        return current_tile

    def _handle_mouse_button_down(
        self,
        button_click_time_loading,
        button_click_time_saving,
        current_time,
        load_button_clicked,
        save_button_clicked,
    ):
        mouse_pressed = True
        mouse_pos = self.pygame.mouse.get_pos()
        if self._save_button_rect.collidepoint(mouse_pos):
            save_button_clicked = True
            button_click_time_saving = current_time
            self._save_map()
        elif self._load_button_rect.collidepoint(mouse_pos):
            load_button_clicked = True
            button_click_time_loading = current_time
            self._load_map()
        elif self._input_rect_saving.collidepoint(mouse_pos):
            self._input_active_saving = True
            self._input_active_loading = False
        elif self._input_rect_loading.collidepoint(mouse_pos):
            self._input_active_loading = True
            self._input_active_saving = False
        else:
            self._input_active_saving = False
            self._input_active_loading = False
        return (
            button_click_time_loading,
            button_click_time_saving,
            load_button_clicked,
            mouse_pressed,
            save_button_clicked,
        )

    def _load_map(self):
        map_name = self._input_text_loading
        filename = map_name + ".json"
        self._set_up_basics(filename, self.pygame)
        self._set_up_paint_related()
        self._input_text_saving = map_name

    def _save_map(self):
        self.save_to_json(self._input_text_saving + ".json")

    def _paint_arena_builder(self, save_button_clicked, load_button_clicked):
        """
        Paints the arena defined by tiles with a grid
        and a legend of possible tiles as well as other fields
        """
        self.paint_arena(self.pygame, self.screen)
        self._draw_grid()
        self._draw_legend()
        self._draw_input_fields()
        self._draw_buttons(load_button_clicked, save_button_clicked)

    def _draw_buttons(self, load_button_clicked, save_button_clicked):
        # Draw save button
        if save_button_clicked:
            self.pygame.draw.rect(self.screen, self.DARK_GREEN, self._save_button_rect)
        else:
            self.pygame.draw.rect(self.screen, self.GREEN, self._save_button_rect)
        self.screen.blit(
            self._save_button_text,
            (self._save_button_rect.x + 10, self._save_button_rect.y + 10),
        )
        # Draw load button
        if load_button_clicked:
            self.pygame.draw.rect(self.screen, self.DARK_GREEN, self._load_button_rect)
        else:
            self.pygame.draw.rect(self.screen, self.GREEN, self._load_button_rect)
        self.screen.blit(
            self._load_button_text,
            (self._load_button_rect.x + 10, self._load_button_rect.y + 10),
        )

    def _draw_input_fields(self):
        # Draw text input field saving
        self.pygame.draw.rect(self.screen, self.BLACK, self._input_rect_saving)
        self.pygame.draw.rect(self.screen, self._text_color, self._input_rect_saving, 2)
        text_surface = self._font.render(
            self._input_text_saving, True, self._text_color
        )
        self.screen.blit(
            text_surface, (self._input_rect_saving.x + 5, self._input_rect_saving.y + 5)
        )
        # Draw text input field loading
        self.pygame.draw.rect(self.screen, self.BLACK, self._input_rect_loading)
        self.pygame.draw.rect(
            self.screen, self._text_color, self._input_rect_loading, 2
        )
        text_surface = self._font.render(
            self._input_text_loading, True, self._text_color
        )
        self.screen.blit(
            text_surface,
            (self._input_rect_loading.x + 5, self._input_rect_loading.y + 5),
        )

    def _draw_legend(self):
        legend_surface = self.pygame.Surface((200, self.screen.get_height()))
        legend_surface.fill((0, 0, 0))
        legend_pos = (self._x_placing_of_legend + 20, 10)
        legend_spacing = 20
        for idx, tile_type in enumerate(self.TileType):
            legend_text = f"{idx + 1}: {tile_type.name}"
            text_surface = self._font.render(legend_text, True, self._text_color)
            legend_surface.blit(
                text_surface, (10, legend_pos[1] + idx * legend_spacing)
            )
        self.screen.blit(legend_surface, (self._x_placing_of_legend, 0))

    def _draw_grid(self):
        for x in range(0, self._x_placing_of_legend, self.tile_size):
            self.pygame.draw.line(
                self.screen, self.GREY, (x, 0), (x, self.screen.get_height())
            )
        for y in range(0, self.screen.get_height(), self.tile_size):
            self.pygame.draw.line(
                self.screen, self.GREY, (0, y), (self.screen.get_width(), y)
            )

    def set_tile(self, x, y, tile_type):
        self.tiles[y][x] = tile_type

    # Speichere die Daten in einer JSON-Datei
    def save_to_json(self, filename):
        data = {
            "num_tiles_x": self.num_tiles_x,
            "num_tiles_y": self.num_tiles_y,
            "tiles": [[tile.name for tile in row] for row in self.tiles],
        }
        with open(filename, "w") as f:
            json.dump(data, f)
