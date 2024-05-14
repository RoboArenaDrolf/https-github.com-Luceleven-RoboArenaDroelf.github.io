import json
from enum import Enum


class Arena:
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

    tile_size = 50

    def __init__(self, filename):
        self.load_map_from_json(filename)

    def load_map_from_json(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.num_tiles_x = data["num_tiles_x"]
                self.num_tiles_y = data["num_tiles_y"]
                self.tiles = [
                    [Arena.TileType[tile] for tile in row] for row in data["tiles"]
                ]
        except (
            FileNotFoundError,
            json.JSONDecodeError,
            UnicodeDecodeError,
            ValueError,
        ):
            print("File not found!")
            with open("emptyMap.json", "r") as f:
                data = json.load(f)
                self.num_tiles_x = data["num_tiles_x"]
                self.num_tiles_y = data["num_tiles_y"]
                self.tiles = [
                    [Arena.TileType[tile] for tile in row] for row in data["tiles"]
                ]

    def paint_arena(self, pygame, screen):
        """
        Paints the arena with help of parameters pygame and screen.

        :param pygame: pygame instance
        :param screen: screen element of pygame initialized with pygame.display.set_mode()
        """
        y = 0
        for row in self.tiles:
            x = 0
            for tile in row:
                pygame.draw.rect(
                    screen, tile.value, [x, y, self.tile_size, self.tile_size]
                )
                x += self.tile_size
            y += self.tile_size
