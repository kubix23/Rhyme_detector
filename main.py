import os
from pprint import pprint

from rhymes_schema import *
from advanced_estimate import *
from simple_estimate import *
from score import *

def main(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        print(f"---{path}---")
        s1 = score(text)
        s2 = score(text,"advanced")
        s3 = score(text,"advanced", threshold=2)
        for a, b in zip(s1, s2):
            find = False
            for x, y in zip(a, b):
                if (x == 0 and y != 0) or (x != 0 and y == 0):
                    print('\n'.join([
                                        f"{num + 1} {' '.join([dic.inserted(j) for j in i.split()])} {sum([len(list(dic.iterate(j))) for j in i.split()])}"
                                        for num, i in enumerate([i for i in text.splitlines() if i])]))
                    # rhymes_scheme(text, simple_estimate)
                    # rhymes_scheme(text, advanced_estimate)
                    rhymes_scheme(text, lambda vv: advanced_estimate(vv,2))
                    # print(s1)
                    # print(s2)
                    print(s3)
                    find = True
                    break
            if find:
                break

folder = "E:/Projects/ISI/polish_poetry"

# for plik in os.listdir(folder):
#     path = os.path.join(folder, plik)
#     main(path)

main("E:/Projects/ISI/Polish_poetry/Adam Asnyk - Fantazya ludów.txt")


