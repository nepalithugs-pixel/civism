# CivSim v2 — Chronicle of Civilizations

A human civilization growth simulation with beliefs, religion, ideology, politics, archetypes, thought injection, and a rich visual frontend.

## Setup

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Then open `civsim_frontend.html` in your browser, set the API URL to `http://localhost:8000`.

## API Endpoints

- `GET /` — Current civilization metrics (beliefs, ideologies, archetypes, notable people, events)
- `POST /step?days=365` — Advance the simulation by N days
- `GET /history` — Full population & tech history (last 200 records)
- `POST /reset` — Reset to a fresh civilization

## What's New in v2

### Humans
- Names, archetypes (philosopher, warrior, priest, farmer, merchant, healer, artist, explorer, leader, outcast)
- **Belief systems**: animism, polytheism, monotheism, atheism, shamanism, ancestor worship, nature worship, sun worship, agnosticism, mysticism
- **Ideologies**: tribalism, collectivism, individualism, egalitarianism, hierarchy, expansionism, isolationism, pacifism, militarism, meritocracy
- **Conviction** and **influence** — high-influence priests/leaders spread beliefs to others
- Beliefs and ideologies are **inherited** by children (with mutation)
- Spirituality as a 7th drive

### Thought Injection System
Each day, individuals may receive a **thought event** — a moment of insight, spiritual revelation, or cultural shift that alters their drives. 25 unique thought events ranging from eclipse-induced spiritual awakenings to trade encounters with foreign gods.

### World Events
- **Belief wars** — when two faiths conflict, casualties occur
- **Spiritual awakenings** — mass shifts in spirituality
- **Innovations** — wheel, writing, agriculture, metallurgy, etc. unlock tech bonuses
- Disease, famine, disasters

### Eras
Stone Age → Bronze Age → Iron Age → Classical Age → Medieval Age → Renaissance → Industrial Age → Information Age

### Frontend
A dark parchment-and-gold aesthetic inspired by ancient chronicles. Live charts, belief breakdowns, notable individuals with their last thoughts, event chronicles, innovation tracking.
