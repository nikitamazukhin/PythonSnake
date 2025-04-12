import configparser
import os
import random

import pygame as pg
import asyncio
from game.Enums.direction import Direction
from game.Enums.game_state import GameState
from game.Classes.entity import Entity
from game.Classes.snake import Snake
from game.Classes.Graphics.entity_graphics import EntityGraphics
from game.Classes.Graphics.text_graphics import TextGraphics


def draw_text_graphics(text_graphics_list: list[TextGraphics], screen: pg.Surface):
    for text_graphic in text_graphics_list:
        text_graphic.draw(screen)


def check_fatal_collisions(snake: Snake, screen: pg.Surface):
    snake_head_coordinates = snake.get_head_coordinates()
    return (
            snake_head_coordinates.x >= screen.get_width()
            or snake_head_coordinates.x < 0
            or snake_head_coordinates.y >= screen.get_height()
            or snake_head_coordinates.y < 0
            or snake.check_self_collision()
    )


def check_food_collision(snake: Snake, food: Entity):
    snake_head_coordinates = snake.get_head_coordinates()
    food_coordinates = food.get_coordinates()[0]
    return snake_head_coordinates.x == food_coordinates.x and snake_head_coordinates.y == food_coordinates.y


def snake_eats(snake: Snake, food: Entity, screen: pg.Surface, cell_size):
    food_coordinates = food.get_coordinates()[0]
    snake.coordinates.append(pg.Vector2(food_coordinates.x, food_coordinates.y))
    food.set_coordinates([pg.Vector2(
        round((random.randrange(0, screen.get_width() - cell_size) / 10.0)) * 10,
        round((random.randrange(0, screen.get_height() - cell_size) / 10.0)) * 10
    )])


async def main():
    config_parser = configparser.RawConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), "config.ini")
    config_parser.read(config_file_path)

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()

    screen = pg.display.set_mode((
        config_parser.getint("window", "width"),
        config_parser.getint("window", "height")
    ))
    pg.display.set_caption(config_parser.get("window", "caption"))

    clock = pg.time.Clock()
    game_speed = config_parser.getint("game", "speed")

    font = pg.font.Font(
        config_parser.get("font", "path"),
        int(config_parser.get("font", "size"))
    )

    black = pg.Color(0, 0, 0)
    white = pg.Color(255, 255, 255)
    red = pg.Color(225, 0, 0)
    green = pg.Color(0, 225, 0)
    blue = pg.Color(0, 0, 225)

    cell_size = config_parser.getint("game", "cell_size")

    player_name = ""
    player_name_set = False
    grid_size = ""
    show_bad_grid_size_warning = False

    running = True
    game_state = GameState.TITLE

    movement_lock = False

    snake = None
    food = None

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif game_state == GameState.TITLE:
                    if event.key == pg.K_RETURN:
                        if not player_name_set:
                            player_name_set = True
                        else:
                            grid_size = int(grid_size)
                            if 5 <= grid_size <= 25:
                                screen = pg.display.set_mode((grid_size * 40, grid_size * 40))
                                snake = Snake(
                                    [pg.Vector2(screen.get_width() / 2, screen.get_height() / 2 + cell_size),
                                     pg.Vector2(screen.get_width() / 2, screen.get_height() / 2),
                                     pg.Vector2(screen.get_width() / 2, screen.get_height() / 2 - cell_size)],
                                    Direction.UP,
                                    cell_size,
                                )
                                snake.set_graphics(EntityGraphics(snake.coordinates, green, cell_size, cell_size))
                                food = Entity(
                                    [pg.Vector2(
                                        round((random.randrange(0, screen.get_width() - cell_size) / 10.0)) * 10,
                                        round((random.randrange(0, screen.get_height() - cell_size) / 10.0)) * 10
                                    )]
                                )
                                food.set_graphics(EntityGraphics(food.coordinates, red, cell_size, cell_size))
                                game_state = GameState.PLAYING
                            else:
                                show_bad_grid_size_warning = True
                                grid_size = ""
                    elif event.key == pg.K_BACKSPACE:
                        if not player_name_set:
                            player_name = player_name[:-1]
                        else:
                            grid_size = grid_size[:-1]
                    elif len(player_name) < 25 and not player_name_set:
                        player_name += event.unicode
                    elif len(grid_size) < 2 and event.unicode.isdigit():
                        grid_size += event.unicode

                elif game_state == GameState.PLAYING and not movement_lock:
                    if snake.get_direction() != Direction.DOWN and (event.key == pg.K_UP or event.key == pg.K_w):
                        snake.set_direction(Direction.UP)
                        movement_lock = True
                    elif snake.get_direction() != Direction.LEFT and (event.key == pg.K_RIGHT or event.key == pg.K_d):
                        snake.set_direction(Direction.RIGHT)
                        movement_lock = True
                    elif snake.get_direction() != Direction.UP and (event.key == pg.K_DOWN or event.key == pg.K_s):
                        snake.set_direction(Direction.DOWN)
                        movement_lock = True
                    elif snake.get_direction() != Direction.RIGHT and (event.key == pg.K_LEFT or event.key == pg.K_a):
                        snake.set_direction(Direction.LEFT)
                        movement_lock = True

        screen.fill("black")

        if game_state == GameState.TITLE:
            text_graphics_list = [
                TextGraphics(
                    "Snake",
                    green,
                    font,
                    (screen.get_width() / 2, screen.get_height() / 8)
                ),
                TextGraphics(
                    "Input your name" if not player_name_set else "Input grid size (5 - 25)",
                    green,
                    font,
                    (screen.get_width() / 2, screen.get_height() / 4)
                ),
                TextGraphics(
                    player_name if not player_name_set else grid_size,
                    blue,
                    font,
                    (screen.get_width() / 2, screen.get_height() / 2)
                )
            ]
            if show_bad_grid_size_warning:
                text_graphics_list.append(
                    TextGraphics(
                        "Incorrect grid size entered!",
                        red,
                        font,
                        (screen.get_width() / 2, screen.get_height() / 1.5)
                    )
                )
            draw_text_graphics(text_graphics_list, screen)

        elif game_state == GameState.PLAYING:
            if check_fatal_collisions(snake, screen):
                game_state = GameState.GAME_OVER
            else:
                if check_food_collision(snake, food):
                    snake_eats(snake, food, screen, cell_size)
                snake.move()
                movement_lock = False
                snake.graphics.draw(screen)
                food.graphics.draw(screen)
                TextGraphics("Score: " + str(snake.get_length() - 3), white, font).draw(screen)

        else:
            screen = pg.display.set_mode((
                config_parser.getint("window", "width"),
                config_parser.getint("window", "height")
            ))

            text_graphics_list = [
                TextGraphics(
                    "Game Over!",
                    green,
                    font,
                    (screen.get_width() / 2, screen.get_height() / 4)
                ),
                TextGraphics(
                    "Your final score is: " + str(snake.get_length() - 3),
                    green,
                    font,
                    (screen.get_width() / 2, screen.get_height() / 2)
                )
            ]
            draw_text_graphics(text_graphics_list, screen)

        pg.display.flip()
        clock.tick(game_speed)
        await asyncio.sleep(0)
    pg.quit()
    quit()

asyncio.run(main())
