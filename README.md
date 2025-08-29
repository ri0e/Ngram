# N-gram
A simple N-gram model that utilizes dictionaries to achieve its purpose. This N-gram model provides a modular approach for generating and reading N-grams.
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
## usage for the Python library
Download the `ngram.py` file and use the library by typing.
```
import ngram
```
Into your working space.
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
#### Replacing the entire file
```
write_to_json(model, file)
```
- model(dict) - your generated ngram.
- file (str["N-gram.json"]) - Json file to write. (Default N-gram.json)
#### Adding to the file
```
add_to_json(model, file)
```
- model(dict) - your generated ngram.
- file (str["N-gram.json"]) - Json file to write. (Default N-gram.json)
### Reading from file
```
read_from_json(file)
```
- file (str["N-gram.json"]) - Json file to write. (Default N-gram.json)
### Using the ngram for prediction
#### Single word/ list of words
```
predict_next_word(model, text, choose)
```
- model(dict) - your ngram.
- text(str) - text to predict from.
- choose(bool) - whether to return one word or a list of words. (Default True)
#### More words
```
predict_more(model, text, word_count)
```
An extension to predict_next_word.
- model(dict) - your ngram.
- text(str) - text to predict from.
- word_count(int) - the number of words you want to predict.
## Usage example
I made a website using this library, which you can check out here https://ngram-lyart.vercel.app/.
