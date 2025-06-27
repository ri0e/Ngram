import json

punctuation_remover = str.maketrans("","",'''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''')

def generate_ngram(text, ngrams, split_by = ' '):
    words = text.translate(punctuation_remover).lower().split(split_by)
    output = []
    for index in range(len(words) - ngrams+1):
        output.append(tuple(words[index : index + ngrams]))
    return tuple(output)

def sort_ngram(ngrams):
    ngram_with_frequency = {}
    for ngram in ngrams:
        ngram_with_frequency[ngram] = ngram_with_frequency.get(ngram, 0) + 1
    list_of_ngrams = sorted(ngram_with_frequency.items(), key = lambda x: x[1], reverse = True)
    return tuple(list_of_ngrams)


with open('Corpus.txt','r') as c:
    cr = c.read()
    ngram_ = sort_ngram(generate_ngram(cr, 2))
    print(ngram_)
    with open('N-gram.txt','w') as o:
        ngrams = ngram_
        for ngram in ngrams:
            o.write(f'{ngram[0]}: {ngram[1]}')
            o.write('\n')
    with open('N-gram.json', 'w') as f:
        json.dump(ngram_, f, indent = 3)

print('done')