import os
from os import listdir
from os.path import isfile, join
from app import app
from scraper.scraper import scraper
from scraper.analyzer import analyzer
from flask import render_template, request, redirect, url_for, send_file


code_file = 'app/static/codes.txt'
opinions_file = 'app/static/opinions'

@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/', methods=['GET', 'POST'])
def run_scraper():
    if request.method == 'POST':
        global code
        code = request.form['code']
        with open(code_file, 'w+') as f:
            f.write(code)
            f.close()
        onlyfiles = [f for f in listdir(opinions_file) if isfile(join(opinions_file, f))]
        all_codes = [f[:-5] for f in onlyfiles]
        if code not in all_codes:
            scraper(code)
            analyzer(code)
        return redirect(url_for('results', id=code))
    else:
        return render_template('index.html.jinja')
    
@app.route('/results/<id>', methods=['GET', 'POST'])
def results(id):
    with open(code_file, 'r') as f:
        code = f.read()
        f.close()
    paths = []
    paths.append(f'img/{id}_bar.png')
    paths.append(f'img/{id}_pie.png')
    return render_template('results.html.jinja', paths=paths, code=code)

@app.route('/download', methods=['GET', 'POST'])
def download():
    with open(code_file, 'r') as f:
        code = f.read()
        f.close()
    path = f'static/opinions/{code}.json'
    return send_file(path, as_attachment=True)
    