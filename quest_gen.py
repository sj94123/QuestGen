# A simple quest generator
#
# Austin Shafer - 2020

from nltk.tokenize import sent_tokenize
import tracery
import json
from gpt2_client import GPT2Client
import os
import nltk.data

# we need this to split things into sentences
nltk.download('punkt')

# download the gpt-2 model
# (this is from the gpt-2-simple tutorial)
model_name = "124M"
model_path = os.path.join("models", model_name)
if not os.path.isdir(model_path):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/*/

# start gpt-2
gpt2 = GPT2Client('345M') # This could also be `345M`, `774M`, or `1558M`. Rename `save_dir` to anything.
gpt2.load_model(force_download=False) # Use cached versions if available.
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
        sentences = sent_tokenize(proc_generated)

        final_quest = ""
        # generate one gpt-2 sentence for each sentence in base
        # (except the last sentence)
        for i in range(0, len(sentences) - 1):
            sent = sentences[i]
            gpt_raw = gpt2.generate_batch_from_prompts([sent])[0]
            gpt_sent = sent_tokenize(gpt_raw)[0]
            final_quest = "{} {} {}".format(final_quest, sent, gpt_sent)

        print(final_quest + sentences[len(sentences) - 1])
        print('================')
