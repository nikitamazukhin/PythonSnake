import pygame as pg

from game.Classes.Graphics.entity_graphics import EntityGraphics
from game.Classes.entity import Entity
from game.Enums.direction import Direction


class Snake(Entity):
    def __init__(
            self,
            coordinates: [pg.Vector2],
            direction: Direction,
            step_size: int = 0,
            entity_graphics: EntityGraphics = None
    ):
        super().__init__(coordinates, entity_graphics)
        self.direction = direction
        self.step_size = step_size

    def get_direction(self):
        return self.direction

    def set_direction(self, direction: Direction):
        self.direction = direction

    def get_head_coordinates(self):
        return self.coordinates[-1]

    def get_length(self):
        return len(self.coordinates)

    def move(self):
        snake_head_coordinates = self.get_head_coordinates()

        if self.direction == Direction.UP:
            self.coordinates.append(pg.Vector2(snake_head_coordinates.x, snake_head_coordinates.y - self.step_size))
        elif self.direction == Direction.RIGHT:
            self.coordinates.append(pg.Vector2(snake_head_coordinates.x + self.step_size, snake_head_coordinates.y))
        elif self.direction == Direction.DOWN:
            self.coordinates.append(pg.Vector2(snake_head_coordinates.x, snake_head_coordinates.y + self.step_size))
        else:
            self.coordinates.append(pg.Vector2(snake_head_coordinates.x - self.step_size, snake_head_coordinates.y))

        self.coordinates.pop(0)

    def check_self_collision(self):
        snake_head_coordinates = self.get_head_coordinates()
        for segment in self.coordinates[:len(self.coordinates) - 1]:
            if snake_head_coordinates.x == segment.x and snake_head_coordinates.y == segment.y:
                return True
        return False
