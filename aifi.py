class MovingAverage:

    def __init__(self,window):
        self.window = window
        self.message_bundle = []

    def step(self, message):

        # if message source not already in message_bundle, append it
        self.message_bundle.append(message)
        if len(self.message_bundle) > self.window:
            self.message_bundle.pop()

    def current_state(self):
        return self.message_bundle