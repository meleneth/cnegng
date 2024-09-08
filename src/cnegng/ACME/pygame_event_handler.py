import pygame


class DuplicateHandlersError(Exception):
    """Raised when a handler already exists for a given event_type"""
    pass


class KeyEventHandler:
    """
    A class to register and handle key events.

    This class allows registering key events with specific handler methods,
    which will be called when the corresponding key is pressed.

    Methods
    -------
    register_key_event(key, handler_method)
        Registers a handler method to be invoked when the specified key is pressed.
    handle_event(event)
        Checks if the event matches a registered key and invokes the handler method.
    """

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
                def __init__():
                    register_key_event(pygame.K_UP, self.handle_up_arrow)
                def handle_up_arrow(self):
                    print("Up arrow pressed!")
            # TODO cleanup example
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
    """
    A class to register and handle pygame events.

    a pygame event will have a .type attribute that is the event type.  This is what we check on the events that are passed in, as we look for handlers.

    Methods
    -------
    register_event_handler(self, event_type, handler_method)
        Registers a handler method to be invoked when the specified event is passed to handle_event(event).
    handle_event(event)
        Checks if the event matches a registered event and invokes the handler method.
    handle_events(self, event_list=pygame.event)
        pumps the pygame event queue, consuming all events and passing them one at a time to handle_event().
    register_keydown_event_handler(self, key, handler_method)
        convenience method for setting up keydown events to a specific key.
    register_keyup_event_handler(self, key, handler_method)
        convenience method for setting up keyup events to a specific key.
    register_key_event_handler(self, event_type, key, handler_method)
        sets up a KeyEventHandler for the given event_type, then uses it to register a handler for the given key.

    :Example:

    .. code-block:: python

        class SomeClass:
            def __init__():
                register_keydown_event_handler(pygame.K_UP, self.handle_up_arrow)
            def handle_up_arrow(self):
                print("Up arrow pressed!")

        some_instance = SomeClass()
        while(True):
            some_instance.handle_events()
        # Now, whenever pygame.K_UP is pressed, handle_up_arrow will be invoked.
    """

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
        """Process a single event.  Usually called by handle_events()

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
