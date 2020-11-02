# A simple quest generator
#
# Austin Shafer - 2020

from nltk.tokenize import sent_tokenize
import tracery
import json
from prompted import generate_prompted
import os
import nltk.data
from flask import Flask
from flask import request
app = Flask(__name__)

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
# TODO: finetune?

# open our tracery grammar
f = open('quests.json', 'r')
# fold it into one line so json can load it
txt = ''.join(f.readlines())
txt = txt.replace('\n', '')
rules = json.loads(txt)
grammar = tracery.Grammar(rules)

@app.route("/quest_gen", methods=["GET"])
def quest_gen():
	sent = request.args.get("sent")
	gpt_raw = generate_prompted(model_name=model_name, temperature=0.2, length=64, top_k=40, prompt=sent)
	gpt_sent = sent_tokenize(gpt_raw)[0]
	return gpt_sent

app.run(port=1234)
