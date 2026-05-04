PRICES = {
    "gpt-4o-mini": {"input": 0.00015, "output": 0.00060},
    "gpt-4o":      {"input": 0.00250, "output": 0.01000},
    "gpt-3.5-turbo": {"input": 0.00050, "output": 0.00150},
    "gemini-1.5-flash": {"input": 0.000075, "output": 0.000300},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> dict:
    price = PRICES.get(model, {"input": 0.0, "output": 0.0})
    input_cost  = (input_tokens  / 1000) * price["input"]
    output_cost = (output_tokens / 1000) * price["output"]
    return {
        "input_cost":  round(input_cost,  6),
        "output_cost": round(output_cost, 6),
        "total_cost":  round(input_cost + output_cost, 6)
    }
