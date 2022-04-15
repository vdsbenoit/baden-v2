import hashlib


class Game:
    def __init__(self, game_id: int, circuit: str, name: str):
        self.id = game_id
        self.hash = hashlib.sha1(f"Baden {game_id} Battle".encode()).hexdigest()
        self.circuit = circuit
        self.name = name
        self.morningLeaders = list()
        self.afternoonLeaders = list()
        self.matches = list()
        self.weight = 1

    def to_dict(self):
        return self.__dict__


def set_name(db, id, name):
    batch = db.batch()

    game_ref = db.collection("games").document(id)
    batch.update(game_ref, {
        "name": name
    })

    docs = db.collection("matches").where("game_id", "==", id).stream()
    for doc in docs:
        batch.update(doc.reference, {
            "game_name": name
        })

    batch.commit()
    print(f"New name defined for game {id} : {name}")
