import pygame
import pygame.locals as locals
import random

pygame.init()


class Barrier:
    def __init__(self, x: int, y: int):
        """Represents a barrier that a player can control."""

        self.speed = 3
        self.x = x
        self.y = y
        self.score = 0

        # Size in pixels
        self.height = 120
        self.width = 10

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def up(self) -> None:
        """Moves the barrier up"""

        self.y -= self.speed
        self._update_rect()

    def down(self) -> None:
        """Moves the barrier down"""

        self.y += self.speed
        self._update_rect()

    def _update_rect(self) -> None:
        """Updates the rect to be drawn on frame update."""

        if self.y < 0:
            self.y = 0

        if self.y > 380:
            self.y = 380

        # print(
        #     "Updating y pos from Barrier with id",
        #     self.id,
        #     "from y",
        #     self.rect.y,
        #     "to y",
        #     self.y,
        # )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Ball:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.speed = 1.4
        self.served = False

        # Multiplier applied on every time the ball is hitted.
        # This is done so it get's harder every time you hit the ball/
        self.hit_multiplier = 1.15

        # * 0 = Down
        # * 1 = Up
        self.directions_y = [0, 1]
        self.direction_y = random.choice(self.directions_y)

        # * 0 = Left
        # * 1 = Right

        self.directions_x = [0, 1]
        self.direction_x = random.choice(self.directions_x)

        self.height = 35
        self.width = 35

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def hit_right(self):
        """The ball was hitted from the right (p2)."""

        self.direction_x = 0
        self.direction_y = random.choice(self.directions_y)
        self.speed *= self.hit_multiplier

        self._update_rect()

    def hit_left(self):
        """The ball was hitted from the left (p1)."""

        self.direction_x = 1
        self.direction_y = random.choice(self.directions_y)

        self.speed *= self.hit_multiplier
        self._update_rect()

    def move(self):
        """Moves the ball according to the direction"""

        # Make the wall bounce of the screen

        if self.y < 0:
            self.direction_y = 0

        elif self.y > 450:
            self.direction_y = 1

        if self.served:
            # Move ball based on directions
            if self.direction_y:
                self.y -= self.speed

            else:
                self.y += self.speed

            if self.direction_x:
                self.x += self.speed

            else:
                self.x -= self.speed

        self._update_rect()

    def _update_rect(self):
        """Updates the ball rect"""

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


WIDTH = 800
HEIGHT = 500
running = True

clock = pygame.time.Clock()

# TODO: Refactor the way of storing game elements?
elements = []


def game():
    # Start a window

    #! Find a way of NOT using globals
    global running
    global elements

    pygame.display.init()
    screen = pygame.display.set_mode(size=(WIDTH, HEIGHT), flags=pygame.SCALED)

    # get the size of the window and put it in the middle

    w_width, w_height = pygame.display.get_window_size()
    print(w_width, w_height)

    ball = Ball(x=round(w_width / 2), y=round(w_height / 2))

    player_start_pos = round(w_height / 2.5)
    p1 = Barrier(x=45, y=player_start_pos)
    p2 = Barrier(x=w_width - 45, y=player_start_pos)

    elements.append(p1)
    elements.append(p2)

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key inputs

        keys = pygame.key.get_pressed()

        if ball.served:
            # Player 1 inputs
            if keys[pygame.K_w]:
                elements[0].up()

            elif keys[pygame.K_s]:
                elements[0].down()

            # Player 2 inputs

            if keys[pygame.K_UP]:
                elements[1].up()

            elif keys[pygame.K_DOWN]:
                elements[1].down()

        elif keys[pygame.K_SPACE]:
            ball.served = True

        screen.fill(
            color=pygame.Color(
                0,
                0,
                0,
            )
        )

        for element in elements:
            # draw
            pygame.draw.rect(
                surface=screen, rect=element.rect, color=pygame.Color(255, 255, 255)
            )

        # Check if ball is colliding with a barrier
        # * Functions returns the index of the rectangle the ball is colliding with
        collider = ball.rect.collidelist([p1.rect, p2.rect])

        if collider == 0:
            ball.hit_left()

        elif collider == 1:
            ball.hit_right()

        # if not ball.rect.collidelist([p1.rect]):
        #     ball.hit_left()

        # elif not ball.rect.collidelist(p2.rect):
        #     ball.hit_right()

        # Move the ball and draw it on screen
        ball.move()

        # Check if ball is out of bounds

        # Ball went pass player 1
        # print(ball.x)
        if ball.x < 0:
            p2.score += 1
            print("P2 scored!")
            print(p1.score, "-", p2.score)

            p1.y = player_start_pos
            p2.y = player_start_pos
            p1._update_rect()
            p2._update_rect()

            ball = Ball(x=round(w_width / 2), y=round(w_height / 2))

        # Ball went pass player 2
        elif ball.x > 800:
            p1.score += 1
            print("P1 scored!")
            print(p1.score, "-", p2.score)
            p1.y = player_start_pos
            p2.y = player_start_pos

            p1._update_rect()
            p2._update_rect()
            ball = Ball(x=round(w_width / 2), y=round(w_height / 2))

        pygame.draw.rect(
            surface=screen, rect=ball.rect, color=pygame.Color(255, 255, 255)
        )

        pygame.display.flip()
