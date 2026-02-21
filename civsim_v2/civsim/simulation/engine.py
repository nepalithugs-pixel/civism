import json
import os
from .world import World

STATE_PATH = "/var/data/state.json"

class Simulation:

    def __init__(self, world):
        self.world = world

    @classmethod
    def load_or_create(cls):
        try:
            if os.path.exists(STATE_PATH):
                with open(STATE_PATH) as f:
                    data = json.load(f)
                world = World.from_dict(data)
            else:
                world = World.initial()
        except:
            world = World.initial()

        return cls(world)

    def run(self, days):
        for _ in range(days):
            self.world.step()

    def save(self):
        os.makedirs("/var/data", exist_ok=True)
        with open(STATE_PATH, "w") as f:
            json.dump(self.world.to_dict(), f)

    def metrics(self):
        return self.world.metrics()
