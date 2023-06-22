from app import app
from flask import render_template, request, redirect, url_for
from scraper import scraper

@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/', methods=['GET', 'POST'])
def run_scraper():
    if request.method == 'POST':
        code = request.form['code']
        print(code)
        return redirect(url_for('results'))
    else:
        return render_template('index.html.jinja')
    
@app.route('/results')
def results():
    return render_template('results.html')
    