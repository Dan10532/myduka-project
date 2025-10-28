from flask import Flask,render_template,request,redirect,url_for
from database import fetch_data,insert_products

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

    return render_template('my_sales.html',my_sale=sales)
# stock route
@app.route('/stock')
def stock():
    stock=fetch_data('stock')

    return render_template('my_stock.html',my_stock=stock)

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
app.run(debug=True)


