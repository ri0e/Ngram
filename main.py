import ngram
import io
import json
from flask import Flask, render_template, request, send_file, session, redirect, url_for
from datetime import datetime

def generate_filename(name: str, extension: str) -> str:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return f"{name}_{timestamp}.{extension}"

def allowed_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext

app = Flask(__name__,
            template_folder='templates/',
            static_folder='')

from os import urandom
app.config['SECRET_KEY'] = urandom(128)

allowed_ext = ['json']
allowed_mime = ['application/json']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_corpus', methods=['POST'])
def submit_corpus():
    if request.method == 'POST':
        length = int(float(request.form.get('ngram_length', '2')))
        corpus = request.form.get('corpus', '')
        
        punctuations = request.form.get('punctuation_remove', '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''')
        #split_by = request.form.get('split_by', ' ')
        
        _ngram = ngram.generate_ngram(corpus, length, punctuations = punctuations)
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

@app.route('/upload_json', methods = ['POST'])
def upload_json():
    if 'json_file' not in request.files:
        return redirect(url_for('index', message = "No file part in the request.", status = "error"))
    
    file = request.files['json_file']
    
    if file.filename == '':
        return redirect(url_for('index', message = "No selected file.", status = "error"))

    if file:
        try:
            json_bytes = file.read()
            json_string = json_bytes.decode('utf-8')
            _ngram = json.loads(json_string)

            session['ngram'] = _ngram
            
            return redirect(url_for('index', message = "File uploaded and parsed successfully!", status = "success"))

        except json.JSONDecodeError as e:
            return redirect(url_for('index', message = f'Error parsing JSON: File content is not valid JSON. ({e})', status = "error"))
        except Exception as e:
            return redirect(url_for('index', message = f'An unexpected error occurred during processing: {e}', status = "error"))
        
    return redirect(url_for('index', message = "Something went wrong with the upload. Please try again.", status = "error"))
#####################################################################################################
@app.route('/predict_text', methods = ['POST'])
def predict_text():
    text = request.form.get('user_input', '')
    choose = 'choose' in request.form
    if 'ngram' not in session:
        return redirect(url_for('index', message = "No N-gram data found in session. Please upload or generate one first.", status = "error"))
    
    try:
        next_word = ngram.predict_next_word(session['ngram'], text, choose)
        return f'{next_word}'
    except Exception as e:
        return redirect(url_for('index', message = f"Could not predict the next word: {e}", status = "error"))

if __name__ == '__main__':
    app.run()