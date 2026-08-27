PRICING = {"mini": {"in":0.15/1e6, "out":0.60/1e6}, "maxi": {"in":3.0/1e6, "out":15.0/1e6}}
def route_model(intent): return "maxi" if intent in ("proposta","analise_complexa") else "mini"
def cost(task, cache_hit=False):
    m = PRICING[route_model(task["intent"])]
    return (task["in"]*m["in"] + task["out"]*m["out"]) * (0.0 if cache_hit else 1.0)
t = {"intent":"triagem","in":500,"out":200}
print(round(cost(t),6), round(cost(t, cache_hit=True),6))
