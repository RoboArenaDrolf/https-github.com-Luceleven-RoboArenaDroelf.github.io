from enum import Enum

class Arena:
    class _TileType(Enum):
        """
        Enum of different tile types, value of tile represents it's color.
        """
        CONCRETE = (178,190,181)
        AIR = (255, 255, 255)
        GRASS = (0,107,60)
        ICE = (113,166,210)
        SAND = (237,201,175)
        LAVA = (207,16,32)


    _CO = _TileType.CONCRETE
    _GR = _TileType.GRASS
    _IC = _TileType.ICE
    _AI = _TileType.AIR
    _SA = _TileType.SAND
    _LA = _TileType.LAVA

    _tiles = [[_CO, _CO, _CO, _CO, _CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO, _CO, _CO, _CO, _CO, _AI, _AI, _AI],
              [_LA, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI],
              [_LA, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI],
              [_LA, _AI, _AI, _AI, _SA, _SA, _SA, _SA, _AI, _AI, _AI, _CO, _CO, _CO, _CO, _AI, _SA, _IC, _IC, _SA],
              [_CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO],
              [_AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _GR, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO],
              [_AI, _AI, _GR, _GR, _AI, _AI, _AI, _AI, _AI, _GR, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO],
              [_AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _GR, _AI, _AI, _AI, _AI, _CO, _CO, _AI, _AI, _CO],
              [_AI, _AI, _AI, _AI, _AI, _GR, _GR, _AI, _AI, _AI, _AI, _GR, _AI, _AI, _AI, _LA, _AI, _AI, _AI, _AI],
              [_CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _LA, _AI, _AI, _GR, _AI],
              [_CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _GR, _AI, _AI, _AI, _AI, _AI, _LA, _AI, _AI, _AI, _AI],
              [_CO, _AI, _AI, _CO, _CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO, _CO, _LA, _CO, _AI, _AI, _CO],
              [_AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _LA, _AI, _AI, _AI, _CO],
              [_AI, _AI, _AI, _AI, _IC, _IC, _IC, _CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _LA, _AI, _AI, _GR, _CO],
              [_AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO, _CO, _CO, _CO, _CO, _AI, _AI, _AI, _AI],
              [_CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _GR, _AI, _AI],
              [_CO, _GR, _GR, _GR, _GR, _GR, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI],
              [_CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO, _CO, _CO, _IC, _IC, _IC, _IC, _AI, _AI, _AI, _AI],
              [_CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _AI, _CO],
              [_CO, _AI, _AI, _AI, _AI, _CO, _CO, _CO, _CO, _CO, _AI, _AI, _AI, _AI, _AI, _CO, _CO, _CO, _CO, _CO]]
    _tile_size = 50

    def paint_arena(self, pygame, screen):
        """
        Paints the arena with help of parameters pygame and screen.

        Precond: Screen size has to be 1000 x 1000, throws a ValueError otherwise.
        :param pygame: pygame instance
        :param screen: screen element of pygame initialized with pygame.display.set_mode()
        :return:
        """
        if screen.get_size() != (1000, 1000):
            raise ValueError("Wrong screen size! Must be 1000x1000.")
        y = 0
        for row in self._tiles:
            x = 0
            for tile in row:
                pygame.draw.rect(screen, tile.value, [x, y, self._tile_size, self._tile_size])
                x += self._tile_size
            y += self._tile_size
