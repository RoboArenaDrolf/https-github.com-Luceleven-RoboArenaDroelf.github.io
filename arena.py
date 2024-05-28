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
                # Load the image for each tile type and assign it to the member's value
                member._value_ = pygame.image.load(base_path + member.value)

    tile_size = 50
    base_path = ".\\PixelArt\\"

    def __init__(self, filename, pygame):
        # Load the map from the provided JSON file
        self.load_map_from_json(filename)
        # Set the images for each tile type
        self.TileType.set_values_to_pics(pygame, self.base_path)

    def load_map_from_json(self, filename):
        try:
            # Try to open and load the map data from the JSON file
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
            # Handle exceptions by loading a default empty map
            print("File not found or error in file!")
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
                # Draw each tile on the screen at the specified position
                screen.blit(pygame.transform.scale(tile.value, (self.tile_size, self.tile_size)), (x, y))
                x += self.tile_size
            y += self.tile_size
