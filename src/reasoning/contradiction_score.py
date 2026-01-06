def contradiction_score(validations):
    score = 0
    for v in validations:
        if v == "contradict":
            score += 1
        elif v == "neutral":
            score += 0.5

    return min(score / len(validations), 1.0)
