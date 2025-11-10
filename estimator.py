import string
from itertools import combinations, groupby, batched, permutations, accumulate
import pyphen
dic = pyphen.Pyphen(lang='pl_PL')

def simple_estimate(text):
    def count(word1: str, word2: str):
        length = 0
        for a, b in zip(word1[::-1], word2[::-1]):
            if a == b:
                length += 1
            else:
                break
        return length

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
        scores_list = [[[a, b, count(a, b), simple_score(a, b)] for a, b in g] for g in pary]
        return [(scores[0][0], [data[1:] for data in scores if data[2] > 1]) for scores in scores_list]

    words = [i.split() for i in text.splitlines() if i]
    words_line_len = [len(i.split()) for i in text.splitlines() if i]
    words_line_num = sum([[0],list(accumulate(words_line_len))],[])
    words_score = make_simple_score(sum(words,[]))
    return [words_score[words_line_num[i]:words_line_num[i+1]] for i in range(len(words))]

def score(text):
    return [[sum([i[2] for i in group]) for key,group in inn] for inn in simple_estimate(text)]

def rhymes_scheme(text):
    def rhyme_list(scores):
        letter = 'a'
        rhymes = {}
        for score in scores:
            for _, group in score:
                for i in group:
                    if i[2] != 0:
                        rhyme = i[0][-i[1]:]
                        if rhyme not in rhymes:
                            rhymes[rhyme] = letter
                            letter = chr(ord(letter) + 1)

        return rhymes

    scores =  list(simple_estimate(text))
    rhymes = rhyme_list(scores)
    scheme = [[[''.join(list(set([rhymes[i[0][-i[1]:]] if i[2] > 0 else '-' for i in group]))).strip()] if group else ['-'] for k,group in score] for score in scores]
    scheme_string = f'\n'.join(['{0:3}.\t'.format(num+1) +'|'.join(sum(i,[])) for num,i in enumerate(scheme)])

    print(rhymes)
    print(scheme_string)

with open("E:\Projects\ISI\polish_poetry\Adam Asnyk - Krąg przemian.txt", "r", encoding="utf-8") as f:
    text = f.read()
    print('\n'.join([f"{' '.join([dic.inserted(j) for j in i.split()])} {sum([len(dic.inserted(j).split('-')) for j in i.split()])}" for i in text.splitlines()]))
    rhymes_scheme(text)
    print("---")
    print([[[i for i in inn] for inn in simple_estimate(text)]])
    print(score(text))
