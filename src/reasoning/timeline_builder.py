def build_timeline(evidence):
    """Build a structured timeline from evidence list.
    
    Args:
        evidence: List of evidence/event strings
    
    Returns:
        List of timeline entries with event, time, and effect fields
    """
    if not evidence:
        return []
    
    timeline = []
    for i, e in enumerate(evidence):
        # Keep full event text, not truncated
        timeline.append({
            "event": e,
            "time": f"event_{i}",  # Placeholder for chronological ordering
            "effect": "under_review"  # Mark for further analysis
        })

    return timeline
