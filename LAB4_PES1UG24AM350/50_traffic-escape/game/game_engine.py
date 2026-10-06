import pygame

from game.player import Player
from game.traffic import Car, Log, make_car


# ============================================================
# GAME SETTINGS
# ============================================================

LANES = 8

WIDTH = 640
HEIGHT = 600

FPS = 60

BG = (30, 150, 70)

LANE_W = 80


# ============================================================
# TASK 2 - WATER / LOG SETTINGS
# ============================================================

WATER_TOP = 220
WATER_BOTTOM = 320

LOG_Y = 260

# Player gets a small amount of time to find a log
# after entering the water.
WATER_GRACE_FRAMES = 15


class GameEngine:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Traffic Escape"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "arial",
            24
        )

        self.big_font = pygame.font.SysFont(
            "arial",
            52,
            bold=True
        )

        self.reset()

    # ========================================================
    # RESET GAME
    # ========================================================

    def reset(self):

        # Player
        self.player = Player(
            WIDTH // 2,
            HEIGHT - 80
        )

        # Cars
        self.cars = []

        # ----------------------------------------------------
        # TASK 2 - MOVING LOGS
        #
        # Wide overlapping logs make the lane playable.
        # They still move continuously.
        # ----------------------------------------------------

        self.logs = [
            Log(
                -80,
                LOG_Y,
                300,
                2
            ),

            Log(
                170,
                LOG_Y,
                300,
                -2
            ),

            Log(
                390,
                LOG_Y,
                300,
                2
            )
        ]

        # The log the player is currently riding
        self.riding_log = None

        # Water timer
        self.water_timer = 0

        # Car spawning
        self.timer = 0
        self.spawn_interval = 50

        # Difficulty
        self.speed = 3

        # Score
        self.score = 0

        # ====================================================
        # TASK 1 - LIVES
        # ====================================================

        self.lives = 3

        # Game states
        self.game_over = False
        self.won = False

    # ========================================================
    # PLAYER RESPAWN
    # ========================================================

    def respawn_player(self):

        self.player.rect.centerx = WIDTH // 2

        self.player.rect.bottom = HEIGHT - 30

        self.riding_log = None

        self.water_timer = 0

    # ========================================================
    # TASK 2 - WATER CHECK
    # ========================================================

    def is_in_water(self):

        return (
            self.player.rect.bottom > WATER_TOP
            and
            self.player.rect.top < WATER_BOTTOM
        )

    # ========================================================
    # TASK 2 - HORIZONTAL OVERLAP
    # ========================================================

    def horizontal_overlap(self, log):

        return (
            self.player.rect.right > log.rect.left
            and
            self.player.rect.left < log.rect.right
        )

    # ========================================================
    # TASK 2 - FIND LOG
    # ========================================================

    def find_log_under_player(self):

        for log in self.logs:

            if not self.horizontal_overlap(log):
                continue

            # Vertical overlap
            if (
                self.player.rect.bottom >= log.rect.top
                and
                self.player.rect.top <= log.rect.bottom
            ):
                return log

        return None

    # ========================================================
    # TASK 2 - BOARD LOG
    # ========================================================

    def board_log(self, log):

        self.riding_log = log

        # Put player's feet exactly on top of log
        self.player.rect.bottom = log.rect.top

        self.water_timer = 0

    # ========================================================
    # TASK 1 - LOSE LIFE
    # ========================================================

    def lose_life(self):

        self.lives -= 1

        self.riding_log = None

        self.water_timer = 0

        if self.lives <= 0:

            self.lives = 0

            self.game_over = True

        else:

            self.respawn_player()

    # ========================================================
    # TASK 1 - CAR COLLISION
    # ========================================================

    def check_car_collisions(self):

        # Don't collide with cars while inside the water.
        if self.is_in_water():
            return

        for car in self.cars:

            if self.player.rect.colliderect(car.rect):

                self.lose_life()

                # Remove the car that hit player
                if car in self.cars:
                    self.cars.remove(car)

                return

    # ========================================================
    # UPDATE LOGS
    # ========================================================

    def update_logs(self):

        # If player is riding a log, remember their position
        # relative to that log.
        riding = self.riding_log

        relative_x = None

        if riding is not None:

            relative_x = (
                self.player.rect.x
                - riding.rect.x
            )

        # Move every log
        for log in self.logs:

            log.update(WIDTH)

        # Carry player with the log
        if riding is not None:

            if relative_x is not None:

                self.player.rect.x = (
                    riding.rect.x
                    + relative_x
                )

                # Keep player inside screen
                if self.player.rect.right < 0:
                    self.player.rect.left = 0

                if self.player.rect.left > WIDTH:
                    self.player.rect.right = WIDTH

    # ========================================================
    # UPDATE PLAYER + LOG
    # ========================================================

    def update_player(self, keys):

        old_bottom = self.player.rect.bottom

        # Player movement
        self.player.move(
            keys,
            0,
            WIDTH
        )

        new_bottom = self.player.rect.bottom

        # ----------------------------------------------------
        # If already riding a log
        # ----------------------------------------------------

        if self.riding_log is not None:

            log = self.riding_log

            # If player moves horizontally completely
            # away from the log, stop riding it.
            if not self.horizontal_overlap(log):

                self.riding_log = None

            # If player goes down far below the log,
            # they have stepped/fallen off.
            elif self.player.rect.top > log.rect.bottom + 15:

                self.riding_log = None

            else:

                # Keep player standing on the log
                # unless they intentionally move upward.
                if (
                    self.player.rect.bottom >= log.rect.top
                    and
                    self.player.rect.bottom <= log.rect.bottom + 15
                ):
                    self.player.rect.bottom = log.rect.top

        # ----------------------------------------------------
        # If NOT riding a log, check whether player can board
        # one.
        # ----------------------------------------------------

        if self.riding_log is None:

            for log in self.logs:

                if not self.horizontal_overlap(log):
                    continue

                # Normal rectangle contact
                vertical_contact = (
                    self.player.rect.bottom >= log.rect.top
                    and
                    self.player.rect.top <= log.rect.bottom
                )

                # Detect crossing the top of the log
                landing_contact = (
                    old_bottom >= log.rect.top
                    and
                    new_bottom <= log.rect.top + 18
                )

                if vertical_contact or landing_contact:

                    self.board_log(log)

                    break

    # ========================================================
    # UPDATE WATER
    # ========================================================

    def update_water(self):

        # If riding a log, completely safe.
        if self.riding_log is not None:

            self.water_timer = 0

            return

        # If player is not in water, reset timer.
        if not self.is_in_water():

            self.water_timer = 0

            return

        # Player is in water without a log.
        self.water_timer += 1

        # Give player a short window to board a moving log.
        if self.water_timer >= WATER_GRACE_FRAMES:

            self.lose_life()

    # ========================================================
    # UPDATE CARS
    # ========================================================

    def update_cars(self):

        for car in self.cars:

            car.update()

    # ========================================================
    # SPAWN CARS
    # ========================================================

    def spawn_cars(self):

        self.timer += 1

        if self.timer < self.spawn_interval:
            return

        self.timer = 0

        # Choose random lane
        lane = pygame.time.get_ticks() % LANES

        car = make_car(
            lane,
            HEIGHT,
            self.speed
        )

        self.cars.append(car)

    # ========================================================
    # REMOVE OFF-SCREEN CARS
    # ========================================================

    def remove_offscreen_cars(self):

        self.cars = [
            car
            for car in self.cars
            if not car.off_screen(HEIGHT)
        ]

    # ========================================================
    # SCORE / DIFFICULTY
    # ========================================================

    def update_score(self):

        # Score based on player progress
        progress = HEIGHT - self.player.rect.y

        new_score = max(
            0,
            progress // 5
        )

        if new_score > self.score:

            self.score = new_score

        # Increase difficulty gradually
        self.speed = min(
            7,
            3 + self.score // 100
        )

    # ========================================================
    # CHECK WIN
    # ========================================================

    def check_win(self):

        if self.player.rect.top <= 10:

            self.won = True

    # ========================================================
    # UPDATE EVERYTHING
    # ========================================================

    def update(self):

        if self.game_over or self.won:
            return

        keys = pygame.key.get_pressed()

        # 1. Move logs
        self.update_logs()

        # 2. Move player
        self.update_player(keys)

        # 3. Water / log system
        self.update_water()

        # If water collision caused game over,
        # don't continue this frame.
        if self.game_over:
            return

        # 4. Cars
        self.spawn_cars()

        self.update_cars()

        # 5. Car collision
        self.check_car_collisions()

        if self.game_over:
            return

        # 6. Remove cars
        self.remove_offscreen_cars()

        # 7. Score
        self.update_score()

        # 8. Win
        self.check_win()

    # ========================================================
    # DRAW ROAD
    # ========================================================

    def draw_road(self):

        # Grass
        self.screen.fill(
            BG
        )

        # Road area
        road_rect = pygame.Rect(
            0,
            0,
            WIDTH,
            HEIGHT
        )

        pygame.draw.rect(
            self.screen,
            (55, 55, 55),
            road_rect
        )

        # Road lane markings
        for x in range(
            LANE_W,
            WIDTH,
            LANE_W
        ):

            pygame.draw.line(
                self.screen,
                (210, 210, 210),
                (x, 0),
                (x, WATER_TOP),
                2
            )

            pygame.draw.line(
                self.screen,
                (210, 210, 210),
                (x, WATER_BOTTOM),
                (x, HEIGHT),
                2
            )

    # ========================================================
    # DRAW WATER
    # ========================================================

    def draw_water(self):

        water_rect = pygame.Rect(
            0,
            WATER_TOP,
            WIDTH,
            WATER_BOTTOM - WATER_TOP
        )

        pygame.draw.rect(
            self.screen,
            (35, 120, 210),
            water_rect
        )

        # Water waves
        for y in range(
            WATER_TOP + 15,
            WATER_BOTTOM,
            25
        ):

            for x in range(
                10,
                WIDTH,
                60
            ):

                pygame.draw.line(
                    self.screen,
                    (100, 180, 240),
                    (x, y),
                    (x + 25, y),
                    2
                )

    # ========================================================
    # DRAW LOGS
    # ========================================================

    def draw_logs(self):

        for log in self.logs:

            log.draw(
                self.screen
            )

    # ========================================================
    # DRAW CARS
    # ========================================================

    def draw_cars(self):

        for car in self.cars:

            car.draw(
                self.screen
            )

    # ========================================================
    # DRAW HUD
    # ========================================================

    def draw_hud(self):

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )

        lives_text = self.font.render(
            f"Lives: {self.lives}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            score_text,
            (10, 10)
        )

        self.screen.blit(
            lives_text,
            (500, 10)
        )

    # ========================================================
    # DRAW GAME OVER
    # ========================================================

    def draw_game_over(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(150)

        overlay.fill(
            (0, 0, 0)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        text = self.big_font.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        text_rect = text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 30)
        )

        self.screen.blit(
            text,
            text_rect
        )

        restart = self.font.render(
            "Press R to restart",
            True,
            (255, 255, 255)
        )

        restart_rect = restart.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 35)
        )

        self.screen.blit(
            restart,
            restart_rect
        )

    # ========================================================
    # DRAW WIN
    # ========================================================

    def draw_win(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(150)

        overlay.fill(
            (0, 0, 0)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        text = self.big_font.render(
            "YOU WIN!",
            True,
            (100, 255, 100)
        )

        text_rect = text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 30)
        )

        self.screen.blit(
            text,
            text_rect
        )

        score = self.font.render(
            f"Final Score: {self.score}",
            True,
            (255, 255, 255)
        )

        score_rect = score.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 35)
        )

        self.screen.blit(
            score,
            score_rect
        )

    # ========================================================
    # DRAW EVERYTHING
    # ========================================================

    def draw(self):

        self.draw_road()

        self.draw_water()

        # Logs must be drawn before player
        self.draw_logs()

        self.draw_cars()

        self.player.draw(
            self.screen
        )

        self.draw_hud()

        if self.game_over:

            self.draw_game_over()

        elif self.won:

            self.draw_win()

        pygame.display.flip()

    # ========================================================
    # MAIN GAME LOOP
    # ========================================================

    def run(self):

        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False

                # Restart
                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_r
                ):

                    if self.game_over or self.won:

                        self.reset()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()
