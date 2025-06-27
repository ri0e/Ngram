import ngram
import json

with open('Corpus.txt', 'r') as o:
    with open('N-gram.json', 'w') as w:
        json.dump(ngram.generate_ngram(o.read()), w, indent = 4)