class Section:
    def __init__(self, id, name, city, unit, category, nb_teams, nb_players):
        self.id = id
        self.name = name
        self.city = city
        self.unit = unit
        self.category = category
        self.nbTeams = nb_teams
        self.nbPlayers = nb_players
        self.teams = list()
        self.score = 0

    def to_dict(self):
        return self.__dict__
