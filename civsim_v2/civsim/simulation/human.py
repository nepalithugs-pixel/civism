import random
import uuid

BELIEF_SYSTEMS = [
    "animism", "polytheism", "monotheism", "atheism", "shamanism",
    "ancestor_worship", "nature_worship", "sun_worship", "agnosticism", "mysticism"
]

IDEOLOGIES = [
    "tribalism", "collectivism", "individualism", "egalitarianism", "hierarchy",
    "expansionism", "isolationism", "pacifism", "militarism", "meritocracy"
]

ARCHETYPES = [
    "philosopher", "warrior", "farmer", "merchant", "healer",
    "priest", "artist", "explorer", "leader", "outcast"
]

THOUGHT_EVENTS = [
    ("A strange dream left visions of celestial beings.", {"spirituality": 0.15, "health": 0.02}),
    ("Watching stars move in patterns sparked cosmic wonder.", {"technical": 0.1, "spirituality": 0.05}),
    ("A plague survivor preached divine protection.", {"spirituality": 0.2, "social": 0.05}),
    ("A charismatic elder united the tribe under shared myths.", {"social": 0.15, "political": 0.1}),
    ("Trade with strangers brought new ideas and distrust.", {"economic": 0.1, "cultural": 0.08}),
    ("Discovery of fire mastery elevated social status.", {"technical": 0.12, "survival": 0.1}),
    ("A long famine made people question divine favor.", {"spirituality": -0.1, "survival": 0.15}),
    ("A beautiful cave painting moved hearts toward art.", {"cultural": 0.15, "social": 0.05}),
    ("Victory in battle reinforced belief in warrior gods.", {"spirituality": 0.1, "political": 0.1}),
    ("An eclipse caused mass spiritual awakening.", {"spirituality": 0.25, "technical": -0.05}),
    ("A child prodigy invented a new tool.", {"technical": 0.2, "economic": 0.05}),
    ("Stolen knowledge from a rival clan sparked revolution.", {"technical": 0.15, "political": -0.05}),
    ("Rumors of paradise beyond the horizon drove exploration.", {"survival": 0.05, "cultural": 0.1}),
    ("A philosopher questioned the nature of suffering.", {"cultural": 0.1, "spirituality": 0.05}),
    ("A prophet claimed to speak for the divine.", {"spirituality": 0.3, "political": 0.15}),
    ("Betrayal by an ally fractured political unity.", {"political": -0.15, "social": -0.1}),
    ("Shared grief over the dead forged deep bonds.", {"social": 0.2, "cultural": 0.1}),
    ("An outsider brought healing herbs and strange gods.", {"health": 0.05, "cultural": 0.12}),
    ("Prosperity led to excess and moral questioning.", {"cultural": 0.08, "spirituality": 0.05}),
    ("Drought forced migration and new tribal alliances.", {"survival": 0.15, "political": 0.1}),
    ("A meteor fall was taken as a divine omen.", {"spirituality": 0.2, "technical": 0.05}),
    ("Music was discovered as a form of collective worship.", {"cultural": 0.2, "social": 0.1}),
    ("Writing was invented to record sacred laws.", {"technical": 0.15, "political": 0.1}),
    ("A sacred mountain became a pilgrimage site.", {"spirituality": 0.15, "social": 0.08}),
    ("A great leader's death caused a crisis of succession.", {"political": 0.2, "social": -0.1}),
]


def rand_drive():
    keys = ["technical", "social", "economic", "political", "cultural", "survival", "spirituality"]
    vals = [random.random() for _ in keys]
    s = sum(vals)
    return {k: v/s for k, v in zip(keys, vals)}


class Human:

    def __init__(self, age_days=0, parent_belief=None, parent_ideology=None):
        self.id = str(uuid.uuid4())[:8]
        self.age_days = age_days
        self.alive = True
        self.name = self._gen_name()

        self.health = random.uniform(0.75, 1.0)
        self.wealth = random.uniform(0.2, 1.0)
        self.happiness = random.uniform(0.4, 0.9)

        self.lifespan = random.randint(40 * 365, 80 * 365)

        self.drives = rand_drive()
        self.archetype = random.choice(ARCHETYPES)

        if parent_belief and random.random() < 0.75:
            self.belief = parent_belief
        else:
            self.belief = random.choice(BELIEF_SYSTEMS)

        if parent_ideology and random.random() < 0.65:
            self.ideology = parent_ideology
        else:
            self.ideology = random.choice(IDEOLOGIES)

        self.conviction = random.uniform(0.3, 1.0)
        self.influence = random.uniform(0.1, 0.8)
        self.thoughts = []

    def _gen_name(self):
        syllables = ["Ka", "Ra", "Nu", "Ma", "Li", "Te", "An", "Ku", "Shi", "Ba",
                     "Da", "Ro", "Gi", "Ve", "Mo", "Zo", "Ae", "Ui", "Bra", "Kha",
                     "Sor", "Ven", "Thal", "Myr", "Ori", "Zel", "Phar", "Wyn"]
        return random.choice(syllables) + random.choice(syllables).lower()

    def age_one_day(self):
        self.age_days += 1
        age_ratio = self.age_days / self.lifespan

        self.health -= 0.00003 * age_ratio

        if self.archetype == "healer":
            self.health += 0.000005
        elif self.archetype == "warrior":
            self.health -= 0.000002

        if random.random() < max(0, age_ratio - 0.80) * 0.5:
            self.alive = False

        if self.health <= 0:
            self.alive = False

        self.happiness += (0.6 - self.happiness) * 0.001

    def apply_thought(self, thought_event):
        text, effects = thought_event
        self.thoughts.append(text)
        if len(self.thoughts) > 5:
            self.thoughts = self.thoughts[-5:]

        for drive, delta in effects.items():
            if drive == "health":
                self.health = min(1.0, self.health + delta * self.conviction)
            elif drive in self.drives:
                self.drives[drive] = max(0.01, min(1.0, self.drives[drive] + delta * self.conviction))

        self.happiness = min(1.0, self.happiness + 0.05)

    def can_reproduce(self):
        age_years = self.age_days / 365
        return 16 <= age_years <= 45 and self.health > 0.4

    def spread_belief(self, other):
        if self.influence * self.conviction > random.random():
            if random.random() < 0.3:
                other.belief = self.belief
                other.conviction = min(1.0, other.conviction + 0.05)
            if random.random() < 0.2:
                other.ideology = self.ideology

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        h = cls.__new__(cls)
        h.__dict__.update(data)
        return h
