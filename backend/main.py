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

engine = create_engine((os.environ['SQLALCHEMY_CONFIG']))

@app.route('/')
def index():
    try:
        return render_template('index.html', message='Connected to Flask server')
    except Exception as e:
        return f"Flask server connection error: {e}"

def get_query():
    return text("SELECT * FROM sql_inventory.products;")

def post_query(data):
    return text(f"INSERT INTO sql_inventory.products (ProductName, Quantity, PurchasePrice, VAT, Margin) VALUES (:name, :quantity, :price, :vat, :margin);").bindparams(
        name=data['name'], quantity=data['quantity'], price=data['price'], vat=data['vat'], margin=data['margin']
    )

def put_query(data):
    return text(f"UPDATE sql_inventory.products SET ProductName = :new_name WHERE ProductName = :old_name").bindparams(
        new_name=data['new_name'], old_name=data['old_name']
    )

def delete_query(data):
    return text(f"DELETE FROM sql_inventory.products WHERE ProductID = :id").bindparams(id=data['id'])

@app.route('/api/products', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_products():
    try:
        connection = engine.connect()

        if request.method == 'GET':
            query = get_query()
            result = connection.execute(query)
            columns = list(result.keys())
            rows = [list(row) for row in result]
            response = {'columns': columns, 'data': rows}

        elif request.method == 'POST':
            newValue = request.json 
            query = post_query(newValue)
            connection.execute(query)
            response = {'message': 'Product added successfully', 'data': newValue}

        elif request.method == 'PUT':
            updateValue = request.json
            query = put_query(updateValue)
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
        return jsonify({'API handling error': str(e)}), 500 
    
# @app.route('/api/customers')
# def get_customers():
#     try:
#         connection = engine.connect()
#         query = text("SELECT * FROM sql_store.customers LIMIT 5")
#         result = connection.execute(query)

#         columns = list(result.keys())
#         rows = [list(row) for row in result]

#         connection.close()

#         response = {'columns': columns, 'data': rows}

#         return jsonify(response)
    
#     except Exception as e:
#         return jsonify({'API handling error': str(e)}), 500
    
    
# @app.route('/api/orders')
# def get_orders():
#     try:
#         with engine.connect() as connection:
#             query = text("SELECT * FROM sql_store.orders LIMIT 5")
#             result = connection.execute(query)

#             columns = list(result.keys())
#             rows = [list(row) for row in result]

#             response = {'columns': columns, 'data': rows}

#         return jsonify(response)
    
#     except Exception as e:
#         return jsonify({'API handling error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)