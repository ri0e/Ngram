# N-gram
Simple N-gram model that utilizes dictionaries to achieve its purpose. This N-gram model provides a modular approach for gernerating and reading N-grams.
It basically uses nested dictionaries in this way: (for bigrams)
```
'word1': {
.  'word2': 0.5
.  'Wordn': 0.5
}
'word2': {
.   'word3': 1
} ...
```
## usage for the python library
```
import ngram
```
### Generating N-gram
```
generate_ngram(text, ngramLength, file_write, punctuations)
```
- text (str) -- The text you want to generate your ngram from.
- ngramLength (int) -- the length of the ngram to generate (2 generates two pairs and so on.) (Default 2)
- file_write (bool) -- Whether you want to write a text file containing another representation of the ngram. (Default True)
- punctuations (str) -- Symbols to remove. (Default !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
```
word1 -> word2 : probability
```
### Writing to file
```
write_to_json(ngram, file)
```
- ngram (dict) - your generated ngram.
- file (str["N-gram.json"]) - Json file to write. (Default N-gram.json)
### Reading from file
```
ngram = read_from_json(file)
```
- file (str["N-gram.json"]) - Json file to write. (Default N-gram.json)
- ngram - variable to hold the ngram.
