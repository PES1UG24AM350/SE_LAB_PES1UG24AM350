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
            or
            self.rect.bottom < -100
        )

    def draw(self, screen, night=False):

        # Car body
        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=8
        )

        # Windows
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

        # ====================================================
        # TASK 4 - NIGHT HEADLIGHTS
        # ====================================================

        if night:

            # Front of the car depends on direction.
            if self.direction > 0:

                headlights_y = self.rect.bottom - 8

            else:

                headlights_y = self.rect.top + 8

            left_headlight = pygame.Rect(
                self.rect.x + 10,
                headlights_y - 5,
                12,
                8
            )

            right_headlight = pygame.Rect(
                self.rect.right - 22,
                headlights_y - 5,
                12,
                8
            )

            pygame.draw.rect(
                screen,
                (255, 245, 150),
                left_headlight,
                border_radius=3
            )

            pygame.draw.rect(
                screen,
                (255, 245, 150),
                right_headlight,
                border_radius=3
            )

            # Headlight beams
            if self.direction > 0:

                beam_points_left = [
                    (
                        self.rect.x + 10,
                        self.rect.bottom
                    ),
                    (
                        self.rect.x - 15,
                        self.rect.bottom + 100
                    ),
                    (
                        self.rect.x + 30,
                        self.rect.bottom + 100
                    )
                ]

                beam_points_right = [
                    (
                        self.rect.right - 22,
                        self.rect.bottom
                    ),
                    (
                        self.rect.right - 5,
                        self.rect.bottom + 100
                    ),
                    (
                        self.rect.right - 45,
                        self.rect.bottom + 100
                    )
                ]

            else:

                beam_points_left = [
                    (
                        self.rect.x + 10,
                        self.rect.top
                    ),
                    (
                        self.rect.x - 15,
                        self.rect.top - 100
                    ),
                    (
                        self.rect.x + 30,
                        self.rect.top - 100
                    )
                ]

                beam_points_right = [
                    (
                        self.rect.right - 22,
                        self.rect.top
                    ),
                    (
                        self.rect.right - 5,
                        self.rect.top - 100
                    ),
                    (
                        self.rect.right - 45,
                        self.rect.top - 100
                    )
                ]

            # Transparent beam surfaces
            beam_surface = pygame.Surface(
                screen.get_size(),
                pygame.SRCALPHA
            )

            pygame.draw.polygon(
                beam_surface,
                (255, 245, 150, 35),
                beam_points_left
            )

            pygame.draw.polygon(
                beam_surface,
                (255, 245, 150, 35),
                beam_points_right
            )

            screen.blit(
                beam_surface,
                (0, 0)
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

        if self.speed > 0:

            if self.rect.left > screen_width:
                self.rect.right = 0

        else:

            if self.rect.right < 0:
                self.rect.left = screen_width

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (120, 65, 30),
            self.rect,
            border_radius=12
        )

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

        pygame.draw.circle(
            screen,
            (80, 40, 20),
            (
                self.rect.left + 12,
                self.rect.centery
            ),
            8
        )

        pygame.draw.circle(
            screen,
            (80, 40, 20),
            (
                self.rect.right - 12,
                self.rect.centery
            ),
            8
        )
