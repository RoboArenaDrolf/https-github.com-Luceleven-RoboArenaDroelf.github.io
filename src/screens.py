class Screens:
    class MenuItem:
        def __init__(self, text, textcolor, font, dist_mult, display_resolution, dist_between_elements):
            self.text = font.render(text, True, textcolor)
            self.rect = self.text.get_rect(
                center=(display_resolution[0] // 2, display_resolution[1] // 2 + dist_mult * dist_between_elements)
            )
            self.selected = False

        def draw(self, screen, pygame, color):
            color = (255, 0, 0) if self.selected else color
            pygame.draw.rect(screen, color, self.rect)
            screen.blit(self.text, self.rect)

    black = (0, 0, 0)
    white = (255, 255, 255)

    def __init__(self, pygame):
        self.display_resolution = pygame.display.get_window_size()
        self.dist_between_elements = self.display_resolution[1] / 20
        self.input_fields_x_size = self.display_resolution[0] / 12
        self.input_fields_y_size = self.display_resolution[1] / 33
        self.input_text_offset_x = self.display_resolution[0] / 200
        self.input_text_offset_y = self.display_resolution[1] / 200
        self.rect_inflate_x = self.display_resolution[0] / 50
        self.rect_inflate_y = self.display_resolution[1] / 50
        self.font_size_big = int(self.display_resolution[1] / 16)
        self.font_size_small = int(self.display_resolution[1] / 25)

    def death_screen(self, pygame, screen):
        screen.fill(self.black)

        font = pygame.font.Font(None, self.font_size_big)
        text = font.render("You Died!", True, (101, 28, 50))
        screen.blit(
            text,
            (
                self.display_resolution[0] // 2 - text.get_width() // 2,
                self.display_resolution[1] // 2 - text.get_height() // 2,
            ),
        )

        font = pygame.font.Font(None, self.font_size_small)
        menu_items = [
            self.MenuItem("Main Menu", self.black, font, 2, self.display_resolution, self.dist_between_elements),
            self.MenuItem("Quit Game", self.black, font, 3, self.display_resolution, self.dist_between_elements),
        ]

        for item in menu_items:
            item.draw(screen, pygame, self.white)

        return menu_items

    def pause_screen(self, pygame, screen):
        font = pygame.font.Font(None, self.font_size_big)
        text = font.render("Paused Game", True, self.black)
        screen.blit(
            text,
            (
                self.display_resolution[0] // 2 - text.get_width() // 2,
                self.display_resolution[1] // 2 - text.get_height() // 2,
            ),
        )

        font = pygame.font.Font(None, self.font_size_small)
        menu_items = [
            self.MenuItem("Resume", self.white, font, 1, self.display_resolution, self.dist_between_elements),
            self.MenuItem("Main Menu", self.white, font, 2, self.display_resolution, self.dist_between_elements),
            self.MenuItem("Quit Game", self.white, font, 3, self.display_resolution, self.dist_between_elements),
        ]

        for item in menu_items:
            item.draw(screen, pygame, self.black)

        return menu_items

    def main_menu(self, pygame, screen):
        screen.fill(self.white)

        font = pygame.font.Font(None, self.font_size_small)
        menu_items = [
            self.MenuItem("Play", self.white, font, 1, self.display_resolution, self.dist_between_elements),
            self.MenuItem("Build Arena", self.white, font, 2, self.display_resolution, self.dist_between_elements),
            self.MenuItem("Settings", self.white, font, 3, self.display_resolution, self.dist_between_elements),
            self.MenuItem("Exit", self.white, font, 4, self.display_resolution, self.dist_between_elements),
        ]

        for item in menu_items:
            item.draw(screen, pygame, self.black)

        return menu_items

    def settings_menu(self, pygame, screen, available_resolutions):
        screen.fill(self.white)

        font = pygame.font.Font(None, self.font_size_big)
        text = font.render("Settings", True, self.black)
        screen.blit(
            text,
            (
                self.display_resolution[0] // 2 - text.get_width() // 2,
                self.display_resolution[1] // 2 - text.get_height() // 2 - 3 * self.dist_between_elements,
            ),
        )

        menu_items = []
        font = pygame.font.Font(None, self.font_size_small)
        for i, res in enumerate(available_resolutions):
            menu_items.append(
                self.MenuItem(
                    f"{res[0]}x{res[1]}", self.white, font, i, self.display_resolution, self.dist_between_elements
                )
            )

        menu_items.append(
            self.MenuItem("Fullscreen", self.white, font, 4, self.display_resolution, self.dist_between_elements)
        )
        menu_items.append(
            self.MenuItem("Back", self.white, font, 5, self.display_resolution, self.dist_between_elements)
        )

        for item in menu_items:
            item.draw(screen, pygame, self.black)

        return menu_items

    def build_arena_menu(self, pygame, screen, x_tiles, y_tiles):
        screen.fill(self.white)

        font = pygame.font.Font(None, self.font_size_big)
        text = font.render("Number x tiles:", True, self.black)
        screen.blit(
            text,
            (
                self.display_resolution[0] // 2 - text.get_width() // 2,
                self.display_resolution[1] // 2 - text.get_height() // 2 - 2 * self.dist_between_elements,
            ),
        )

        # Set up text input field for number x tiles
        input_rect_x_tiles = pygame.Rect(
            self.display_resolution[0] // 2 - text.get_width() // 2,
            self.display_resolution[1] // 2 - text.get_height() // 2 - self.dist_between_elements,
            self.input_fields_x_size,
            self.input_fields_y_size,
        )

        pygame.draw.rect(screen, self.black, input_rect_x_tiles)
        text_surface = pygame.font.SysFont(None, 24).render(x_tiles, True, self.white)
        screen.blit(
            text_surface,
            (input_rect_x_tiles.x + self.input_text_offset_x, input_rect_x_tiles.y + self.input_text_offset_y),
        )

        font = pygame.font.Font(None, self.font_size_big)
        text = font.render("Number y tiles:", True, self.black)
        screen.blit(
            text,
            (
                self.display_resolution[0] // 2 - text.get_width() // 2,
                self.display_resolution[1] // 2 - text.get_height() // 2,
            ),
        )

        # Set up text input field for number y tiles
        input_rect_y_tiles = pygame.Rect(
            self.display_resolution[0] // 2 - text.get_width() // 2,
            self.display_resolution[1] // 2 - text.get_height() // 2 + self.dist_between_elements,
            self.input_fields_x_size,
            self.input_fields_y_size,
        )

        pygame.draw.rect(screen, self.black, input_rect_y_tiles)
        text_surface = pygame.font.SysFont(None, 24).render(y_tiles, True, self.white)
        screen.blit(
            text_surface,
            (input_rect_y_tiles.x + self.input_text_offset_x, input_rect_y_tiles.y + self.input_text_offset_y),
        )

        font = pygame.font.Font(None, self.font_size_small)
        menu_items = [
            self.MenuItem("Start Building", self.white, font, 3, self.display_resolution, self.dist_between_elements)
        ]

        for item in menu_items:
            item.draw(screen, pygame, self.black)

        return input_rect_x_tiles, input_rect_y_tiles, menu_items

    def start_screen(self, pygame, screen):
        screen.fill(self.white)

        font = pygame.font.Font(None, self.font_size_big)
        text = font.render("Wie viele Spieler?", True, self.black)
        screen.blit(
            text,
            (
                self.display_resolution[0] // 2 - text.get_width() // 2,
                self.display_resolution[1] // 2 - text.get_height() // 2 - 2 * self.dist_between_elements,
            ),
        )

        font = pygame.font.Font(None, self.font_size_small)
        menu_items = [
            self.MenuItem("1", self.white, font, 1, self.display_resolution, self.dist_between_elements),
            self.MenuItem("2", self.white, font, 2, self.display_resolution, self.dist_between_elements),
            self.MenuItem("3", self.white, font, 3, self.display_resolution, self.dist_between_elements),
            self.MenuItem("4", self.white, font, 4, self.display_resolution, self.dist_between_elements),
        ]

        for item in menu_items:
            item.draw(screen, pygame, self.black)

        return menu_items

    def level_menu(self, pygame, screen, json_filenames):
        screen.fill(self.white)

        font = pygame.font.Font(None, self.font_size_big)
        text = font.render("Welches Level möchten Sie spielen?", True, self.black)
        screen.blit(
            text,
            (
                self.display_resolution[0] // 2 - text.get_width() // 2,
                self.display_resolution[1] // 2 - text.get_height() // 2 - 3 * self.dist_between_elements,
            ),
        )

        # Hole die JSON- und PNG-Dateinamen
        # png_filenames = get_png_filenames(directory)

        menu_items = []
        maps = []
        # Anzeige der JSON-Dateinamen
        small_font = pygame.font.Font(None, self.font_size_small)
        for i, filename in enumerate(json_filenames):
            menu_items.append(
                self.MenuItem(filename, self.white, font, i, self.display_resolution, self.dist_between_elements)
            )
            maps.append(filename + ".json")

        for item in menu_items:
            item.draw(screen, pygame, self.black)

        return menu_items, maps
