import pygame as pg


class EntityGraphics:
    def __init__(self, coordinates: [pg.Vector2], color: pg.Color, width: int, height: int):
        self.coordinates = coordinates
        self.color = color
        self.width = width
        self.height = height

    def draw(self, screen):
        for coordinate in self.coordinates:
            pg.draw.rect(screen, self.color, [coordinate.x, coordinate.y, self.width, self.height])

    def update(self, coordinates: [pg.Vector2], color: pg.Color = None, width: int = None, height: int = None):
        self.coordinates = coordinates
        if color is not None:
            self.color = color
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
