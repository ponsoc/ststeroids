class Route:
    def __init__(self, name: str, target: callable, condition: callable = None):
        self.name = name
        self.target = target
        self.condition = condition