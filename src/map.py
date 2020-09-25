import pygame
import pytmx as pytmx


class TiledMap(pygame.sprite.Sprite):
    def __init__(self, filename):
        """The map is an empty sprite for now"""
        super(TiledMap, self).__init__()
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

        self.image = pygame.Surface((self.width, self.height))
        self.__render(self.image)
        self.rect = self.image.get_rect()

    def __render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))
