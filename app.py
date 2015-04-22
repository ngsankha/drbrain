import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = 'user_data/'
ALLOWED_EXTENSIONS = set(['csv'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test_data():
	if request.method == 'POST':
		file = request.files['csvfile']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return 'file uploaded'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
