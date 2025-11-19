from flask import Flask, render_template, request, redirect, url_for, flash, session,send_file
from flask_bcrypt import Bcrypt
from database import (
    fetch_data, insert_products, insert_sales, insert_stock,
    product_profit, sales_products, profit_day, sales_day,
    insert_users, check_email, update_product as db_update_product,
    delete_product as db_delete_product, update_stock as db_update_stock, delete_stock as db_delete_stock,
    update_sale as db_update_sale, delete_sale as db_delete_sale

)

from io import BytesIO
import pandas as pd 

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'Mdan10532'

# -------------------------------
# HOME
# -------------------------------


@app.route('/')
def home_page():
    return render_template('index.html')

# -------------------------------
# PRODUCTS
# -------------------------------


@app.route('/products')
@login_required
def products():
    prods = fetch_data('products')
    return render_template('myproducts.html', my_prod=prods)


@app.route('/add_products', methods=['POST'])
def add_products():
    pname = request.form['product_name']
    bp = request.form['buying_price']
    sp = request.form['selling_price']
    insert_products((pname, bp, sp))
    flash('Product added successfully!', 'success')
    return redirect(url_for('products'))


@app.route('/update_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    pname = request.form['product_name']
    bp = request.form['buying_price']
    sp = request.form['selling_price']
    db_update_product(product_id, pname, bp, sp)
    flash('Product updated successfully!', 'success')
    return redirect(url_for('products'))


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    db_delete_product(product_id)
    flash('Product deleted successfully!', 'danger')
    return redirect(url_for('products'))

# SALES
@app.route('/sales')
@login_required
def sales():
    sales_data = fetch_data('sales')
    products = fetch_data('products')
    return render_template('my_sales.html', my_sale=sales_data, products=products)


@app.route('/add_sales', methods=['POST'])
def add_sales():
    pid = request.form['product_id']
    qty = request.form['quantity']
    insert_sales((pid, qty))
    flash('Sale added successfully!', 'success')
    return redirect(url_for('sales'))


@app.route('/update_sale/<int:sale_id>', methods=['POST'])
def update_sales(sale_id):
    pid = request.form['product_id']
    qty = request.form['quantity']
    db_update_sale(sale_id, pid, qty)
    flash('Sale updated successfully!', 'success')
    return redirect(url_for('sales'))


@app.route('/delete_sale/<int:sale_id>', methods=['POST'])
def remove_sale(sale_id):
    db_delete_sale(sale_id)
    flash('Sale deleted successfully!', 'danger')
    return redirect(url_for('sales'))
                    
# STOCK

@app.route('/stock')
@login_required
def stock():
    stock_data = fetch_data('stock')
    products = fetch_data('products')
    return render_template('my_stock.html', my_stock=stock_data, products=products)


@app.route('/add_stock', methods=['POST'])
def add_stock():
    pid = request.form['product_id']
    stq = request.form['stock_quantity']
    insert_stock((pid, stq))
    flash('Stock added successfully!', 'success')
    return redirect(url_for('stock'))


@app.route('/update_stock/<int:stock_id>', methods=['POST'])

def update_stock(stock_id):
    pid = request.form['product_id']
    qty = request.form['stock_quantity']
    db_update_stock(stock_id, pid, qty)
    flash('Stock updated successfully!', 'success')
    return redirect(url_for('stock'))


@app.route('/delete_stock/<int:stock_id>', methods=['POST'])
def remove_stock(stock_id):
    db_delete_stock(stock_id)
    flash('Stock deleted successfully!', 'danger')
    return redirect(url_for('stock'))

# -------------------------------
# DASHBOARD
# -------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    profit = product_profit()       # Returns list of (id, name, profit)
    sales = sales_products()        # Returns list of (id, name, total_sales)
    profitperday = profit_day()     # Returns list of (date, profit)
    salesperday = sales_day()       # Returns list of (date, total_sales)

    # Prepare chart data
    product_names = [i[1] for i in profit]
    product_profits = [float(i[2]) for i in profit]
    sales_product = [float(i[2]) for i in sales]
    profitday = [float(i[1]) for i in profitperday]
    salesday = [float(i[1]) for i in salesperday]
    dates = [str(i[0]) for i in salesperday]

    # Calculate stats
    total_sales = sum([float(i[2]) for i in sales])
    total_profit = sum([float(i[2]) for i in profit])
    daily_sales = sum([float(i[1]) for i in salesperday[-1:]])  # last day
    daily_profit = sum([float(i[1]) for i in profitperday[-1:]])  # last day

    return render_template(
        'dashboard.html',
        product_names=product_names,
        product_profits=product_profits,
        sales_product=sales_product,
        profitday=profitday,
        salesday=salesday,
        dates=dates,
        total_sales=total_sales,
        total_profit=total_profit,
        daily_sales=daily_sales,
        daily_profit=daily_profit
    )


# -------------------------------
# USER AUTH
# -------------------------------


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fullname']
        email = request.form['email']
        pnumber = request.form['phone']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        new_user = (fname, email, pnumber, hashed_password)
        check = check_email(email)

        if check is None:
            insert_users(new_user)
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User already exists. Try another email or login.', 'warning')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        check = check_email(email)  # should return user tuple or None

        if check is None:
            flash('User does not exist! Please register.', 'danger')
            return redirect(url_for('register'))

        # check password
        stored_password = check[4]  # make sure index 4 is the password hash
        if bcrypt.check_password_hash(stored_password, password):
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect email or password!', 'danger')
            return redirect(url_for('login'))  # ✅ redirect instead of render_template

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/export_sales')
@login_required
def export_sales():
    sales_data = fetch_data('sales')  # [(id, product_id, quantity, created_at), ...]
    products = {prod[0]: {'name': prod[1], 'selling_price': float(prod[3])} for prod in fetch_data('products')}

    df = pd.DataFrame(sales_data, columns=['ID', 'Product ID', 'Quantity', 'Date'])
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')  # format for Excel
    df['Product Name'] = df['Product ID'].map(lambda x: products[x]['name'])
    df['Total Sold'] = df.apply(lambda row: row['Quantity'] * products[row['Product ID']]['selling_price'], axis=1)
    df = df[['Date', 'Product Name', 'Quantity', 'Total Sold']]

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales')
        worksheet = writer.sheets['Sales']

        # Adjust column widths
        for col_cells in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in col_cells)
            col_letter = col_cells[0].column_letter
            worksheet.column_dimensions[col_letter].width = max_length + 2

    output.seek(0)
    return send_file(
        output,
        download_name="sales_report.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )




if __name__ == '__main__':
    app.run(debug=True)
