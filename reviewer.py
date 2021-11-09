class Reviewer:

    def __init__(self, name):
        self.name = name
        self.movies = []
        self.reviews = []
        self.id = None
        self.trust = 0 

    def __str__(self):
        return '%s / %s' % (self.id, self.name)

    def __repr__(self):
        return '#%s %s' % (self.id, self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def add_to_list(self, movie, review_id):
        self.movies.append(hash(movie))
        self.reviews.append(review_id)
