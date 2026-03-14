class EmotionHistory:

    def __init__(self):

        self.timeline = []

    def add(self, emotion):

        self.timeline.append(emotion)

        if len(self.timeline) > 50:
            self.timeline.pop(0)