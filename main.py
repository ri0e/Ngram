import ngram
import io
import json
from flask import Flask, render_template, request, send_file, session
from datetime import datetime
#####################################################################################################
def generate_filename(name: str, extension: str) -> str:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return f"{name}_{timestamp}.{extension}"
#####################################################################################################
app = Flask(__name__,
            template_folder='templates/',
            static_folder='')
app.config['SECRET_KEY'] = 'Should be secret, not randomly generated or hardcoded. (I wont do it because it will be opensourced and I don\'t know how to do it.)'
#####################################################################################################
@app.route('/')
def index():
    return render_template('index.html')
#####################################################################################################
@app.route('/submit_corpus', methods=['POST'])
def submit_corpus():
    if request.method == 'POST':
        length = int(float(request.form.get('ngram_length', '2')))
        corpus = request.form.get('corpus', '')
        
        punctuations = request.form.get('punctuation_remove', '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''')
        split_by = request.form.get('split_by', ' ')
        
        ngram.punctuations = punctuations
        ngram.split_by = split_by
        
        _ngram = ngram.generate_ngram(corpus, length)
        session['ngram'] = _ngram
        
        filename = generate_filename('N-gram','json')
        
        json_string = json.dumps(_ngram, indent=4, ensure_ascii=False)
        json_bytes = json_string.encode('utf-8')
        buffer = io.BytesIO(json_bytes)
        buffer.seek(0)
        
        return send_file(buffer,
                        mimetype='application/json',
                        as_attachment = True,
                        download_name = filename)
#####################################################################################################
if __name__ == '__main__':
    app.run(debug=True)