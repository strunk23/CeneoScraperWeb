import os
from os import listdir
from os.path import isfile, join
from app import app
from scraper import scraper
from flask import render_template, request, redirect, url_for, json


@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/', methods=['GET', 'POST'])
def run_scraper():
    if request.method == 'POST':
        global code
        code = request.form['code']
        onlyfiles = [f for f in listdir('opinions') if isfile(join('opinions', f))]
        all_codes = [f[:-5] for f in onlyfiles]
        if code not in all_codes:
            scraper.scraper(code)
        return redirect(url_for('results'))
    else:
        return render_template('index.html.jinja')
    
@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html.jinja', jsonfile=json.dumps(json.load(open(f'opinions/{code}.json', encoding='utf-8'))))
    