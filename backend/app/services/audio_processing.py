from allosaurus.app import read_recognizer

# model = read_recognizer()

class AudioPart:
    def __init__(self, start: float, end: float, text: str):
        self.start = start
        self.end = end
        self.text = text

    def __repr__(self):
        return f"AudioPart(start={self.start}, end={self.end}, text='{self.text}')"