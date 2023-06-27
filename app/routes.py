import os
from os import listdir
from os.path import isfile, join
from app import app
from scraper.scraper import scraper
from scraper.analyzer import analyzer
from flask import render_template, request, redirect, url_for


img = os.path.join('static', 'Image')

@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/', methods=['GET', 'POST'])
def run_scraper():
    if request.method == 'POST':
        global code
        code = request.form['code']
        onlyfiles = [f for f in listdir('app/static/opinions') if isfile(join('app/static/opinions', f))]
        all_codes = [f[:-5] for f in onlyfiles]
        if code not in all_codes:
            scraper(code)
            analyzer(code)
        return redirect(url_for('results', id=code))
    else:
        return render_template('index.html.jinja')
    
@app.route('/results/<id>', methods=['GET', 'POST'])
def results(id):
    return render_template('results.html.jinja')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'GET':
        code = request.args.get['code']
        path = f'app/static/opinions/{code}.json'
        return path
    return "None"
    