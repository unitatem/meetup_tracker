import json


class AttackVector:
    _FILE_PATH = "attack_vector.json"

    def __init__(self):
        with open(AttackVector._FILE_PATH) as file:
            self._attack_vector = json.load(file)

    def get_seed_url(self):
        return self._attack_vector["seed_url"]
