from flask import Flask, render_template, request, send_file, make_response
import ngram

app = Flask(__name__,
            template_folder='templates/',
            static_folder='')
app.config['SECRET_KEY'] = 'Enter what ever you want here (I wont because it will be opensourced)'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_corpus', methods=['POST'])
def submit_corpus():
    if request.method == 'POST':
        punctuations = request.form.get('punctuation_remove', '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''')
        length = int(float(request.form.get('ngram_length', '2')))
        corpus = request.form.get('corpus', '')
        
        return f'punctuation {punctuations} <br> {ngram.generate_ngram(corpus, length)}'

if __name__ == '__main__':
    app.run(debug=True)