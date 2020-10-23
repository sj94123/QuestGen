# A simple quest generator
#
# Austin Shafer - 2020

import tracery
import json

with open('quests.json', 'r') as f:
    txt = ''.join(f.readlines())
    txt = txt.replace('\n', '')
    rules = json.loads(txt)
    grammar = tracery.Grammar(rules)
    for i in range(0, 10):
        print(grammar.flatten("#origin#"))
