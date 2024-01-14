import random
import re

from parsimonious import Grammar

pre_parse = re.compile(r"(?<!\\){.*?}")
grammar = Grammar(open("pytelebotter/randomizer/grammar.peg").read())


def parse_and_randomize(text: str):
    for i in pre_parse.finditer(text):
        possible_variants = []
        parsed_expression = grammar.parse(i.group(0))
        for j in parsed_expression.children[1].children:
            possible_variants.append(j.children[0].text.strip())

        text = pre_parse.sub(random.choice(possible_variants), text, count=1)

    return text
