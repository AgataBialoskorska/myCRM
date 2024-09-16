from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)
CORS(app)
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
database_name = os.getenv('DB_NAME')
database_uri = os.getenv('DB_URI')
products = []

engine = create_engine(f'mysql+pymysql://{username}:{password}@{database_uri}/{database_name}')

@app.route('/')
def index():
    try:
        return render_template('index.html', message='Connected to Flask server')
    except Exception as e:
        return f"Flask server connection error: {e}"

def get_query():
    return text("SELECT * FROM sql_inventory.products;")

def post_query(data):
    insertQuery = text(f"INSERT INTO sql_inventory.products (ProductName, Quantity, PurchasePrice, VAT, Margin) VALUES (:name, :quantity, :price, :vat, :margin);").bindparams(
        name=data['name'], quantity=data['quantity'], price=data['price'], vat=data['vat'], margin=data['margin']
    )
    print(insertQuery)
    return insertQuery

def put_query(data):
    query = "UPDATE sql_inventory.products SET "
    params = {}
    
    if 'name' in data and data['name']:
        query += "ProductName = :name, "
        params['name'] = data['name']
    if 'quantity' in data and data['quantity']:
        query += "Quantity = :quantity, "
        params['quantity'] = data['quantity']
    if 'price' in data and data['price']:
        query += "PurchasePrice = :price, "
        params['price'] = data['price']
    if 'vat' in data and data['vat']:
        query += "Vat = :vat, "
        params['vat'] = data['vat']
    if 'margin' in data and data['margin']:
        query += "Margin = :margin, "
        params['margin'] = data['margin']

    query = query.rstrip(', ')
    
    query += " WHERE ProductID = :id"
    params['id'] = data['id']

    buildQuery = text(query).bindparams(**params)
    
    print("Generated query:", query)
    print("With params:", params)    
    return buildQuery

def delete_query(data):
    return text(f"DELETE FROM sql_inventory.products WHERE ProductID = :id").bindparams(id=data['id'])

@app.route('/api/products', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_products():
    try:
        connection = engine.connect()

        if request.method == 'GET':
            query = get_query()
            print("query")
            result = connection.execute(query)
            columns = list(result.keys())
            rows = [list(row) for row in result]
            response = {'columns': columns, 'data': rows}

        elif request.method == 'POST':
            newValue = request.json 
            query = post_query(newValue)
            print("query")
            connection.execute(query)
            response = {'message': 'Product added successfully', 'data': newValue}

        elif request.method == 'PUT':
            updateValue = request.json
            query = put_query(updateValue)
            print("query")
            connection.execute(query)
            response = {'message': 'Product updated successfully'}

        elif request.method == 'DELETE':
            deleteValue = request.json
            query = delete_query(deleteValue)
            connection.execute(query)
            response = {'message': 'Product deleted successfully'}

        connection.commit()
        connection.close()

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'Error: handle_products()': str(e)}), 500 
    
if __name__ == '__main__':
    app.run(debug=True)