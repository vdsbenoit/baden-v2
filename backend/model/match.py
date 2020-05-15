class Match:
    def __init__(self, id: str, game_id: str, time):
        self.id = id
        self.game_id = game_id
        self.time = time
        self.game_name = ""
        self.start_time = ""
        self.stop_time = ""
        self.player_ids = list()
        self.player_numbers = list()
        self.winner = ""
        self.loser = ""
        self.even = False
        self.reporter = ""

    def to_dict(self):
        return self.__dict__
