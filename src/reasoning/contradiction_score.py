def contradiction_score(validations):
    """Calculate contradiction score from validation results.
    
    Args:
        validations: List of validation results ('support', 'contradict', 'neutral')
    
    Returns:
        Float between 0 and 1; higher = more contradictions found
    """
    if not validations:
        return 0.0
    
    score = 0
    for v in validations:
        if v == "contradict":
            score += 1
        elif v == "neutral":
            score += 0.5

    return min(score / len(validations), 1.0)
