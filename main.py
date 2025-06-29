import ngram
import io
import json
from flask import Flask, render_template, request, send_file, session, redirect, url_for
from datetime import datetime
#####################################################################################################
def generate_filename(name: str, extension: str) -> str:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return f"{name}_{timestamp}.{extension}"

def allowed_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext
#####################################################################################################
app = Flask(__name__,
            template_folder='templates/',
            static_folder='')

app.config['SECRET_KEY'] = 'Should be secret, not randomly generated or hardcoded. (I wont do it because it will be opensourced and I don\'t know how to do it.)'
#or you can alternatively use this (just delete the # symbols infront of them and delete the one above.)
#from os import urandom
#app.config['SECRET_KEY'] = urandom(24)
allowed_ext = ['json']
allowed_mime = ['application/json']
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
@app.route('/upload_json', methods = ['POST'])
def upload_json():    
    file = request.files['json_file']
    
    if file:
        try:
            json_bytes = file.read()
            json_string = json_bytes.decode('utf-8')
            _ngram = json.loads(json_string)

            session['ngram'] = _ngram
            return f'{_ngram}'

        except json.JSONDecodeError as e:
            return f'Error parsing JSON: The file content is not valid JSON. ({e})'
        except Exception as e:
            return f'How did we get here? \n {e}'
#####################################################################################################
if __name__ == '__main__':
    app.run(debug=True)