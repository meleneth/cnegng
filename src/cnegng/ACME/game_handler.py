import time
from typing import Tuple, Optional

import pygame

from cnegng.ACME.events.pygame_event_handler import PyGameEventHandler
from cnegng.ACME.events.timed_event_handler import TimedEventHandler


class GameHandler:
    """
    GameHandler is responsible for initializing the screen, handling the main game loop,
    processing events, and delegating them to a PyGameEventHandler instance.

    It also provides a simple interface for subclasses to override the update() and render()
    methods for game-specific logic.

    Attributes
    ----------
    screen_size : Tuple[int, int]
        The width and height of the game screen.
    running : bool
        Indicates whether the game is running.
    surface : pygame.Surface
        The Pygame screen surface where the game is drawn.
    event_handler : PyGameEventHandler
        Instance of a custom event handler that handles specific events.
    fps : int
        The frames per second at which the game runs.
    clock : pygame.time.Clock
        Pygame clock object to manage frame timing and delta time.
    dt : float
        Delta time (in seconds) since the last frame.
    frame_no : int
        number of frames so far
    start_time : float
        when we started tracking time
    timed_event_handler : TimedEventHandler
        This allows events to be scheduled to run at some future time
    """

    def __init__(
        self,
        screen_size: Tuple[int, int],
        event_handler: Optional[PyGameEventHandler] = None,
        fps: int = 60,
    ) -> None:
        """
        Initializes the GameHandler with a screen of the specified size and an event handler.

        Parameters
        ----------
        screen_size : Tuple[int, int]
            The width and height of the game screen.
        event_handler : PyGameEventHandler
            The instance of the event handler for processing events.
        fps : int, optional
            The frames per second to run the game (default is 60).
        """
        if event_handler is None:
            event_handler = PyGameEventHandler()
        pygame.init()
        self.screen_size: Tuple[int, int] = screen_size
        self.running: bool = True
        self.surface: pygame.Surface = pygame.display.set_mode(self.screen_size)
        self.event_handler = event_handler
        self.fps: int = fps
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.dt: float = 0.0  # Delta time
        self.frame_no: int = 0
        self.start_time: float = time.time()
        self.timed_event_handler = TimedEventHandler()
        self.fill_color = (30, 30, 30)

    def run(self) -> None:
        """
        The main game loop that processes events and delegates them to the event handler.
        it calls timed_event_handler.apply(dt)
        and will call self.update(dt)
        and self.render()

        It will exit when the QUIT event is detected.
        """
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.event_handler.handle_event(event)

            self.timed_event_handler.apply(self.dt)
            self._update(self.dt)
            self.surface.fill(self.fill_color)
            self.render()

            pygame.display.flip()
        print(f"Actual FPS: {self.actual_fps()}")

    def actual_fps(self) -> float:
        """Calculate and return the actual frames per second (FPS)."""
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            return self.frame_no / elapsed_time
        return 0.0

    def _update(self, dt: float) -> None:
        self.frame_no += 1
        self.update(dt)

    def update(self, dt: float) -> None:
        """
        Updates the game state. This should be overridden by subclasses.

        Parameters
        ----------
        dt : float
            Delta time (in seconds) since the last frame.
        """
        pass

    def render(self) -> None:
        """
        Renders the game. This should be overridden by subclasses.
        """
        pass

    def stop(self) -> None:
        """
        Stops the game loop by setting the running flag to False.
        """
        self.running = False

    def close(self) -> None:
        """
        Closes the Pygame window and quits Pygame.
        """
        pygame.quit()
