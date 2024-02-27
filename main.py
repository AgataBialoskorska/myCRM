from flask import Flask, render_template
from sqlalchemy import create_engine, text
import os

app = Flask(__name__)

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
database_name = os.getenv('DB_NAME')
database_uri = os.getenv('DB_URI')

engine = create_engine(f'mysql+pymysql://{username}:{password}@{database_uri}/{database_name}')
@app.route('/')

def index():
    try:
        connection = engine.connect()
        
        query = text("SELECT * FROM test.products LIMIT 3")
        result = connection.execute(query)
        rows = [row for row in result]

        connection.close()

        return render_template('index.html', rows=rows)

    except Exception as e:
        return f"Błąd: {e}"

if __name__ == '__main__':
    app.run(debug=True)