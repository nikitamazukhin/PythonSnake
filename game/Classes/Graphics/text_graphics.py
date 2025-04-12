import pygame as pg


class TextGraphics:
    def __init__(
            self,
            text: str,
            color: pg.Color,
            font: pg.font.Font,
            center: tuple[int, int] | tuple[float, float] = None
    ):
        self.text = text
        self.color = color
        self.font = font
        self.center = center

    def draw(self, surface: pg.Surface):
        rendered_font = self.font.render(self.text, True, self.color)
        rect = rendered_font.get_rect()

        if self.center is not None:
            rect.center = self.center

        surface.blit(rendered_font, rect)