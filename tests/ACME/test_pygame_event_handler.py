from flexmock import flexmock

import PyGameEventHandler from cnegng.ACME

def test_pygame_event_handler():
    event_handler = PyGameEventHandler()
    flag = False
    event_handler.register_event_handler("some_event_type", lambda flag = True)
    fake_event = flexmock(type="some_event_type")
    event_handler.handle_event(fake_event)
    assert flag == True