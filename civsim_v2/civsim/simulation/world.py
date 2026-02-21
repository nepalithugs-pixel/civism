import random
from collections import Counter
from .human import Human, THOUGHT_EVENTS, BELIEF_SYSTEMS, IDEOLOGIES

MAX_POPULATION = 5000

class World:

    def __init__(self):
        self.day = 0
        self.era = "Stone Age"
        self.tech_score = 0.0
        self.population = [Human(age_days=random.randint(18*365, 35*365)) for _ in range(20)]
        self.history = []
        self.events_log = []
        self.belief_wars = 0
        self.innovations = []

    @classmethod
    def initial(cls):
        return cls()

    def _determine_era(self):
        t = self.tech_score
        if t < 5:      return "Stone Age"
        elif t < 15:   return "Bronze Age"
        elif t < 30:   return "Iron Age"
        elif t < 60:   return "Classical Age"
        elif t < 100:  return "Medieval Age"
        elif t < 150:  return "Renaissance"
        elif t < 200:  return "Industrial Age"
        else:          return "Information Age"

    def step(self):
        self.day += 1
        alive = [h for h in self.population if h.alive]
        births = []
        event_texts = []

        # Age everyone
        for h in alive:
            h.age_one_day()

        alive = [h for h in alive if h.alive]

        # --- Thought injection ---
        # Each day a random % of population may receive a thought
        thought_chance = 0.002 + (0.001 * self.tech_score / 50)
        for h in alive:
            if random.random() < thought_chance:
                event = random.choice(THOUGHT_EVENTS)
                h.apply_thought(event)

        # --- Belief spreading ---
        if len(alive) > 1:
            influencers = [h for h in alive if h.influence > 0.5 and h.archetype in ("priest","leader","philosopher")]
            for inf in influencers:
                targets = random.sample(alive, min(5, len(alive)))
                for t in targets:
                    if t is not inf:
                        inf.spread_belief(t)

        # --- Reproduction ---
        repro = [h for h in alive if h.can_reproduce()]
        random.shuffle(repro)
        pop_cap_factor = max(0.1, 1.0 - len(alive) / MAX_POPULATION)
        for i in range(0, len(repro)-1, 2):
            birth_rate = 0.008 * pop_cap_factor
            if alive[i].ideology == "collectivism":
                birth_rate *= 1.2
            if random.random() < birth_rate:
                pb = repro[i].belief
                pi = repro[i].ideology
                child_age = random.randint(0, 5 * 365)
                births.append(Human(age_days=child_age, parent_belief=pb, parent_ideology=pi))

        # --- Economy ---
        avg_tech = sum(h.drives["technical"] for h in alive) / max(1, len(alive))
        for h in alive:
            productivity = h.drives["economic"] * h.health * (1 + avg_tech * 0.5)
            h.wealth += productivity * 0.002
            h.wealth -= 0.0008
            if h.wealth < 0:
                h.health -= 0.002
            h.wealth = max(0, h.wealth)

        # --- Tech accumulation ---
        tech_gain = sum(h.drives["technical"] for h in alive if h.archetype in ("philosopher","explorer")) * 0.0001
        self.tech_score += tech_gain
        self.era = self._determine_era()

        # --- Random events ---
        if random.random() < 0.0003:
            severity = random.uniform(0.05, 0.25)
            for h in alive:
                if random.random() < 0.15:
                    h.health -= severity
            event_texts.append(f"Plague swept the land (severity {severity:.2f})")

        if random.random() < 0.00005:
            for h in alive:
                h.health -= random.uniform(0.05, 0.2)
            event_texts.append("A great disaster struck the civilization")

        if random.random() < 0.0002 and len(alive) > 10:
            # Belief war
            beliefs = [h.belief for h in alive]
            belief_counts = Counter(beliefs)
            if len(belief_counts) > 1:
                top_beliefs = belief_counts.most_common(2)
                faction_a = [h for h in alive if h.belief == top_beliefs[0][0]]
                faction_b = [h for h in alive if h.belief == top_beliefs[1][0]]
                casualties = random.randint(1, max(1, min(len(faction_a), len(faction_b)) // 3))
                for h in random.sample(faction_a + faction_b, casualties):
                    h.health -= random.uniform(0.3, 0.8)
                self.belief_wars += 1
                event_texts.append(f"Belief conflict between {top_beliefs[0][0]} and {top_beliefs[1][0]}: {casualties} casualties")

        if random.random() < 0.00005:
            # Innovation
            innovation_types = ["wheel", "writing", "agriculture", "metallurgy", "medicine",
                                "mathematics", "architecture", "navigation", "trade routes", "philosophy"]
            avail = [i for i in innovation_types if i not in self.innovations]
            if avail:
                inn = random.choice(avail)
                self.innovations.append(inn)
                self.tech_score += 5
                for h in alive:
                    h.drives["technical"] = min(1.0, h.drives["technical"] + 0.01)
                event_texts.append(f"Innovation discovered: {inn}!")

        # Collective spiritual awakening
        if random.random() < 0.00005:
            for h in alive:
                h.drives["spirituality"] = min(1.0, h.drives.get("spirituality", 0.1) + 0.1)
                h.happiness = min(1.0, h.happiness + 0.1)
            event_texts.append("A great spiritual awakening swept the civilization")

        self.population = [h for h in alive if h.alive] + births
        if event_texts:
            self.events_log.append({"day": self.day, "events": event_texts})
            if len(self.events_log) > 100:
                self.events_log = self.events_log[-100:]

        self.record_metrics()

    def record_metrics(self):
        pop = self.population
        n = len(pop)
        if n == 0:
            return

        beliefs = Counter(h.belief for h in pop)
        ideologies = Counter(h.ideology for h in pop)
        archetypes = Counter(h.archetype for h in pop)

        self.history.append({
            "day": self.day,
            "population": n,
            "avg_health": sum(h.health for h in pop) / n,
            "avg_happiness": sum(h.happiness for h in pop) / n,
            "avg_wealth": sum(h.wealth for h in pop) / n,
            "tech_score": round(self.tech_score, 2),
            "era": self.era,
            "dominant_belief": beliefs.most_common(1)[0][0] if beliefs else "none",
            "dominant_ideology": ideologies.most_common(1)[0][0] if ideologies else "none",
            "belief_diversity": len(beliefs),
            "innovations_count": len(self.innovations),
            "belief_wars": self.belief_wars,
        })
        if len(self.history) > 500:
            self.history = self.history[-500:]

    def metrics(self):
        pop = self.population
        n = len(pop)
        if not self.history:
            return {"population": n, "day": self.day}

        last = dict(self.history[-1])

        beliefs = Counter(h.belief for h in pop)
        ideologies = Counter(h.ideology for h in pop)
        archetypes = Counter(h.archetype for h in pop)

        last["beliefs"] = dict(beliefs)
        last["ideologies"] = dict(ideologies)
        last["archetypes"] = dict(archetypes)
        last["innovations"] = self.innovations
        last["recent_events"] = self.events_log[-5:] if self.events_log else []
        last["notable_people"] = [
            {
                "name": h.name,
                "archetype": h.archetype,
                "belief": h.belief,
                "ideology": h.ideology,
                "influence": round(h.influence, 2),
                "age": round(h.age_days / 365),
                "last_thought": h.thoughts[-1] if h.thoughts else None,
            }
            for h in sorted(pop, key=lambda x: -x.influence)[:8]
        ]
        return last

    def to_dict(self):
        return {
            "day": self.day,
            "tech_score": self.tech_score,
            "era": self.era,
            "belief_wars": self.belief_wars,
            "innovations": self.innovations,
            "events_log": self.events_log,
            "population": [h.to_dict() for h in self.population],
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data):
        w = cls.__new__(cls)
        w.day = data["day"]
        w.tech_score = data.get("tech_score", 0.0)
        w.era = data.get("era", "Stone Age")
        w.belief_wars = data.get("belief_wars", 0)
        w.innovations = data.get("innovations", [])
        w.events_log = data.get("events_log", [])
        w.population = [Human.from_dict(h) for h in data["population"]]
        w.history = data["history"]
        return w
