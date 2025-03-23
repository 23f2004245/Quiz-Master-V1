from flask import Flask
import config
from routes import main
from models import db, User
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

config.configure_app(app)

db.init_app(app)

app.register_blueprint(main)

with app.app_context():
    db.create_all()  
    admin = User.query.filter_by(is_admin=True).first()
    
    if not admin:
        password_hash = generate_password_hash('admin')
        admin = User(
            username='admin', 
            password=password_hash, 
            fullname='Admin', 
            qualification='Administrator',  
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
