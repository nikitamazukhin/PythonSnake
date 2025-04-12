import pygame as pg

from game.Classes.Graphics.entity_graphics import EntityGraphics


class Entity:
    def __init__(self, coordinates: list[pg.Vector2], entity_graphics: EntityGraphics = None):
        self.coordinates = coordinates
        self.graphics = entity_graphics

    def set_graphics(self, entity_graphics: EntityGraphics):
        self.graphics = entity_graphics

    def get_coordinates(self):
        return self.coordinates

    def set_coordinates(self, coordinates: list[pg.Vector2]):
        self.coordinates = coordinates
        self.graphics.update(coordinates)
