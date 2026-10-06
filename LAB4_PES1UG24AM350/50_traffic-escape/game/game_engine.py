import pygame

from game.player import Player
from game.traffic import Log, make_car
from game.high_scores import save_score, get_high_scores


LANES = 8

WIDTH = 640
HEIGHT = 600

FPS = 60

LANE_W = 80


# ============================================================
# TASK 2
# ============================================================

WATER_TOP = 220
WATER_BOTTOM = 320

LOG_Y = 260

WATER_GRACE_FRAMES = 15


# ============================================================
# TASK 4
# ============================================================

DAY_DURATION = 10 * FPS


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

        self.small_font = pygame.font.SysFont(
            "arial",
            20
        )

        self.reset()

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.player = Player(
            WIDTH // 2,
            HEIGHT - 80
        )

        self.cars = []

        # ----------------------------------------------------
        # TASK 2 - LOGS
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

        self.riding_log = None

        self.water_timer = 0

        # Cars
        self.timer = 0
        self.spawn_interval = 50

        self.speed = 3

        # Score
        self.score = 0

        # Task 1
        self.lives = 3

        self.game_over = False
        self.won = False

        # Task 3
        self.score_saved = False
        self.high_scores = get_high_scores()

        # ====================================================
        # TASK 4 - DAY/NIGHT
        # ====================================================

        self.day_night_timer = 0

        self.is_night = False

    # ========================================================
    # TASK 1 - RESPAWN
    # ========================================================

    def respawn_player(self):

        self.player.rect.centerx = WIDTH // 2

        self.player.rect.bottom = HEIGHT - 30

        self.riding_log = None

        self.water_timer = 0

    # ========================================================
    # TASK 2 - WATER
    # ========================================================

    def is_in_water(self):

        return (
            self.player.rect.bottom > WATER_TOP
            and
            self.player.rect.top < WATER_BOTTOM
        )

    def horizontal_overlap(self, log):

        return (
            self.player.rect.right > log.rect.left
            and
            self.player.rect.left < log.rect.right
        )

    def board_log(self, log):

        self.riding_log = log

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

            self.save_final_score()

        else:

            self.respawn_player()

    # ========================================================
    # TASK 3 - SAVE SCORE
    # ========================================================

    def save_final_score(self):

        if self.score_saved:
            return

        self.high_scores = save_score(
            self.score
        )

        self.score_saved = True

    # ========================================================
    # CAR COLLISION
    # ========================================================

    def check_car_collisions(self):

        if self.is_in_water():
            return

        for car in self.cars:

            if self.player.rect.colliderect(
                car.rect
            ):

                self.lose_life()

                if car in self.cars:
                    self.cars.remove(car)

                return

    # ========================================================
    # LOG UPDATE
    # ========================================================

    def update_logs(self):

        riding = self.riding_log

        relative_x = None

        if riding is not None:

            relative_x = (
                self.player.rect.x
                - riding.rect.x
            )

        for log in self.logs:

            log.update(WIDTH)

        if riding is not None:

            self.player.rect.x = (
                riding.rect.x
                + relative_x
            )

            if self.player.rect.right < 0:
                self.player.rect.left = 0

            if self.player.rect.left > WIDTH:
                self.player.rect.right = WIDTH

    # ========================================================
    # PLAYER UPDATE
    # ========================================================

    def update_player(self, keys):

        old_bottom = self.player.rect.bottom

        self.player.move(
            keys,
            0,
            WIDTH
        )

        new_bottom = self.player.rect.bottom

        # Already on log
        if self.riding_log is not None:

            log = self.riding_log

            if not self.horizontal_overlap(log):

                self.riding_log = None

            elif self.player.rect.top > log.rect.bottom + 15:

                self.riding_log = None

            else:

                if (
                    self.player.rect.bottom >= log.rect.top
                    and
                    self.player.rect.bottom
                    <= log.rect.bottom + 15
                ):

                    self.player.rect.bottom = log.rect.top

        # Try to board log
        if self.riding_log is None:

            for log in self.logs:

                if not self.horizontal_overlap(log):
                    continue

                vertical_contact = (
                    self.player.rect.bottom >= log.rect.top
                    and
                    self.player.rect.top <= log.rect.bottom
                )

                landing_contact = (
                    old_bottom >= log.rect.top
                    and
                    new_bottom <= log.rect.top + 18
                )

                if (
                    vertical_contact
                    or
                    landing_contact
                ):

                    self.board_log(log)

                    break

    # ========================================================
    # WATER UPDATE
    # ========================================================

    def update_water(self):

        if self.riding_log is not None:

            self.water_timer = 0

            return

        if not self.is_in_water():

            self.water_timer = 0

            return

        self.water_timer += 1

        if self.water_timer >= WATER_GRACE_FRAMES:

            self.lose_life()

    # ========================================================
    # CAR UPDATE
    # ========================================================

    def update_cars(self):

        for car in self.cars:

            car.update()

    # ========================================================
    # CAR SPAWN
    # ========================================================

    def spawn_cars(self):

        self.timer += 1

        if self.timer < self.spawn_interval:
            return

        self.timer = 0

        lane = pygame.time.get_ticks() % LANES

        car = make_car(
            lane,
            HEIGHT,
            self.speed
        )

        self.cars.append(car)

    # ========================================================
    # REMOVE CARS
    # ========================================================

    def remove_offscreen_cars(self):

        self.cars = [
            car
            for car in self.cars
            if not car.off_screen(HEIGHT)
        ]

    # ========================================================
    # SCORE
    # ========================================================

    def update_score(self):

        progress = HEIGHT - self.player.rect.y

        new_score = max(
            0,
            progress // 5
        )

        if new_score > self.score:

            self.score = new_score

        self.speed = min(
            7,
            3 + self.score // 100
        )

    # ========================================================
    # WIN
    # ========================================================

    def check_win(self):

        if self.player.rect.top <= 10:

            self.won = True

            self.save_final_score()

    # ========================================================
    # TASK 4 - DAY/NIGHT TIMER
    # ========================================================

    def update_day_night(self):

        self.day_night_timer += 1

        if self.day_night_timer >= DAY_DURATION:

            self.day_night_timer = 0

            self.is_night = not self.is_night

    # ========================================================
    # MAIN UPDATE
    # ========================================================

    def update(self):

        if self.game_over or self.won:
            return

        keys = pygame.key.get_pressed()

        # Task 4
        self.update_day_night()

        # Task 2
        self.update_logs()

        self.update_player(keys)

        self.update_water()

        if self.game_over:
            return

        # Traffic
        self.spawn_cars()

        self.update_cars()

        self.check_car_collisions()

        if self.game_over:
            return

        self.remove_offscreen_cars()

        # Score
        self.update_score()

        # Win
        self.check_win()

    # ========================================================
    # DRAW ROAD
    # ========================================================

    def draw_road(self):

        if self.is_night:

            road_color = (20, 20, 28)

        else:

            road_color = (55, 55, 55)

        self.screen.fill(
            road_color
        )

        for x in range(
            LANE_W,
            WIDTH,
            LANE_W
        ):

            line_color = (
                (80, 80, 95)
                if self.is_night
                else
                (210, 210, 210)
            )

            pygame.draw.line(
                self.screen,
                line_color,
                (x, 0),
                (x, WATER_TOP),
                2
            )

            pygame.draw.line(
                self.screen,
                line_color,
                (x, WATER_BOTTOM),
                (x, HEIGHT),
                2
            )

    # ========================================================
    # DRAW WATER
    # ========================================================

    def draw_water(self):

        water_color = (
            (15, 65, 120)
            if self.is_night
            else
            (35, 120, 210)
        )

        pygame.draw.rect(
            self.screen,
            water_color,
            pygame.Rect(
                0,
                WATER_TOP,
                WIDTH,
                WATER_BOTTOM - WATER_TOP
            )
        )

        wave_color = (
            (50, 110, 170)
            if self.is_night
            else
            (100, 180, 240)
        )

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
                    wave_color,
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
                self.screen,
                self.is_night
            )

    # ========================================================
    # TASK 4 - NIGHT OVERLAY
    # ========================================================

    def draw_night_overlay(self):

        if not self.is_night:
            return

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (5, 10, 35, 75)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

    # ========================================================
    # HUD
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

        # Day/Night indicator
        if self.is_night:

            time_text = self.small_font.render(
                "NIGHT",
                True,
                (255, 245, 150)
            )

        else:

            time_text = self.small_font.render(
                "DAY",
                True,
                (255, 255, 255)
            )

        self.screen.blit(
            time_text,
            (WIDTH // 2 - 25, 12)
        )

    # ========================================================
    # HIGH SCORES
    # ========================================================

    def draw_high_scores(self):

        panel = pygame.Rect(
            145,
            100,
            350,
            390
        )

        pygame.draw.rect(
            self.screen,
            (35, 35, 35),
            panel,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            (220, 220, 220),
            panel,
            3,
            border_radius=12
        )

        title = self.font.render(
            "TOP 5 HIGH SCORES",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(WIDTH // 2, 145)
        )

        self.screen.blit(
            title,
            title_rect
        )

        if not self.high_scores:

            empty = self.small_font.render(
                "No scores yet",
                True,
                (200, 200, 200)
            )

            empty_rect = empty.get_rect(
                center=(WIDTH // 2, 220)
            )

            self.screen.blit(
                empty,
                empty_rect
            )

        else:

            for index, score in enumerate(
                self.high_scores[:5]
            ):

                text = self.font.render(
                    f"{index + 1}.    {score}",
                    True,
                    (255, 255, 255)
                )

                self.screen.blit(
                    text,
                    (210, 190 + index * 45)
                )

        restart = self.small_font.render(
            "Press R to restart",
            True,
            (200, 200, 200)
        )

        restart_rect = restart.get_rect(
            center=(WIDTH // 2, 450)
        )

        self.screen.blit(
            restart,
            restart_rect
        )

    # ========================================================
    # GAME OVER
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
            center=(WIDTH // 2, 60)
        )

        self.screen.blit(
            text,
            text_rect
        )

        self.draw_high_scores()

    # ========================================================
    # WIN
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
            center=(WIDTH // 2, 60)
        )

        self.screen.blit(
            text,
            text_rect
        )

        self.draw_high_scores()

    # ========================================================
    # DRAW EVERYTHING
    # ========================================================

    def draw(self):

        self.draw_road()

        self.draw_water()

        self.draw_logs()

        self.draw_cars()

        self.player.draw(
            self.screen
        )

        # Night overlay goes before HUD/game-over UI
        self.draw_night_overlay()

        self.draw_hud()

        if self.game_over:

            self.draw_game_over()

        elif self.won:

            self.draw_win()

        pygame.display.flip()

    # ========================================================
    # GAME LOOP
    # ========================================================

    def run(self):

        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False

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
