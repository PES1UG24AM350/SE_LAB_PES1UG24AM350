import pygame
import random


LANE_W = 80


COLORS = [
    (220, 60, 60),
    (220, 140, 40),
    (140, 60, 180),
    (60, 180, 80),
    (180, 180, 40),
    (60, 80, 200)
]


class Car:
    def __init__(self, lane_x, y, direction, speed):
        self.rect = pygame.Rect(
            lane_x + 10,
            y,
            60,
            80
        )

        self.direction = direction
        self.speed = speed
        self.color = random.choice(COLORS)

    def update(self):
        self.rect.y += self.direction * self.speed

    def off_screen(self, height):
        return (
            self.rect.top > height + 100
            or self.rect.bottom < -100
        )

    def draw(self, screen):
        # Car body
        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=8
        )

        # Window
        pygame.draw.rect(
            screen,
            (180, 220, 240),
            pygame.Rect(
                self.rect.x + 8,
                self.rect.y + 10,
                44,
                22
            ),
            border_radius=4
        )

        # Wheels
        for wx in [
            self.rect.x + 6,
            self.rect.right - 16
        ]:
            for wy in [
                self.rect.y + 4,
                self.rect.bottom - 16
            ]:
                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    pygame.Rect(
                        wx,
                        wy,
                        10,
                        12
                    ),
                    border_radius=3
                )


def make_car(lane_idx, height, speed):
    x = lane_idx * LANE_W

    direction = 1 if lane_idx % 2 == 0 else -1

    if direction == 1:
        y = -90
    else:
        y = height + 10

    return Car(
        x,
        y,
        direction,
        speed
    )


class Log:
    """
    Moving log used for Task 2.

    The player can stand on the log and gets
    carried along with it.
    """

    HEIGHT = 44

    def __init__(self, x, y, width, speed):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            self.HEIGHT
        )

        self.speed = speed

    def update(self, screen_width):
        self.rect.x += self.speed

        # Wrap from right to left
        if self.speed > 0:
            if self.rect.left > screen_width:
                self.rect.right = 0

        # Wrap from left to right
        else:
            if self.rect.right < 0:
                self.rect.left = screen_width

    def draw(self, screen):
        # Main wooden body
        pygame.draw.rect(
            screen,
            (120, 65, 30),
            self.rect,
            border_radius=12
        )

        # Wooden highlight
        pygame.draw.line(
            screen,
            (170, 100, 55),
            (
                self.rect.left + 15,
                self.rect.centery - 8
            ),
            (
                self.rect.right - 15,
                self.rect.centery - 8
            ),
            4
        )

        # Second wooden line
        pygame.draw.line(
            screen,
            (95, 48, 22),
            (
                self.rect.left + 15,
                self.rect.centery + 8
            ),
            (
                self.rect.right - 15,
                self.rect.centery + 8
            ),
            3
        )

        # Left end
        pygame.draw.circle(
            screen,
            (80, 40, 20),
            (
                self.rect.left + 12,
                self.rect.centery
            ),
            8
        )

        # Right end
        pygame.draw.circle(
            screen,
            (80, 40, 20),
            (
                self.rect.right - 12,
                self.rect.centery
            ),
            8
        )
