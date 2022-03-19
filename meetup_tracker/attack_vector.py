import json


class AttackVector:
    _FILE_PATH = "attack_vector.json"

    def __init__(self):
        with open(AttackVector._FILE_PATH, "r") as file:
            self._attack_vector = json.load(file)

    def get_login(self):
        return self._attack_vector["meetup"]["login"]

    def get_password(self):
        return self._attack_vector["meetup"]["password"]

    def get_seed_url(self):
        return self._attack_vector["target"]["seed_url"]

    def get_name(self):
        return self._attack_vector["target"]["name"]

