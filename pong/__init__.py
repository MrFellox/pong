import pygame
import pygame.locals as locals

pygame.init()


class Barrier:
    def __init__(self, x: int, y: int, surface: pygame.Surface):
        """Represents a barrier that a player can control."""

        self.speed = 3
        self.x = x
        self.y = y
        self.surface = surface

        # Size in pixels
        self.height = 120
        self.width = 10

        # self.rect = pygame.Rect(
        #     height=self.height, width=self.width, left=self.x, top=self.y
        # )

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(
        #     surface=self.surface, color=pygame.Color(1, 1, 1), rect=self.rect
        # )

    def up(self) -> None:
        """Moves the barrier up"""

        print("up")
        self.y -= self.speed
        self._update_rect()

    def down(self) -> None:
        """Moves the barrier down"""

        print("down")
        self.y += self.speed
        self._update_rect()

    def _update_rect(self) -> None:
        """Updates the rect to be drawn on frame update."""

        if self.y < 0:
            self.y = 0

        if self.y > 380:
            self.y = 380

        print("Updating y pos from", self.rect.y, "to", self.y)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


WIDTH = 800
HEIGHT = 500
running = True

clock = pygame.time.Clock()

elements = []


def game():
    # Start a window
    global running
    global elements

    pygame.display.init()
    screen = pygame.display.set_mode(size=(WIDTH, HEIGHT), flags=pygame.SCALED)

    # get the size of the window and put it in the middle

    w_width, w_height = pygame.display.get_window_size()
    print(w_width, w_height)
    # p1 = Barrier(x=round(w_width / 2), y=round(w_height / 2), surface=screen)
    p1 = Barrier(x=45, y=round(w_height / 2.5), surface=screen)
    p2 = Barrier(x=w_width - 45, y=round(w_height / 2.5), surface=screen)

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

        pygame.display.flip()
