import heapq
from typing import Callable, List, Tuple


class TimedEventHandler:
    """
    Manages a collection of timed events. Events are scheduled to occur at a
    specific time in the future and are stored in sorted order for efficient
    processing.

    Attributes
    ----------
    _events : List[Tuple[float, Callable[[], None]]]
        A heap storing events with their absolute expiration time and associated callbacks.
    _current_time : float
        Internal clock to manage virtual time.
    """

    def __init__(self) -> None:
        """
        Initializes the TimedEventHandler with an empty event list and sets the
        internal clock to 0.
        """
        self._events: List[Tuple[float, Callable[[], None]]] = []
        self._current_time: float = 0.0  # Internal clock to manage virtual time

    def add_event(
        self, time_until_trigger: float, callback: Callable[[], None]
    ) -> None:
        """
        Adds a timed event that will trigger after `time_until_trigger` seconds.

        Parameters
        ----------
        time_until_trigger : float
            Time in seconds after which the event will be triggered.
        callback : Callable[[], None]
            A callable that will be invoked when the event is triggered.
        """
        expiration_time = self._current_time + time_until_trigger
        heapq.heappush(self._events, (expiration_time, callback))

    def apply(self, dt: float) -> None:
        """
        Advances the internal clock by `dt` seconds and processes any events
        that have expired.

        Parameters
        ----------
        dt : float
            Time delta (in seconds) to advance the internal clock.
        """
        self._current_time += dt

        # Process events that have expired
        while self._events and self._events[0][0] <= self._current_time:
            expiration_time, callback = heapq.heappop(self._events)
            if expiration_time <= self._current_time:
                # Trigger the event
                callback()

    def has_pending_events(self) -> bool:
        """
        Returns whether there are any pending events.

        Returns
        -------
        bool
            True if there are pending events, False otherwise.
        """
        return len(self._events) > 0
