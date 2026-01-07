def final_decision(score, threshold=0.6):
    """Determine narrative consistency based on contradiction score.
    
    Args:
        score: Contradiction score (0-1; higher = more contradictions)
        threshold: Threshold above which narrative is considered inconsistent (default 0.6)
    
    Returns:
        1 if consistent (score < threshold), 0 if inconsistent (score >= threshold)
    """
    return 1 if score < threshold else 0
