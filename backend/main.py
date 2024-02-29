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
    

@app.route('/api/data')
def get_data():
    try:
        connection = engine.connect()
        query = text("SELECT * FROM test.products LIMIT 3")
        result = connection.execute(query)

        columns = list(result.keys())
        rows = [list(row) for row in result]

        connection.close()

        response = {'columns': columns, 'data': rows}

        return jsonify(response)
    
    except Exception as e:
        return jsonify({'API handling error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)