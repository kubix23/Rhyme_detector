def score(text, type = '', threshold = 0):
    match type.lower():
        case 'advanced':
            from advanced_estimate import advanced_estimate
            return [
                [
                    sum([i["score"] for i in word["matches"]])
                    for word in line
                ]
                for line in advanced_estimate(text, threshold)
            ]
        case _:
            from simple_estimate import simple_estimate
            return [
                [
                    sum([i["score"] for i in word["matches"]])
                    for word in line
                ]
                for line in simple_estimate(text)
            ]