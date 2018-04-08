from collections import Counter

class Freq(Counter):

    def __init__(self, items):
        length = len(items)
        counts = Counter(items)
        for item, count in counts.items():
            frequency = float(count) / length
            self.__setitem__(item, frequency)
