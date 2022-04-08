class Section:
    def __init__(self, id, name, city, unit, category, nb_teams):
        self.id = id
        self.name = name
        self.city = city
        self.unit = unit
        self.category = category
        self.nbTeams = nb_teams
        self.teams = list()
        self.scores = list()

    def to_dict(self):
        return self.__dict__