class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def percentage(self, base):
        total = len(self.strbases)
        if total > 0:
            numberbases = self.strbases.count(base)
            percentage = round(100.0 * numberbases/total, 1)
        else:
            percentage = 0
        return percentage