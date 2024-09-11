from flask import Flask, render_template, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)
CORS(app)
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
database_name = os.getenv('DB_NAME')
database_uri = os.getenv('DB_URI')

engine = create_engine(f'mysql+pymysql://{username}:{password}@{database_uri}/{database_name}')

@app.route('/')
def index():
    try:
        return render_template('index.html', message='Connected to Flask server')
    except Exception as e:
        return f"Flask server connection error: {e}"
    
def select():
        return text("SELECT * FROM sql_inventory.products;")
def update():
        return text("UPDATE sql_inventory.products SET ProductName = 'Butter 300g' WHERE ProductName = 'Butter 100g';")
def delete():
        return text("DELETE FROM sql_inventory.products WHERE ProductName = 'Peanuts 500g';")
def insert():
        return text("INSERT INTO sql_inventory.products (ProductName, Quantity, PurchasePrice, VAT, Margin ) VALUES ('Peanuts 500g',100, 12.65,  '5%', 0.12);")

    
@app.route('/api/products')
def get_products():
    try:
        connection = engine.connect()
        # query = insert()
        querySelect = select()
        # result = connection.execute(query)
        result = connection.execute(querySelect)

        columns = list(result.keys())
        rows = [list(row) for row in result]

        connection.commit()
        connection.close()

        response = {'columns': columns, 'data': rows}

        return jsonify(response)
    
    except Exception as e:
        return jsonify({'API handling error': str(e)}), 500
    
    
@app.route('/api/customers')
def get_customers():
    try:
        connection = engine.connect()
        query = text("SELECT * FROM sql_store.customers LIMIT 5")
        result = connection.execute(query)

        columns = list(result.keys())
        rows = [list(row) for row in result]

        connection.close()

        response = {'columns': columns, 'data': rows}

        return jsonify(response)
    
    except Exception as e:
        return jsonify({'API handling error': str(e)}), 500
    
    
@app.route('/api/orders')
def get_orders():
    try:
        with engine.connect() as connection:
            query = text("SELECT * FROM sql_store.orders LIMIT 5")
            result = connection.execute(query)

            columns = list(result.keys())
            rows = [list(row) for row in result]

            response = {'columns': columns, 'data': rows}

        return jsonify(response)
    
    except Exception as e:
        return jsonify({'API handling error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)