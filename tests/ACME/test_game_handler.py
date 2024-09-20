import pytest
from flexmock import flexmock
from cnegng.ACME import PyGameEventHandler
from cnegng.ACME import GameHandler
import pygame


@pytest.fixture
def game_handler():
    """
    Fixture to create a GameHandler instance with a mock event handler.
    """
    event_handler = flexmock(PyGameEventHandler)  # Mock event handler using flexmock
    return GameHandler((800, 600), event_handler, fps=60)


def test_game_initialization(game_handler):
    """
    Test if the game handler initializes with the correct screen size and FPS.
    """
    assert game_handler.screen_size == (800, 600)
    assert game_handler.fps == 60


def dont_test_event_handling(game_handler):
    """
    Test if the event handler's handle_event method is called for non-QUIT events.
    """
    flexmock(pygame.event).should_receive("get").and_return(
        [flexmock(type=pygame.KEYDOWN)]
    )

    game_handler.event_handler.should_receive("handle_event").once().with_args(
        flexmock(type=pygame.KEYDOWN)
    )

    game_handler.run()


def test_quit_event(game_handler):
    """
    Test if the game stops running when the QUIT event is received.
    """
    flexmock(pygame.event).should_receive("get").and_return(
        [flexmock(type=pygame.QUIT)]
    )

    game_handler.run()

    assert not game_handler.running


def dont_test_update_render_call(game_handler):
    """
    Test if the update() and render() methods are called during the game loop.
    """
    game_handler = flexmock(game_handler)
    game_handler.should_receive("update").once().with_args(game_handler.dt)
    game_handler.should_receive("render").once()

    flexmock(pygame.event).should_receive("get").and_return(
        [flexmock(type=pygame.KEYDOWN)]
    )
    flexmock(pygame.display).should_receive("flip").once()

    game_handler.run()


def test_stop_game(game_handler):
    """
    Test if the game loop can be stopped manually by calling the stop() method.
    """
    game_handler.stop()
    assert not game_handler.running
