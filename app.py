from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simulation.engine import Simulation

app = FastAPI(title="CivSim", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sim = Simulation.load_or_create()

@app.get("/")
def status():
    return sim.metrics()

@app.post("/step")
def step(days: int = 1):
    sim.run(days)
    sim.save()
    return {
        "message": "Civilization advanced",
        "days": days,
        "metrics": sim.metrics()
    }

@app.get("/history")
def history():
    return sim.world.history[-200:]

@app.post("/reset")
def reset():
    from simulation.world import World
    sim.world = World.initial()
    sim.save()
    return {"message": "Civilization reset", "metrics": sim.metrics()}
