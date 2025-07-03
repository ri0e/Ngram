import ngram

word_count = 10
_ngram = ngram.read_from_json('N-gram_2025_06_29_17_12_56.json')
text = 'I'
next_word = ngram.predict_more(_ngram, text, word_count)

print(next_word)