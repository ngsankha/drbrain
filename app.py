import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from classifier import Classifier

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
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(filepath)
			clf = Classifier(filepath)
			return str([clf.test1(), clf.test2(), clf.test3()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
