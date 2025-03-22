from flask import Flask
from config import configure_app
from models import db  

app = Flask(__name__)

configure_app(app)

db.init_app(app)

import routes

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)