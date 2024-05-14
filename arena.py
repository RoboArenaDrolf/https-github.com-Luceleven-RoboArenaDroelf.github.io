import json
from enum import Enum


class Arena:
    class TileType(Enum):
        """
        Enum of different tile types, value of tile represents its filename.
        """

        AIR = "Air.png"
        GRASS = "Grass.png"
        ICE = "Ice.png"
        SAND = "Sand.png"
        LAVA = "Lava.png"
        BIRCH = "Birch.png"
        LEAVES = "Leaves.png"

        @classmethod
        def set_values_to_pics(cls, pygame, base_path):
            """
            Sets the values of the Enum TileType to the loaded pictures specified by their filename.
            :param pygame: instance of pygame
            :param base_path: base path of picture directory, for example ".\\PixelArt\\"
            """
            for member in cls:
                member._value_ = pygame.image.load(base_path + member.value)

    tile_size = 50
    base_path = ".\\PixelArt\\"

    def __init__(self, filename, pygame):
        self.load_map_from_json(filename)
        self.TileType.set_values_to_pics(pygame, self.base_path)

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
                screen.blit(pygame.transform.scale(tile.value, (self.tile_size, self.tile_size)), (x, y))
                x += self.tile_size
            y += self.tile_size
