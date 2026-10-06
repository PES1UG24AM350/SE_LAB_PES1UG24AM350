import pygame


SPEED = 4
LANE_W = 80


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x - 20,
            y - 30,
            40,
            60
        )

        self.color = (60, 160, 220)

        # Prevents very fast left/right movement
        self.move_cooldown = 0

    def move(self, keys, min_x, max_x):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        else:
            dx = 0
            dy = 0

            # Horizontal movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -LANE_W

            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = LANE_W

            # Vertical movement
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -8

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 8

            # Apply horizontal movement
            if dx != 0:
                new_x = self.rect.x + dx

                new_x = max(
                    min_x,
                    min(max_x - self.rect.width, new_x)
                )

                self.rect.x = new_x
                self.move_cooldown = 12

            # Apply vertical movement
            if dy != 0:
                self.rect.y += dy

                # Don't allow player above screen
                if self.rect.top < 0:
                    self.rect.top = 0

                # Don't allow player below screen
                if self.rect.bottom > 600:
                    self.rect.bottom = 600

    def draw(self, screen):
        # Body
        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=8
        )

        # Windshield
        pygame.draw.rect(
            screen,
            (180, 220, 240),
            pygame.Rect(
                self.rect.x + 6,
                self.rect.y + 8,
                28,
                18
            ),
            border_radius=4
        )

        # Wheels
        for wx in [
            self.rect.x + 4,
            self.rect.right - 12
        ]:
            for wy in [
                self.rect.y + 4,
                self.rect.bottom - 14
            ]:
                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    pygame.Rect(
                        wx,
                        wy,
                        8,
                        10
                    ),
                    border_radius=3
                )
