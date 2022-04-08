import hashlib


class Team:
    def __init__(self, id, section, category):
        self.id = id
        self.number = -1
        self.section = section
        self.category = category
        self.hash = hashlib.sha1(f"Baden {id} Battle".encode()).hexdigest()
        self.matches = list()
        self.ignoreScore = False
        self.scores = list()

    def to_dict(self):
        return self.__dict__
