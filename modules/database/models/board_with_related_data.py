import json

class BoardWithRelatedData:

    id = None
    name = None
    bg_color = None
    lists = None

    def __init__(self, id, name, bg_color, lists):
        self.id = id
        self.name = name
        self.bg_color = bg_color
        self.lists = lists

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
