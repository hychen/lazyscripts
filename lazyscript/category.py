
class Category:

    def __init__(self, name):
        self.name = name
        self.items = {}

    def items(self):
        return self.items.values()

    def get(self, obj_id):
        return self.items.get(obj_id)

    def add(self, obj):
        self.items[obj.id] = obj
