from flexmock import flexmock
import pygame

from cnegng.ACME import PyGameEventHandler


class SpecificEventHandler(PyGameEventHandler):
    def __init__(self):
        self.some_flag = False
        super().__init__()
        self.register_event_handler("some_event_type", self.handle_specific_event)

    def handle_specific_event(self, event):
        self.some_flag = True

class MultiKeyEventHandler(PyGameEventHandler):
    def __init__(self):
        self.some_value = 0
        super().__init__()
        self.register_keydown_event_handler(pygame.K_UP, self.handle_specific_event)
        self.register_keydown_event_handler(pygame.K_w, self.handle_specific_event)

    def handle_specific_event(self, event):
        self.some_value = self.some_value + 1

def test_pygame_event_handler():
    event_handler = SpecificEventHandler()
    fake_event = flexmock(type="some_event_type")
    assert not event_handler.some_flag
    event_handler.handle_event(fake_event)
    assert event_handler.some_flag

def test_pygame_key_event_handler():
    event_handler = MultiKeyEventHandler()
    assert event_handler.some_value == 0
    fake_event = flexmock(type=pygame.KEYDOWN, key=pygame.K_UP)
    event_handler.handle_event(fake_event)
    assert event_handler.some_value == 1
    fake_event = flexmock(type=pygame.KEYDOWN, key=pygame.K_w)
    event_handler.handle_event(fake_event)
    assert event_handler.some_value == 2
