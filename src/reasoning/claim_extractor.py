def extract_claims(backstory):
    sentences = backstory.split(".")
    claims = []

    for s in sentences:
        s = s.strip()
        if len(s) > 10:
            claims.append(s)

    return claims
