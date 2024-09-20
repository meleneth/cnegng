import pytest
from typing import List
from cnegng.ACME import TimedEventHandler


@pytest.fixture
def timed_event_handler() -> TimedEventHandler:
    """
    Fixture to create a fresh instance of TimedEventHandler for each test.
    """
    return TimedEventHandler()


def test_single_event(timed_event_handler: TimedEventHandler) -> None:
    """
    Test a single event is triggered correctly after the correct time has passed.
    """
    triggered: List[bool] = [False]

    def callback() -> None:
        triggered[0] = True

    timed_event_handler.add_event(5.0, callback)
    timed_event_handler.apply(2.0)
    assert not triggered[0]  # Event should not trigger yet

    timed_event_handler.apply(3.0)
    assert triggered[0]  # Event should now trigger


def test_multiple_events_order(timed_event_handler: TimedEventHandler) -> None:
    """
    Test that multiple events are triggered in the correct order based on time.
    """
    results: List[str] = []

    def event1() -> None:
        results.append("event1")

    def event2() -> None:
        results.append("event2")

    timed_event_handler.add_event(5.0, event1)
    timed_event_handler.add_event(3.0, event2)

    timed_event_handler.apply(3.0)
    assert results == ["event2"]  # Event 2 should trigger first

    timed_event_handler.apply(2.0)
    assert results == ["event2", "event1"]  # Then event 1


def test_no_event_trigger(timed_event_handler: TimedEventHandler) -> None:
    """
    Test that no events are triggered if not enough time has passed.
    """
    results: List[str] = []

    def event1() -> None:
        results.append("event1")

    def event2() -> None:
        results.append("event2")

    timed_event_handler.add_event(5.0, event1)
    timed_event_handler.add_event(10.0, event2)

    timed_event_handler.apply(4.0)
    assert results == []  # No events should trigger


def test_has_pending_events(timed_event_handler: TimedEventHandler) -> None:
    """
    Test the has_pending_events method to ensure it accurately reflects whether
    there are pending events.
    """

    def dummy_callback() -> None:
        pass

    assert not timed_event_handler.has_pending_events()

    timed_event_handler.add_event(5.0, dummy_callback)
    assert timed_event_handler.has_pending_events()

    timed_event_handler.apply(5.0)
    assert not timed_event_handler.has_pending_events()  # Event should be triggered


def test_all_events_trigger(timed_event_handler: TimedEventHandler) -> None:
    """
    Test that all events trigger correctly even with multiple apply calls.
    """
    triggered: List[bool] = [False, False]

    def event1() -> None:
        triggered[0] = True

    def event2() -> None:
        triggered[1] = True

    timed_event_handler.add_event(3.0, event1)
    timed_event_handler.add_event(6.0, event2)

    timed_event_handler.apply(4.0)
    assert triggered[0]  # First event triggered
    assert not triggered[1]  # Second event not triggered yet

    timed_event_handler.apply(2.0)
    assert triggered[1]  # Now second event should trigger
