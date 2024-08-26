from flexmock import flexmock

from cnegng.ACME import PyGameEventHandler

class SpecificEventHandler(PyGameEventHandler):
    def __init__(self):
        self.some_flag = False
        super().__init__()
        self.register_event_handler("some_event_type", self.handle_specific_event)

    def handle_specific_event(self, event):
        self.some_flag = True

def test_pygame_event_handler():
    event_handler = SpecificEventHandler()
    flag = False
    fake_event = flexmock(type="some_event_type")
    event_handler.handle_event(fake_event)
    assert event_handler.some_flag
