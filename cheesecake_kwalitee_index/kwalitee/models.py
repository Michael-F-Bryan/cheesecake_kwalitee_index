"""
All the data structures that are needed when generating a "kwalitee" score.
"""

class Score:
    """
    A generic score.
    """
    def __init__(self, value, total):
        self.value = value
        self.total = total

    def as_float(self):
        return self.value/self.total

    def __repr__(self):
        return '<{}: {}/{}>'.format(
            self.__class__.__name__,
            self.value,
            self.total)

    def __eq__(self, other):
        return self.value == other.value and self.total == other.total
