def build_timeline(evidence):
    timeline = []

    for e in evidence:
        timeline.append({
            "event": e[:80],
            "time": "unknown",
            "effect": "unknown"
        })

    return timeline
