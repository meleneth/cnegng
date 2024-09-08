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
