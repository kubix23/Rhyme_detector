import os.path
import re
import pprint

from rhymes_schema import *
from advanced_estimate import *
from simple_estimate import *
from score import *


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        text = '\n'.join([re.sub(r'[^\w\s]', '',re.sub(r'-', ' ',i.lower().strip())) for i in text.splitlines()])

        print(f"---{path}---")
        print('\n'.join([
            f"{num + 1} {' '.join([dic.inserted(j) for j in i.split()])} "
            f"{sum([len(dic.inserted(j).split('-')) for j in i.split()])}"
            for num, i in enumerate([i for i in text.splitlines() if i])]))

        print_text = [i for i in text.splitlines() if i]
        print_text_max_len = (max([len(i) for i in print_text]))

        for nnnn in range(4):
            num = 1.5 * nnnn
            print(num)
            rhymes_info = rhymes_scheme(text, lambda vv: advanced_estimate(vv, num))
            scr = score(text, "advanced", threshold=num)
            max_len = max([len(i) for i in rhymes_info["scheme_string"].splitlines()])

            data = (
                        pprint.pformat(rhymes_info["printable_rhymes_symbol"],compact=True)
                        + '\n'
                        # + pprint.pformat(advanced_estimate(text, num), compact=True)
                        # + '\n'
                        + '\n'.join(
                            [
                                str(f"{{0:{print_text_max_len}}} {{1:{max_len}}} {str([round(nn,2) for nn in j])}").format(text, i)
                                for text, i, j in zip(print_text, rhymes_info["scheme_string"].splitlines(), scr)
                            ]
                        )
                    )

            path = os.path.join(folder, "result", f"{nnnn}.txt")

            with open(path, "w", encoding="utf-8") as f:
                f.write(data)


folder = "E:/Projects/ISI/polish_poetry"

# for plik in os.listdir(folder):
#     path = os.path.join(folder, plik)
#     main(path)

main("E:/Projects/ISI/Polish_poetry/Adam Asnyk - Fale.txt")
