from itertools import groupby
from operator import itemgetter
from pprint import pprint
from typing import Callable

def rhymes_scheme(text, estimate_func: Callable):
    def rhyme_list(scores):
        rhymes_symbol = {}
        for score in scores:
            for words in score:
                for matche in words["matches"]:
                    if matche["score"] != 0:
                        rhyme = matche["rhyme_target"]
                        if rhyme not in rhymes_symbol:
                            if "rhyme_source" in matche and matche["rhyme_source"] in rhymes_symbol:
                                rhymes_symbol[rhyme] = rhymes_symbol[matche["rhyme_source"]]
                            else:
                                rhymes_symbol[rhyme] = chr(ord(list(rhymes_symbol.values())[-1]) + 1) if rhymes_symbol else 'a'

        return rhymes_symbol

    scores = estimate_func(text)
    rhymes_symbol = rhyme_list(scores)
    scheme = \
    [
        [
            temp
            if (temp := ''.join(
                list(set(
                    [
                        rhymes_symbol[match["rhyme_target"]]
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
    printable_rhymes_symbol = {
        key: x[0] if len(x := [i[0] for i in group]) == 1 else x
        for key,group in groupby(sorted(rhymes_symbol.items(), key= lambda rhyme: rhyme[1]), lambda rhyme: rhyme[1])
    }
    scheme_string = f'\n'.join(['{0:3}.\t'.format(num+1) +'|'.join(line) for num,line in enumerate(scheme)])

    pprint(printable_rhymes_symbol)
    print(scheme_string)