import json
from enum import Enum


class Arena:
    class TileType(Enum):
        """
        Enum of different tile types, value of tile represents its filename.
        """
        AIR = ("Air.png", False)
        GRASS = ("Grass.png", True)
        ICE = ("Ice.png", True)
        SAND = ("Sand.png", True)
        LAVA = ("Lava.png", True)
        BIRCH = ("Birch.png", True)
        LEAVES = ("Leaves.png", True)

        def __init__(self, filename, solid):
            self.filename = filename
            self.solid = solid
            self.image = None

        @classmethod
        def set_values_to_pics(cls, pygame, base_path):
            """
            Sets the images of the Enum TileType to the loaded pictures specified by their filename.
            :param pygame: instance of pygame
            :param base_path: base path of picture directory, for example ".\\PixelArt\\"
            """
            for member in cls:
                member.image = pygame.image.load(base_path + member.filename)

    tile_size = 50
    blocks_base_path = ".\\PixelArt\\"
    maps_base_path = ".\\Maps\\"

    def __init__(self, filename, pygame):
        self.load_map_from_json(filename)
        self.TileType.set_values_to_pics(pygame, self.blocks_base_path)

    def load_map_from_json(self, filename):
        try:
            self._load_map_from_json_helper(filename)
        except (
            FileNotFoundError,
            json.JSONDecodeError,
            UnicodeDecodeError,
            ValueError,
        ):
            print("File not found!")
            self._load_map_from_json_helper("emptyMap.json")

    def _load_map_from_json_helper(self, filename):
        with open(self.maps_base_path + filename, "r") as f:
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
                screen.blit(pygame.transform.scale(tile.image, (self.tile_size, self.tile_size)), (x, y))
                x += self.tile_size
            y += self.tile_size

    def is_solid(self, x_positions, y_positions):
        for x in x_positions:
            for y in y_positions:
                if x < 0 or y < 0 or x >= self.num_tiles_x or y >= self.num_tiles_y:
                    return False
                elif self.tiles[y][x].solid:
                    return True
        return False
