def score_prompt(prompt: str) -> int:
    score = 0
    prompt_lower = prompt.lower()

    # Uzunluq
    words = len(prompt.split())
    if words > 50:
        score += 3
    elif words > 20:
        score += 1

    # Mürəkkəb açar sözlər
    complex_keywords = [
        "analiz et", "müqayisə et", "izah et", "niyə", "necə işləyir",
        "fərq nədir", "ətraflı", "hesabla", "sübut et", "architecture",
        "explain", "analyze", "compare", "difference", "complex", "detailed"
    ]
    for word in complex_keywords:
        if word in prompt_lower:
            score += 2

    # Kod sualları
    code_keywords = ["kod yaz", "funksiya", "class", "python", "javascript",
                     "write code", "function", "implement", "debug"]
    for word in code_keywords:
        if word in prompt_lower:
            score += 2

    # Sual işarəsi sayı
    score += prompt.count("?")

    return score


def select_model(prompt: str) -> dict:
    score = score_prompt(prompt)

    if score >= 6:
        model = "gpt-4o"
        reason = f"Mürəkkəb sual (score={score}) → bahalı model"
    elif score >= 3:
        model = "gpt-4o-mini"
        reason = f"Orta sual (score={score}) → ucuz model"
    else:
        model = "gpt-4o-mini"
        reason = f"Sadə sual (score={score}) → ucuz model"

    return {
        "model": model,
        "score": score,
        "reason": reason
    }
