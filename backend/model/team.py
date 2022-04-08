import hashlib

from model.section import Section


class Team:
    def __init__(self, team_id, section: Section):
        self.id = team_id
        self.number = -1
        self.sectionId = section.id
        self.sectionName = section.name
        self.city = section.city
        self.category = section.category
        self.hash = hashlib.sha1(f"Baden {id} Battle".encode()).hexdigest()
        self.matches = list()
        self.ignoreScore = False
        self.scores = list()

    def to_dict(self):
        return self.__dict__
