PRICE = {"gpt-4o": 0.005, "gemini-1.5-pro": 0.0035}  # por 1k tokens
def cost(model, p, c):
    r = PRICE.get(model, 0.01)
    return round((p + c)/1000 * r, 4)
