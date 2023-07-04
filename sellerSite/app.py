from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'doa'


def create_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='d240601k',
        database='software'
    )
    return connection

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        seller_password = request.form.get('Seller_Password')
        seller_id = request.form.get('Seller_ID')

        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM login WHERE Seller_Password = %s AND Seller_ID = %s",
                       (seller_password, seller_id))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            print('User authenticated successfully:', user)
            return redirect(url_for('index'))  # Redirect to index.html page
        else:
            flash('Invalid credentials. Please try again.', 'error')  # Show an error message
            print('Invalid credentials')
            
    return render_template('login.html')

@app.route('/orders')
def get_orders():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(orders)

@app.route('/order.html')
def order():
    return render_template('order.html')



@app.route('/completed_order')
def get_completed_order():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT order_id, order_date, total_price, customer_id, payment_method FROM orders ORDER BY order_date ASC LIMIT 1")
    completed_order = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(completed_order)

@app.route('/recent_order')
def get_recent_order():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT order_date, order_id, customer_id FROM orders ORDER BY order_date DESC LIMIT 1")
    recent_order = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(recent_order)

@app.route('/low_stock')
def get_low_stock():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT product_id, category, availability FROM product ORDER BY availability ASC LIMIT 1")
    low_stock = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(low_stock)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/category.html', methods=['GET', 'POST'])
def category():
    if request.method == 'POST':
        # Retrieve the category data from the request
        category_id = request.form['category_id']
        category_type = request.form['category_type']

        # Insert the new category into the database
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO categories (category_id, categoryType) VALUES (%s, %s)"
        cursor.execute(insert_query, (category_id, category_type))
        connection.commit()
        cursor.close()
        connection.close()

    # Fetch all the categories from the database
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT category_id, categoryType FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('category.html', categories=categories)





@app.route('/account.html')
def account():
    return render_template('account.html')


@app.route('/product.html', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        # Get the form data
        product_id = request.form['pID']
        name = request.form['pname']
        price = request.form['price']
        quantity = request.form['quan']
        description = request.form['ldesc']
        category = request.form['sdesc']

        # Insert the new product into the database
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO product (product_id, name, price, availability, category, description) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (product_id, name, price, quantity, category, description))
        connection.commit()
        cursor.close()
        connection.close()
        
       

    # Fetch all the products from the database
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT product_id, name, price, availability, category, description FROM product")
    products = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('product.html', products=products)


@app.route('/stock.html', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        # Retrieve the stock data from the request
        product_id = request.form['productID']
        quantity = request.form['quantity']
        category_type = request.form['category_type']
        category_id = request.form['category_id']

        # Insert the new stock into the database
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO Stock (Product_ID, Quantity, categoryType, category_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (product_id, quantity, category_type, category_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Redirect back to the stock route
        return redirect(url_for('stock'))

    # Fetch all the stock details from the database
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Stock_ID, Product_ID, Quantity, categoryType, category_id, Last_Update FROM Stock")
    stock = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('stock.html', stock=stock)




@app.route('/customer')
def get_customer():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customer")
    customer = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(customer)

@app.route('/users.html')
def users():
    return render_template('users.html')


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))  # Redirect to the login page


if __name__ == '__main__':
    app.run()
