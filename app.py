import ngram
import io
import json
from flask import Flask, render_template, request, send_file, session, jsonify
from datetime import datetime

def generate_filename(name: str, extension: str) -> str:
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return f'{name}_{timestamp}.{extension}'

def allowed_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext

app = Flask(__name__,)

with open('config.json', 'r') as Cg:
    config = json.load(Cg)
app.config.update(config)

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
        message = 'No file part in the request.'
        status = 'error'
        return jsonify(status = status, message = message)
    
    file = request.files['json_file']
    
    if file.filename == '':
        message = 'No selected file.'
        status = 'error'
        return jsonify(status = status, message = message)

    if file:
        try:
            json_bytes = file.read()
            json_string = json_bytes.decode('utf-8')
            _ngram = json.loads(json_string)

            session['ngram'] = _ngram
            
            message = 'File uploaded and parsed successfully!'
            status = 'success'
            return jsonify(status = status, message = message)

        except json.JSONDecodeError as e:
            message = f'Error parsing JSON: File content is not valid JSON. <br> ({e})'
            status = 'error'
            return jsonify(status = status, message = message)
        except Exception as e:
            message = f'An unexpected error occurred during processing: <br> {e}'
            status = 'error'
            return jsonify(status = status, message = message)
        
    message = 'Something went wrong with the upload. Please try again.'
    status = 'error'
    return jsonify(status = status, message = message)
    
@app.route('/predict_text', methods = ['POST'])
def predict_text():
    text = request.form.get('user_input', '')
    choose = 'choose' in request.form
    predict_many = 'predict_many' in request.form
    
    if 'ngram' not in session:
        message = 'No N-gram data found in session. Please upload or generate one first.'
        status = 'error'
        return jsonify(status = status, message = message)
    
    try:
        if predict_many:
            word_count = int(float(request.form.get('word_count', 3)))
            next_word = ngram.predict_more(session['ngram'], text, word_count)
        else:
            next_word = ngram.predict_next_word(session['ngram'], text, choose)
            
        return jsonify(next_word = next_word)
    
    except Exception as e:
        message = f'Could not predict the next word: <br> {e}'
        status = 'error'
        return jsonify(status = status, message = message)

if __name__ == '__main__':
    app.run(port = 36363)