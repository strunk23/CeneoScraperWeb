import os
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
        scraper.scraper(str(code))
        return redirect(url_for('results'))
    else:
        return render_template('index.html.jinja')
    
@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html.jinja', jsonfile=json.dumps(json.load(open(f'scraper/opinions/{code}.json', encoding='utf-8'))))
    