import asyncio
class Agent:
    def __init__(self, name): self.name=name; self.mem=[]
    async def run(self, msg, bus):
        out = f"[{self.name}] processou: {msg}"
        self.mem.append(out)
        await bus.publish("critic", out)

class Bus:
    def __init__(self): self.q={}
    async def publish(self, t, m): self.q.setdefault(t, []).append(m)

async def main():
    bus=Bus(); a=Agent("Hermes")
    await a.run("gerar relatório", bus)
asyncio.run(main())
