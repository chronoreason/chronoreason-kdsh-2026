def extract_claims(backstory):
    """Extract meaningful claims from backstory text.
    
    Args:
        backstory: Text containing narrative claims
    
    Returns:
        List of claim sentences
    """
    if not backstory or not backstory.strip():
        return []
    
    sentences = backstory.split(".")
    claims = []

    for s in sentences:
        s = s.strip()
        # Minimum 10 chars and max 500 chars to avoid noise and truncation
        if 10 < len(s) < 500:
            claims.append(s)

    return claims
