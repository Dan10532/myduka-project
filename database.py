# database.py
import psycopg2

# connect to the postgres database
conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    database='myduka_db',
    port='5432',
    password='Mdan10532'
)
cur = conn.cursor()

# -------------------------------
# FETCH DATA
# -------------------------------
def fetch_data(table):
    cur.execute(f'SELECT * FROM {table};')
    return cur.fetchall()

def fetch_stock():
    cur.execute('SELECT * FROM stock;')
    return cur.fetchall()

# -------------------------------
# INSERT FUNCTIONS
# -------------------------------
def insert_stock(values):
    cur.execute('INSERT INTO stock(pid,stock_quantity,created_at) VALUES(%s,%s,now());', values)
    conn.commit()

def insert_sales(values):
    cur.execute('INSERT INTO sales(pid,quantity,created_at) VALUES(%s,%s,now());', values)
    conn.commit()

def insert_products(values):
    cur.execute('INSERT INTO products(name,buying_price,selling_price) VALUES(%s,%s,%s);', values)
    conn.commit()

def insert_users(values):
    cur.execute('INSERT INTO users(full_name,email,phone_number,password) VALUES(%s,%s,%s,%s);', values)
    conn.commit()

# -------------------------------
# ANALYTICS
# -------------------------------
def product_profit():
    cur.execute('''
        SELECT p.id,p.name,SUM((p.selling_price - p.buying_price) * s.quantity) AS total_profit
        FROM products AS p
        JOIN sales AS s ON p.id=s.pid
        GROUP BY p.id,p.name;
    ''')
    return cur.fetchall()

def sales_products():
    cur.execute('''
        SELECT p.id,p.name,SUM(s.quantity * p.selling_price) AS total_sale
        FROM sales AS s
        JOIN products AS p ON s.pid=p.id
        GROUP BY p.id,p.name;
    ''')
    return cur.fetchall()

def profit_day():
    cur.execute('''
        SELECT DATE(s.created_at) AS sale_date, SUM(s.quantity*(p.selling_price - p.buying_price)) AS daily_profit
        FROM sales AS s
        JOIN products AS p ON s.pid=p.id
        GROUP BY DATE(s.created_at)
        ORDER BY sale_date ASC;
    ''')
    return cur.fetchall()

def sales_day():
    cur.execute('''
        SELECT DATE(s.created_at) AS sale_date, SUM(s.quantity*p.selling_price) AS total_sales
        FROM sales AS s
        JOIN products AS p ON s.pid=p.id
        GROUP BY DATE(s.created_at)
        ORDER BY sale_date ASC;
    ''')
    return cur.fetchall()

# -------------------------------
# USER FUNCTIONS
# -------------------------------
def check_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query, (email,))
    user = cur.fetchone()  
    return user


# -------------------------------
# UPDATE / DELETE PRODUCTS
# -------------------------------
def update_product(product_id, pname, bp, sp):
    cur.execute('''
        UPDATE products
        SET name=%s, buying_price=%s, selling_price=%s
        WHERE id=%s;
    ''', (pname, bp, sp, product_id))
    conn.commit()

def delete_product(product_id):
    cur.execute('DELETE FROM products WHERE id=%s;', (product_id,))
    conn.commit()

# -------------------------------
# UPDATE / DELETE STOCK
# -------------------------------
def update_stock(stock_id, product_id, quantity):
    cur.execute('''
        UPDATE stock
        SET pid=%s, stock_quantity=%s
        WHERE id=%s;
    ''', (product_id, quantity, stock_id))
    conn.commit()

def delete_stock(stock_id):
    cur.execute('DELETE FROM stock WHERE id=%s;', (stock_id,))
    conn.commit()

# UPDATE / DELETE SALES
# -------------------------------
def update_sale(sale_id, product_id, quantity):
    cur.execute('''
        UPDATE sales
        SET pid=%s, quantity=%s
        WHERE id=%s;
    ''', (product_id, quantity, sale_id))
    conn.commit()

def delete_sale(sale_id):
    cur.execute('DELETE FROM sales WHERE id=%s;', (sale_id,))
    conn.commit()