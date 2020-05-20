from app import app
from flask import render_template
from flaskext.markdown import Markdown
from app.forms import ProductForm
app.config['SECRET_KEY'] = '98dahs8da9h8jdjddj'
from app.models import Product, Opinion
import requests

Markdown(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/extract', methods = ['POST','GET'])
def extract():
    form = ProductForm()
    if form.validate_on_submit():
        page_response = requests.get('https://www.ceneo.pl/'+request.form['product_code'])
        if page_response.status_code == 200:
            product = Product(request.form['product_code'])
            return "OK"
        else:
            form.product_code.errors.append("Dla podanego kodu nie ma produktu")
            return render_template('extract.html', form=form)
    return render_template('extract.html', form=form)

@app.route('/products')
def products():
    pass

@app.route('/product/<product_id>')
def product():
    pass

@app.route('/about')
def about():
    content = ''
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('about.html', text=content)

@app.route('/analyzer/<product_id>')
def analyzer():
    return "Podaj kod produktu do analizy"