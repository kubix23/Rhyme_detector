import string
from itertools import combinations, groupby, batched, permutations, accumulate
import pyphen
from collections.abc import Iterable
dic = pyphen.Pyphen(lang='pl_PL')

def simple_estimate(text: str):
    def rhyme_find(word1, word2):
        rhyme = ''
        split_word1 = word1["syllables"]
        split_word2 = word2["syllables"]

        for a, b in zip(split_word1[::-1], split_word2[::-1]):
            if a == b:
                rhyme = a + rhyme
            else:
                break
        return \
            {
                "rhyme": rhyme
            }

    def simple_score(rhyme: str,word_source, word_target):
        if word_source["word"] != word_target["word"]:
            score = len(rhyme)
        elif len(word_source["word"]) > 1 or word_source["word_num"] == 0:
            score = 1
        else:
            score = 0
        return score

    def make_simple_score(words):
        return [
            {
                "word": key,
                "matches": [
                    {
                        "word": word_target["word"],
                        "rhyme": rhyme,
                        "rhyme_len": len(rhyme),
                        "score": simple_score(rhyme, word_source, word_target),
                    }
                    for word_source, word_target in group
                    if word_source["line_num"] - 4 <= word_target["line_num"] <= word_source["line_num"] + 4
                       and word_source["word_num"] - 1 <= word_target["word_num"] <= word_source["word_num"] + 1
                       and (rhyme := rhyme_find(word_source, word_target))
                ]
            }
            for key,group in groupby(permutations(words, 2), lambda x: x[0]["word"])
        ]

    words = [
        [
            {
                "line_num":line_num,
                "word_in_line":len(line.split())-1,
                "word_num":word_num,
                "syllables":dic.inserted(word).split('-'),
                "syllables_num_start":sum([len(dic.inserted(i).split('-')) for i in line.split()]),
                "word":word
            }
            for word_num,word in enumerate(line.split())
        ]
        for line_num,line in enumerate(text.splitlines())
        if line
    ]

    words_line_len = [len(i) for i in words]
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
        rhymes_symbol = {}
        for score in scores:
            for words in score:
                for i in words["matches"]:
                    if i["score"] != 0:
                        rhyme = i["rhyme"]
                        if rhyme not in rhymes_symbol:
                            rhymes_symbol[rhyme] = chr(ord(list(rhymes_symbol.values())[-1]) + 1) if rhymes_symbol else 'a'

        return rhymes_symbol

    scores = simple_estimate(text)
    rhymes_symbol = rhyme_list(scores)
    scheme = \
    [
        [
            temp
            if (temp := ''.join(
                list(set(
                    [
                        rhymes_symbol[match["rhyme"]]
                        for match in word["matches"]
                        if match["score"] > 0
                    ]
                ))
            ))
            else '-'
            for word in line
        ]
        for line in scores
    ]
    scheme_string = f'\n'.join(['{0:3}.\t'.format(num+1) +'|'.join(line) for num,line in enumerate(scheme)])

    print(rhymes_symbol)
    print(scheme_string)

with open("E:\Projects\ISI\polish_poetry\Adam Asnyk - Do Sokołów.txt", "r", encoding="utf-8") as f:
    text = f.read()
    print('\n'.join([f"{' '.join([dic.inserted(j) for j in i.split()])} {sum([len(dic.inserted(j).split('-')) for j in i.split()])}" for i in text.splitlines()]))
    rhymes_scheme(text)
    print("---")
    print(score(text))
