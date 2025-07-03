from json import load,dump
import random

split_by: str = ' '

def cleanup(text: str, punctuations: str, remove_punctuation: bool = True, lowercase: bool = True) -> str:
    _punctuation_remover = str.maketrans(' ',' ', punctuations)
    
    if remove_punctuation:
        new_text = text.translate(_punctuation_remover)
    if lowercase:
        new_text = new_text.lower()
    return new_text

def until_last(current_dict: dict, leng: int, lst: list, generate: bool = False) -> dict: 
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
            current_dict = current_dict[key]
            preceding_words.append(key)
        
        return current_dict, preceding_words
    
def generate_ngram(text: str, length: int = 3, file_write: bool = True, punctuations: str = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''):
    text = cleanup(text, punctuations = punctuations)
    words = text.split(split_by)

    word_collections = []
    ngram = {}
    ngram['___length___'] = length

    for i in range(len(words) - length):
        word_collections.append(words[i: i + length])

    #Assigning counts.
    for word_collection in word_collections:
        current_dict = until_last(current_dict = ngram, leng = length - 1, lst = word_collection, generate = True)

        last_word = word_collection[-1]
        if last_word not in current_dict:
            current_dict[last_word] = 1
        else:
            current_dict[last_word] += 1

    preceding_words_collection = [i[:-1] for i in word_collections]

    with open('N-gram(readable).txt', 'w') as txt:
        #Assigning probabilities.
        for word_collection in word_collections:
            current_dict, preceding_words = until_last(current_dict = ngram, leng = length - 1, lst = word_collection)
            
            last_word = word_collection[-1]
            word_count = current_dict[last_word]

            sequence_occurence = preceding_words_collection.count(preceding_words)

            if isinstance(word_count, int):
                probability = word_count / sequence_occurence
                current_dict[last_word] = probability
            else:
                probability = 1e-4321

            if file_write:
                for i in preceding_words:
                    txt.write(f'{i} -> ')
                txt.write(f'{last_word} : {probability}\n')
                
    return ngram

def predict_next_word(model: dict, text:str, choose: bool = True):
    words = cleanup(text = text, punctuations = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''').split(split_by)
    
    try:
        length: int = model['___length___']
    except Exception as e:
        return e
        
    leng = length - 1
    preceding_words = words[-leng:]
    
    last_dict = until_last(model, leng, preceding_words)[0]
    
    words = list(last_dict.keys())
    probabilities = list(last_dict.values())
    
    if choose:
        choice = random.choices(population = words, weights = probabilities, k = 1)[0]
    else:
        choice = [x for x,_ in sorted(list(zip(words, probabilities)), key = lambda x: x[1])][::-1]
    return choice

def predict_more(model: dict, text: str, word_count: int):
    sentence = f'{text} {predict_next_word(model, text)}'
    for i in range(word_count - 1):
        try:
            sentence += f' {predict_next_word(model, sentence)}'
        except:
            sentence += f' <UNAVAILABLE>'
            
    return sentence

def read_from_json(file: str = 'N-gram.json') -> dict:
    with open(file, 'r') as N:
        ngram = load(N)
    return ngram

def write_to_json(model: dict, file: str = 'N-gram.json') -> None:
    with open(file, 'w') as N:
        dump(model)
    return None

def add_to_json(model: dict, file: str = 'N-gram.json') -> None:
    with open(file, 'a') as N:
        dump(model)
    return None