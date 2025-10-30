from flask import Flask,render_template,request,redirect,url_for
from database import fetch_data,insert_products,insert_sales,insert_stock

app=Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')

# products route
@app.route('/products')
def products():
    prods=fetch_data('products')

    return render_template('myproducts.html',my_prod=prods)

# sales route
@app.route('/sales')
def sales():
    sales=fetch_data('sales')
    products=fetch_data('products')

    return render_template('my_sales.html',my_sale=sales,products=products)
# stock route
@app.route('/stock')
def stock():
    stock=fetch_data('stock')
    products=fetch_data('products')

    return render_template('my_stock.html',my_stock=stock,products=products)

# create a python function that receives data from the ui to the serverside
@app.route('/add_products',methods=['GET','POST'])
def add_products():
    # checking method
    if request.method=='POST':
         # get form input
        pname = request.form['product_name']
        bp=request.form['buying_price']
        sp=request.form['selling_price']
        new_product=(pname,bp,sp)
        # insert to the database
        insert_products(new_product)
    return redirect(url_for('products'))

# create a python function that receives data from the ui to the serverside
@app.route('/add_sales',methods=['GET','POST'])
def add_sales():
    # checking method
    if request.method=='POST':
         # get form input
        pid = request.form['product_id']
        qty=request.form['quantity']
      
        new_sale=(pid,qty)
        # insert to the database
        insert_sales(new_sale)
    return redirect(url_for('sales'))

# create a python function that receives data from the ui to the serverside
@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    # checking method
    if request.method=='POST':
         # get form input
        pid = request.form['product_id']
        stq=request.form['stock_quantity']
      
        new_stock=(pid,stq)
        # insert to the database
        insert_stock(new_stock)
    return redirect(url_for('stock'))
app.run(debug=True)


