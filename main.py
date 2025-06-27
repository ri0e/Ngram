import json

def cleanup(text: str, remove_punctuation: bool = True, lowercase: bool = True, punctuations: str = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''') -> str:
    punctuation_remover = str.maketrans(' ',' ', punctuations)
    if remove_punctuation:
        new_text = text.translate(punctuation_remover)
    if lowercase:
        new_text = new_text.lower()
    return new_text

def until_last(_dict: dict, leng: int, lst: list, generate: bool = False) -> dict: 
    current_dict = _dict
    preceding_words = []
        
    if generate:
        for i in range(leng):
            key = lst[i]
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]

        return current_dict
    
    else:
        for j in range(leng):
            key = lst[j]
            preceding_words.append(key)
            current_dict = current_dict[key]
        
        return current_dict, preceding_words
    
def generate_ngram(text: str, length: int = 5, split_by: str = ' '):
    text = cleanup(text)
    words = text.split(split_by)
    del text

    word_collections = []
    ngram = {}

    for i in range(len(words) - length):
        word_collections.append(words[i: i + length])


    #Assigning counts.
    for word_collection in word_collections:
        current_dict = until_last(_dict = ngram, leng = length - 1, lst = word_collection, generate = True)

        last_word = word_collection[-1]
        if last_word not in current_dict:
            current_dict[last_word] = 1
        else:
            current_dict[last_word] += 1

    del current_dict, word_collection, last_word

    preceding_words_collection = [i[:-1] for i in word_collections]

    #Assigning probabilities.
    for word_collection in word_collections:
        current_dict, preceding_words = until_last(_dict = ngram, leng = length - 1, lst = word_collection)
        
        last_word = word_collection[-1]
        word_count = current_dict[last_word]

        sequence_occurence = preceding_words_collection.count(preceding_words)

        if isinstance(word_count, int):
            probability = word_count / sequence_occurence
            current_dict[last_word] = probability
        else:
            probability = 1e-4321

        with open('N-gram(readable).txt', 'w') as txt:
            for i in preceding_words:
                txt.write(i)
            txt.write(last_word, probability)    
    return ngram


with open('Corpus.txt', 'r') as o:
    with open('N-gram.json', 'w') as w:
        json.dump(generate_ngram(o.read()), w, indent = 4)