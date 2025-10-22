# import the psycopg2 package
import psycopg2

# connect to the postgres database
conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    database='myduka_db',
    port='5432',
    password='Mdan10532'
)
# declare a cursor to perform database operations
cur = conn.cursor()

# database operations


# def fetch_products():
#     cur.execute('select * from products;')
#     prods = cur.fetchall()
#     return prods

# products = fetch_products()
# print(products)

# # display sales on the terminal


# def fetch_sales():
#     cur.execute('select * from sales;')
#     sales = cur.fetchall()
#     return sales

# sales = fetch_sales()
# print(sales)

# # display stock on the terminal


def fetch_stock():
    cur.execute('select * from stock;')
    stock = cur.fetchall()
    return stock


# stock = fetch_stock()  
# print(stock)

# fetch data in the database
def fetch_data(table):
    cur.execute(f'select * from {table};')
    data=cur.fetchall()
    return data

stock=fetch_data('stock')
print(stock)
# products=fetch_data('products')
# print(products)
# sales=fetch_data('sales')
# print(sales)

# insert stock
def insert_stock(values):
    query='insert into stock(pid,stock_quantity,created_at)values(%s,%s,now());'
    cur.execute(query,values)
    conn.commit()

new_stock=(3,40)
insert_stock(new_stock)
stock = fetch_stock()  
print(stock)

# insert sales
def insert_sales(values):
    query='insert into sales(pid,quantity,created_at)values(%s,%s,now());'
    cur.execute(query,values)
    conn.commit()

new_sale=(2,30)
insert_sales(new_sale)
sales = fetch_data('sales')  
print(sales)

# insert products
def insert_products(values):
    query='insert into products(name,buying_price,selling_price)values(%s,%s,%s);'
    cur.execute(query,values)
    conn.commit()

new_product=('banana',20,40)
insert_products(new_product)
products=fetch_data('products')
print(products)
# write query to get profit per product and also sales per product on myduka_db
# write the following queries
# 1.profit per product
# 2.sales per product 


# def fetch_profit():
# #     cur.execute('select product_id,product_name,sum((selling_price - cost_price) * quantity_sold) as total_profit FROM sales GROUP BY product_id, product_name ORDER BY total_profit DESC;
# #  ')
#     profit=cur.fetchall()
#     return(profit)

# profit=fetch_profit()

def product_profit():
    query='SELECT p.id,p.name,SUM((p.selling_price - p.buying_price) * s.quantity) AS total_profit FROM products as p join sales as s on p.id=s.pid group by p.name,p.id;'
    cur.execute(query)
    profit=cur.fetchall()
    return profit

my_profit=product_profit()
print('profit')
print(my_profit)

# write a function that gets sales per product
def sales_product():
    query='SELECT p.id,p.name,SUM(s.quantity * p.selling_price) AS total_sale FROM sales AS s JOIN products AS p ON s.pid = p.id GROUP BY p.id, p.name;'
    cur.execute(query)
    sales=cur.fetchall()
    return sales

my_sales=sales_product()
print('sales')
print(my_sales)

