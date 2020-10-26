# A simple quest generator
#
# Austin Shafer - 2020

import tracery
import json
import gpt_2_simple as gpt2
import os
import nltk.data

# we need this to split things into sentences
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# download the gpt-2 model
# (this is from the gpt-2-simple tutorial)
model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/*/

# start gpt-2
sess = gpt2.start_tf_sess()
# TODO: finetune?

# open our tracery grammar
with open('quests.json', 'r') as f:
    # fold it into one line so json can load it
    txt = ''.join(f.readlines())
    txt = txt.replace('\n', '')
    rules = json.loads(txt)
    grammar = tracery.Grammar(rules)
    for i in range(0, 10):
        print()
        print('===== quest =====')
        # generate a procedural quest using tracery
        proc_generated = grammar.flatten("#origin#")
        # split it into sentences
        sentences = tokenizer.tokenize(proc_generated)

        final_quest = ""
        # generate one gpt-2 sentence for each sentence in base
        # (except the last sentence)
        for i in range(0, len(sentences) - 1):
            sent = sentences[i]
            gpt_sent = gpt2.generate(sess)
            final_quest = final_quest + sent + gpt_sent

        print(final_quest)
        print('=========== =====')
