class PyGameEventHandler:
    def __init__(self):
        """
        """
        self.event_handlers = {}
    
    def handle_events(self):
        """
        """
        pass

    def handle_event(self, event):
        """
        """
        if event.type in self.event_handlers:
            self.event_handlers[event.type](event)

