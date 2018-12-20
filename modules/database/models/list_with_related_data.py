import json

class ListWihtRelatedData:

    id = None
    name = None
    cards = None

    def __init__(self, id, name, cards):
        self.id = id
        self.name = name
        self.cards = cards

    def to_json(self):
        self.cards['cards'] = self.cards
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
