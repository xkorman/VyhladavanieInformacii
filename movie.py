class Movie:

    rank = 0

    def __init__(self, name):
        self.reviews = []
        self.name = name
        self.hash = hash(name)

    def rank_it(self, rank):
        if rank == None:
            rank = self.rank
        length = len(self.reviews)
        self.rank = (self.rank * length + int(rank)) / (length + 1)

    def __str__(self):
        return '%s - [%s]' % (self.name, self.reviews)

    def __repr__(self):
        return '%s | HASH=%s' % (self.name, self.hash)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name