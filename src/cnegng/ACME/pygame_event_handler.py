import pygame


class DuplicateHandlersError(Exception):
    """Raised when a handler already exists for a given event_type"""
    pass


class KeyEventHandler:
    """Handler to handle matching the .key attribute on PyGame generated events"""
    def __init__(self):
        self.key_event_handlers = {}

    def register_key_event(self, key, handler_method):
        """
        Registers a handler method for the specified key.

        :param key: The key constant from pygame (e.g., ``pygame.K_RETURN``).
        :type key: int
        :param handler_method: The method to call when the key is pressed.
        :type handler_method: function

        :Example:

        .. code-block:: python

            class SomeClass:
                def handle_up_arrow(self):
                    print("Up arrow pressed!")

            key_handler = KeyEventHandler()
            some_instance = SomeClass()
            key_handler.register_key_event(pygame.K_UP, some_instance.handle_up_arrow)
            # Now, whenever pygame.K_UP is pressed, handle_up_arrow will be invoked.

        """
        if key in self.key_event_handlers:
            raise DuplicateHandlersError(
                f'Duplicate key handler configured for key "{key}"'
            )
        self.key_event_handlers[key] = handler_method

    def __call__(self, event):
        if (key_event := self.key_event_handlers.get(event.key)) is not None:
            key_event(event)


class PyGameEventHandler:
    """ACME module for data-driven event  handler dispatch"""

    def __init__(self):
        """ """
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
        if (event_handler := self.event_handlers.get(event.type)) is not None:
            event_handler(event)

    def register_event_handler(self, event_type, handler_method):
        """Register a callback for when a specific event type comes in.

        :param event_type: the event type we are registering a handler for.  If one already exists, DuplicateHandlersError will be raised instead
        :param handler_method: the method to call when this event is handled.  It works well to use a method from a class that inherits from PyGameEventHandler

        """
        if event_type in self.event_handlers:
            raise DuplicateHandlersError(
                f"Tried to give a second handler for event_type({event_type})"
            )
        self.event_handlers[event_type] = handler_method

    def register_keydown_event_handler(self, key, handler_method):
        """Register a callback for a specific key down event handler is called

        :param key: the key to react to
        :param handler_method: the method to call when this event is handled.  It works well to use a method from a class that inherits from PyGameEventHandler

        """
        self.register_key_event_handler(pygame.KEYDOWN, key, handler_method)

    def register_keyup_event_handler(self, key, handler_method):
        """Register a callback for a specific key up event handler is called

        :param key: the key to react to
        :param handler_method: the method to call when this event is handled.  It works well to use a method from a class that inherits from PyGameEventHandler

        """
        self.register_key_event_handler(pygame.KEYUP, key, handler_method)

    def register_key_event_handler(self, event_type, key, handler_method):
        """Register a callback for a specific key event handler is called

        :param event_type: the event type we are registering a handler for.
        :param key: the key to react to.  If it already exists, DuplicateHandlersError will be raised instead
        :param handler_method: the method to call when this event is handled.  It works well to use a method from a class that inherits from PyGameEventHandler

        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = KeyEventHandler()
        # if it blows up here because NoMethodError for register_key_event, it means something is already configured to listen to this event_type that isn't using a KeyEventHandler
        self.event_handlers[event_type].register_key_event(key, handler_method)
