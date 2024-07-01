import tkinter as tk
from tkinter import messagebox


class Screens:

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
        text_main_menu = font.render("Main Menu", True, self.black)
        text_quit = font.render("Quit Game", True, self.black)

        main_menu_rect = text_main_menu.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 2 * self.dist_between_elements)
        )
        quit_rect = text_quit.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 3 * self.dist_between_elements)
        )

        pygame.draw.rect(screen, self.white, main_menu_rect)
        pygame.draw.rect(screen, self.white, quit_rect)

        screen.blit(text_main_menu, main_menu_rect)
        screen.blit(text_quit, quit_rect)

        return quit_rect, main_menu_rect

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
        text_resume = font.render("Resume", True, self.white)
        text_main_menu = font.render("Main Menu", True, self.white)
        text_quit = font.render("Quit Game", True, self.white)

        resume_rect = text_resume.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + self.dist_between_elements)
        )
        main_menu_rect = text_main_menu.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 2 * self.dist_between_elements)
        )
        quit_rect = text_quit.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 3 * self.dist_between_elements)
        )

        pygame.draw.rect(screen, self.black, resume_rect)
        pygame.draw.rect(screen, self.black, main_menu_rect)
        pygame.draw.rect(screen, self.black, quit_rect)

        screen.blit(text_resume, resume_rect)
        screen.blit(text_main_menu, main_menu_rect)
        screen.blit(text_quit, quit_rect)

        return resume_rect, quit_rect, main_menu_rect

    def main_menu(self, pygame, screen):
        screen.fill(self.white)

        font = pygame.font.Font(None, self.font_size_small)
        play_text = font.render("Play", True, self.white)
        build_arena_text = font.render("Build Arena", True, self.white)
        settings_text = font.render("Settings", True, self.white)
        exit_text = font.render("Exit", True, self.white)

        play_rect = play_text.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + self.dist_between_elements)
        )
        build_arena_rect = build_arena_text.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 2 * self.dist_between_elements)
        )
        settings_rect = settings_text.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 3 * self.dist_between_elements)
        )
        exit_rect = exit_text.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 4 * self.dist_between_elements)
        )

        pygame.draw.rect(screen, self.black, play_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        pygame.draw.rect(screen, self.black, build_arena_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        pygame.draw.rect(screen, self.black, settings_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        pygame.draw.rect(screen, self.black, exit_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))

        screen.blit(play_text, play_rect)
        screen.blit(build_arena_text, build_arena_rect)
        screen.blit(settings_text, settings_rect)
        screen.blit(exit_text, exit_rect)

        return play_rect, build_arena_rect, exit_rect, settings_rect

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

        resolution_rects = []
        font = pygame.font.Font(None, self.font_size_small)
        for i, res in enumerate(available_resolutions):
            res_text = font.render(f"{res[0]}x{res[1]}", True, self.white)
            res_rect = res_text.get_rect(
                center=(
                    self.display_resolution[0] // 2,
                    self.display_resolution[1] // 2 - self.dist_between_elements + i * self.dist_between_elements,
                )
            )
            pygame.draw.rect(screen, self.black, res_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
            screen.blit(res_text, res_rect)
            resolution_rects.append(res_rect)

        fullscreen_text = font.render("Fullscreen", True, self.white)
        fullscreen_rect = fullscreen_text.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 3 * self.dist_between_elements)
        )
        pygame.draw.rect(screen, self.black, fullscreen_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        screen.blit(fullscreen_text, fullscreen_rect)

        back_text = font.render("Back", True, self.white)
        back_rect = fullscreen_text.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 4 * self.dist_between_elements)
        )
        pygame.draw.rect(screen, self.black, back_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        screen.blit(back_text, back_rect)

        return resolution_rects, fullscreen_rect, back_rect

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
        start_building_text = font.render("Start Building", True, self.white)

        start_building_rect = start_building_text.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 3 * self.dist_between_elements)
        )

        pygame.draw.rect(screen, self.black, start_building_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))

        screen.blit(start_building_text, start_building_rect)

        return input_rect_x_tiles, input_rect_y_tiles, start_building_rect

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
        one_player = font.render("1", True, self.white)
        two_player = font.render("2", True, self.white)
        three_player = font.render("3", True, self.white)
        four_player = font.render("4", True, self.white)

        one_player_rect = one_player.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + self.dist_between_elements)
        )
        two_player_rect = two_player.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 2 * self.dist_between_elements)
        )
        three_player_rect = three_player.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 3 * self.dist_between_elements)
        )
        four_player_rect = four_player.get_rect(
            center=(self.display_resolution[0] // 2, self.display_resolution[1] // 2 + 4 * self.dist_between_elements)
        )

        pygame.draw.rect(screen, self.black, one_player_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        pygame.draw.rect(screen, self.black, two_player_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        pygame.draw.rect(screen, self.black, three_player_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
        pygame.draw.rect(screen, self.black, four_player_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))

        screen.blit(one_player, one_player_rect)
        screen.blit(two_player, two_player_rect)
        screen.blit(three_player, three_player_rect)
        screen.blit(four_player, four_player_rect)

        return one_player_rect, two_player_rect, three_player_rect, four_player_rect

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

        level_rects = []
        maps = []
        # Anzeige der JSON-Dateinamen
        small_font = pygame.font.Font(None, self.font_size_small)
        for index, filename in enumerate(json_filenames):
            level_text = small_font.render(filename, True, self.white)
            level_rect = level_text.get_rect(
                center=(
                    self.display_resolution[0] // 2,
                    self.display_resolution[1] // 2 - self.dist_between_elements + index * self.dist_between_elements,
                )
            )
            pygame.draw.rect(screen, self.black, level_rect.inflate(self.rect_inflate_x, self.rect_inflate_y))
            screen.blit(level_text, level_rect)
            level_rects.append(level_rect)
            maps.append(filename + ".json")

        return level_rects, maps

    @staticmethod
    def show_popup(message):
        root = tk.Tk()
        root.withdraw()  # Verstecke das Haupt-Tkinter-Fenster
        messagebox.showinfo("", message)
        root.destroy()
