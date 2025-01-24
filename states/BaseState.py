class BaseState():
    def enter(self):
        """Initialize the state."""
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass

    def exit(self):
        pass
