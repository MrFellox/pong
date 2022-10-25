import pygame
import pygame.locals as locals
import random

pygame.init()


class Barrier:
    def __init__(self, x: int, y: int, id: int):
        """Represents a barrier that a player can control."""

        self.speed = 3
        self.x = x
        self.y = y
        self.id = id

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
        self.serve()

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

    def serve(self):
        """Move the ball to start the match"""
        pass

    def move(self):
        """Moves the ball according to the direction"""

        # Make the wall bounce of the screen

        if self.y < 0:
            self.direction_y = 0

        elif self.y > 450:
            self.direction_y = 1

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

        print(self.speed)
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

    p1 = Barrier(x=45, y=round(w_height / 2.5), id=1)
    p2 = Barrier(x=w_width - 45, y=round(w_height / 2.5), id=2)

    elements.append(p1)
    elements.append(p2)

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key inputs

        keys = pygame.key.get_pressed()

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

        pygame.draw.rect(
            surface=screen, rect=ball.rect, color=pygame.Color(255, 255, 255)
        )

        pygame.display.flip()
