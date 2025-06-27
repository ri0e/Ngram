# N-gram
Simple N-gram model that utilizes dictionaries to achieve its purpose. This N-gram model provides a modular approach to gernerating (and reading hopefully) N-grams.
It basically uses nested dictionaries in this way: (for trigram)
```
'word1': {
.  'word2': 0.5
.  'Wordn': 0.5
}
'word2': {
.   'word3': 1
} ...
```
(sorry if you couldn't understand this you can watch the devlogs I have posted if you want more information on this or even ask me.) (will update this later)
## usage
```
import ngram
```
Then call on the function:
```
generate_ngram(text, ngramLength, file_write)
```
- text (str) -- The text you want to generate your ngram from.
- ngramLength (int) -- the length of the ngram to generate (2 generates two pairs and so on.)
- file_write (bool) -- Whether you want to write a text file containing another representation of the ngram.
```
word1 -> word2 : probability
``` 