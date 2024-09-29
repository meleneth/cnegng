from typing import Callable, Dict, List


class EventBus:
    """
    A simple event bus system to handle publishing and subscribing to events.

    Events are broadcast to all listeners who have subscribed to a particular event type.

    Example usage:
        >>> bus = EventBus()
        >>> def on_level_up(player):
        ...     print(f"{player.name} leveled up to {player.level}")
        >>> bus.subscribe('LEVEL_UP', on_level_up)
        >>> bus.publish('LEVEL_UP', player_instance)
    """

    def __init__(self):
        """Initialize the EventBus with no subscribers."""
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, listener: Callable):
        """
        Subscribe a listener function to a specific event type.

        :param event_type: The event type to listen for (e.g., 'LEVEL_UP').
        :param listener: The function to call when the event is triggered.
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(listener)

    def publish(self, event_type: str, *args, **kwargs):
        """
        Publish an event to all listeners subscribed to the given event type.

        :param event_type: The event type to trigger (e.g., 'LEVEL_UP').
        :param args: Positional arguments passed to the listener functions.
        :param kwargs: Keyword arguments passed to the listener functions.
        """
        for listener in self._subscribers.get(event_type, []):
            listener(*args, **kwargs)
