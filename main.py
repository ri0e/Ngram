from flask import Flask, render_template, request
import ngram

app = Flask(__name__,
            template_folder='templates/',
            static_folder='')

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/submit_corpus', methods=['POST'])
def submit_corpus():
    if request.method == 'POST':
        corpus = request.form.get('corpus')
        print(corpus)
        return f'{ngram.generate_ngram(corpus, 2)}'

if __name__ == '__main__':
    app.run(debug=True)