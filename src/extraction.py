def check_keywords(text, keywords):
    score = 0
    found = []

    for k in keywords:
        if k.lower() in text:
            score += 1
            found.append(k)

    return score, found
