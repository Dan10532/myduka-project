What is Flask
=>Micro web framework written in Python 
=>Micro Means its lightweight  and doesn't include everything by default 
=>Used to build web applications ,Apis ,dashboards

    Steps to use Flask
1.install flask
    pip install flask 
2.Import Flask class from flask framework
    from flask import Flask
3.create an app object which is the Instance of the class Flask with argument __name__
    app=Flask(__name__)

4.create routes
    =>What is route -> path used to connect a URL with a Python Function 
    =>always starts with a /

    How to create a route 
        @app.route('/')
        def home():
            return 'Hello world'
Routes to create:
'/'
'/products'
'/sales'
'/stock'

5.run the app
    app.run()

=>Each Function on a route should return an html file
=>In Flask All HTML files must be in a folder called templates
=>In Flask ALL css,images and javascript files must be in folder called static   
=>render_template function in flask is used to render html files
=>you must import render_template from flask before using it

            Task
1.Create index,products ,sales and stock html files inside the templates folder 
2.create folder static for css and js files
3.Render each html file to its own route

NB=>always update your github repo
    commands to update 
    1.git add .
    2.git commit -m "name of the change"
    3.git push origin branch name



    Flask Day 2
=>fetch data on main.py
1.import the fetch data function to main
2.call the function to fetch data on specific routes

=>Display data on the ui using JINJA2
=>Templating engine used to write python like code on HTML

    How to use Jinja
1.Variables are written inside double curly braces {{variable}} in HTML  and the variable must be declared on render_template function in python
2.A python operation is written inside single curly brace with percent signs e.g  {% for i in sequence %} and the operation must be closed {% endfor %}

        Task
1.Display sales and stock on the page 
2.make all html files bootstrap enabled 
3.create tables on products,sales,and stock html files with random data with columns similar to the ones on the database

        Flask Day 3(display data in tables)

=>Display the fetched data on tables
=>using JINJA2
=>We start with the products data
=>we loop the products data to html table 

Display stock,sales and products in a table
update github

        Task
1.Navbar on each html  file *
2.Create a modal with a form to add products ,stock and  sales *
3.style your project
4.make homepage appealing


    Flask Day 4
=>Navigation using Navbar
=>we write the routes on the href attribute

        Posting Data (UI=>server=>Database)
=>You can send data from form on UI to the server-side flask route which then stores it in the database 

        HTTP Methods 
1.GET ->used when fetching data from a resource 
2.POST ->used when sending data to a resource(e.g submitting a form)

    Important Notes
=>Every form input Must have a name attribute ->flask uses this to access the form data
=>In main.py ,Create route that:
    1.checks HTTP method (GET or POST)
    2.Receives form data from the UI
    3.call the insert function to add data to the database

    Request,Redirect,url_for  in Flask
    1.Request
=>used to receive data from the form(ui->server)

    2.Redirect
=>Redirect redirects the user to another url after perfoming an action
    3.url_for
=>Url_for takes the function name then redirects to the route 

NB=>ON the form element we must have Action attribute with route as the value and method attribute with post as the value 

        Flask Day 5 (Adding Sales & Stock Functionality)
Today we focus on adding Sales and Stock functionality the right way  using dynamic product data from the database.

We’ll make the sales form more interactive by fetching all available products and displaying them in a dropdown (select) list instead of manually entering product IDs.

Steps to Add Sales

1. Fetch Products for the Sales Page
Before making a sale, we need to display all products fetched from the database:
=> create a variable on render_template e.g(products = products )
python
<!-- code -->
@app.route('/sales')
def sales():
    products = fetch_data('products')
    return render_template('sales.html', products=products)
<!-- end -->
This makes all products available inside the HTML page through the products variable.

2. Create the Sales Form in Modal
=>Each form input must have a name attribute.
<!-- code -->
<label for="pid">Choose a product:</label>
<select name="pid" id="pid" class="form-control">
  {% for product in products %}
    <option value="{{ product[0] }}">{{ product[1] }}</option>
  {% endfor %}
</select>

<br>

<label for="quantity">Quantity:</label>
<input type="number" name="quantity" id="quantity" class="form-control">

<!-- end -->

3.Add the /add_sales Route
=>This route handles form submission and database insertion.

<!-- code -->
@app.route('/add_sales', methods=['POST'])
def add_sales():
    if request.method == 'POST':
        pid = request.form['pid']
        quantity = request.form['quantity']
        new_sale=(pid, quantity)
        insert_sales(new_sale)
        return redirect(url_for('sales'))
    return redirect(url_for('sales'))

<!-- end -->

        TASK
=>Do the Same for Stock
Repeat the same logic for the Stock page:
Fetch all products to display in the form.
Use a <select> for product selection.
Add a POST route to handle adding stock.
Redirect to the stock page after submission.

        Flask Day 6
=>Project Structure 
=>How to link Images,css and js  to html files
=>Datatables 

        Flask Project Structure 
A good Flask project structure helps in organizing your application for scalability and readability.

project/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── other_templates.html
│
├── main.py
└── database.py

=>static/ → Stores all your static assets like CSS, JS, and images.
=>templates/ → Contains all HTML templates rendered by Flask.
=>app.py → Your main Flask application file.
=>database.py → file perfoming database operations.

Linking Static Files

Flask uses the url_for() function to link static files inside templates.
Example:
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
DataTables
What is DataTables?

DataTables is a JavaScript library built on jQuery that enhances HTML tables with:

Pagination
Search and filtering
Sorting and styling
Steps to Implement DataTables
1.Include CSS Link

<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">


2.Include jQuery CDN (Must be Above DataTables JS)

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>


3.Include DataTables JS Link

<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

4.Initialize DataTable

<script>
          let table = new DataTable('#table');

</script>

5.Ensure the Table ID Matches

<table id="myTable" class="display">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Product A</td>
            <td>100</td>
        </tr>
    </tbody>
</table>

Do the same thing we have done on products table to sales and stock
Expected Outcome
=>By the end of Day 6, you should be able to:
1.Organize your Flask project using a clear folder structure.
2.Link images, CSS, and JavaScript files correctly.
3.Implement DataTables for enhanced table functionality.
        Task
Create a route named /dashboard in your Flask app.
Render a dashboard.html file .
have a navbar on dashboard
add dashboad navigation to each page on your application using 
