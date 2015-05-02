import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from classifier import Classifier
from visualizer import Visualizer

UPLOAD_FOLDER = 'user_data/'
ALLOWED_EXTENSIONS = set(['csv'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def diagnosis_result(filepath):
	clf = Classifier(filepath)
	template_obj = {}
	template_obj['network_vis'] = True
	results = [clf.test1(), clf.test2(), clf.test3()]
	total = sum(results)
	if total == 0:
		template_obj['diagnosis_text'] = 'Congratulations! Subject is not diagnosed with Schizophrenia.'
	else:
		frac = float(total) / float(len(results)) * 100
		template_obj['diagnosis_text'] = 'Subject has been diagnosed with Schizophrenia with a confidence of ' + '%.2f' % frac + '%.'
	for i in range(total):
		template_obj['star' + str(i)] = 'glyphicon-star'
	for i in range(total, 3):
		template_obj['star' + str(i)] = 'glyphicon-star-empty'
	template_obj['transitivity'] = clf.features[3]
	template_obj['efficiency'] = clf.features[2]
	template_obj['closeness'] = clf.features[5]
	template_obj['opt_modularity'] = clf.features[4]
	template_obj['assortativity'] = clf.features[1]

	v = Visualizer(filepath)
	transformed_G = v.transform_adjmat()
	uniq_id = '/json/' + v.write_json(transformed_G)
	template_obj['uniq_id'] = uniq_id
	return template_obj

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test_data():
	if request.method == 'POST':
		file = request.files['csvfile']
		if file and allowed_file(file.filename):
			# Upload the file
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(filepath)
			template_obj = diagnosis_result(filepath)
			return render_template('test_results.html', **template_obj)

@app.route('/json/<uniq_id>')
def fetch_json(uniq_id):
	with open('user_data/' + uniq_id, 'r') as f:
		data = f.read()
		return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
