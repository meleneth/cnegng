import pygame

class DuplicateHandlersError(Exception):
    pass

class PyGameEventHandler:
    """ACME module for data-driven event  handler dispatch"""
    def __init__(self):
        """
        """
        self.event_handlers = {}
    
    def handle_events(self, event_list=pygame.event):
        """Consume all pygame events and call handle_event(event) on each one

        :param event_list: target object to call get() on in a loop to handle all events
        """
        for pygame_event in event_list.get():
            self.handle_event(pygame_event)

    def handle_event(self, event):
        """Process a single event

        :param event: usually the result of pygame.event.get()
        """
        if event.type in self.event_handlers:
            self.event_handlers[event.type](event)

    def register_event_handler(self, event_type, handler_method):
        """Register a callback for when a specific event type comes in.

        :param event_type: the event type we are registering a handler for.  If one already exists, DuplicateHandlersError will be raised instead
        :param handler_method: the method to call when this event is handled.  It works well to use a method from a class that inherits from PyGameEventHandler

        """
        if event_type in self.event_handlers:
            raise DuplicateHandlersError(f"Tried to give a second handler for event_type({event_type})")
        self.event_handlers[event_type] = handler_method
