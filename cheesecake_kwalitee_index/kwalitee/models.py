class Score:
    def __init__(self, value, total):
        self.value = value
        self.total = total

    def __repr__(self):
        return '<{}: {}/{}>'.format(
                self.__class__.__name__,
                self.value,
                self.total)
