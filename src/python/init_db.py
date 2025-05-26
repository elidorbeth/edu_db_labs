import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Ініціалізація Flask та SQLAlchemy
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_file = os.path.join(BASE_DIR, 'formsys.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_EXPIRE_ON_COMMIT'] = False

db = SQLAlchemy(app)

# ініціалізація бази
def init_db():
    sql_path = os.path.join(BASE_DIR, 'sql', 'lab6.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        script = f.read()
    conn = db.engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
        print("Ініціалізація бази завершена")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    with app.app_context():
        init_db()
