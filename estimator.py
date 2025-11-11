import string
from itertools import combinations, groupby, batched, permutations, accumulate
import pyphen
dic = pyphen.Pyphen(lang='pl_PL')

def simple_estimate(text):
    def rhyme_find(word1: str, word2: str):
        rhyme = ''
        for a, b in zip(word1[::-1], word2[::-1]):
            if a == b:
                rhyme += a
            else:
                break
        return rhyme

    def simple_score(word1: str, word2: str):
        score = 0
        if word1 != word2:
            for a, b in zip(word1[::-1], word2[::-1]):
                if a == b:
                    score += 1
                else:
                    break
        else:
            score = 0
        return score

    def make_simple_score(words):
        pary = batched(permutations(words, 2),len(words)-1)

        scores_list = \
        [
            [
                (
                    a,
                    {
                        "word": b,
                        "count": len(rhyme_find(a, b)),
                        "rhyme": rhyme_find(a, b),
                        "score": simple_score(a, b),
                    }
                )
                for a, b in g
            ]
            for g in pary
        ]
        return [
            {
                "word": scores[0][0],
                "matches": [ data[1] for data in scores if data[1]["count"] > 1]
            }
            for scores in scores_list
        ]

    words = [i.split() for i in text.splitlines() if i]
    words_line_len = [len(i.split()) for i in text.splitlines() if i]
    words_line_num = sum([[0],list(accumulate(words_line_len))],[])
    words_score = make_simple_score(sum(words,[]))
    return [words_score[words_line_num[i]:words_line_num[i+1]] for i in range(len(words))]

def score(text):
    return [
        [
            sum([i["score"] for i in word["matches"]])
            for word in line
        ]
    for line in simple_estimate(text)
    ]

def rhymes_scheme(text):
    def rhyme_list(scores):
        letter = 'a'
        rhymes = {}
        for score in scores:
            for words in score:
                for i in words["matches"]:
                    if i["score"] != 0:
                        rhyme = i["rhyme"]
                        if rhyme not in rhymes:
                            rhymes[rhyme] = chr(ord(list(rhymes.values())[-1])+1) if rhymes else 'a'

        return rhymes

    scores =  simple_estimate(text)
    rhymes = rhyme_list(scores)
    scheme = \
    [
        [
            ''.join(list(set([rhymes[match["rhyme"]] for match in word["matches"] if match["score"] > 0])))
            for word in line
        ]
        for line in scores
    ]
    scheme = [[j if j else '-' for j in i] for i in scheme]

    scheme_string = f'\n'.join(['{0:3}.\t'.format(num+1) +'|'.join(line) for num,line in enumerate(scheme)])

    print(rhymes)
    print(scheme_string)

with open("E:\Projects\ISI\polish_poetry\Adam Asnyk - Krąg przemian.txt", "r", encoding="utf-8") as f:
    text = f.read()
    print('\n'.join([f"{' '.join([dic.inserted(j) for j in i.split()])} {sum([len(dic.inserted(j).split('-')) for j in i.split()])}" for i in text.splitlines()]))
    rhymes_scheme(text)
    print("---")
    print([[[i for i in inn] for inn in simple_estimate(text)]])
    print(score(text))
