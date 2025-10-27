from flask import Flask
from flask import Flask,render_template
from database import fetch_data

app=Flask(__name__)

@app.route('/')
def home():
    return "hello world"

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/products')
def products():
    prods=fetch_data('products')

    return render_template('myproducts.html',my_prod=prods)


@app.route('/sales')
def sales():
    sales=fetch_data('sales')

    return render_template('my_sales.html',my_sale=sales)

@app.route('/stock')
def stock():
    stock=fetch_data('stock')

    return render_template('my_stock.html',my_stock=stock)
app.run()


