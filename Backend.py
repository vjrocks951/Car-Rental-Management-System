# Car Rental Management System — Backend (Flask, Folder Structure)
# Tech: Python, Flask, SQLAlchemy (SQL DB), PyMongo (MongoDB)

# =====================================================
# 📁 Project Structure
# =====================================================
# backend/
# ├── run.py
# ├── config.py
# ├── requirements.txt
# ├── app/
# │   ├── __init__.py
# │   ├── extensions.py
# │   ├── models/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   ├── car.py
# │   │   └── booking.py
# │   ├── routes/
# │   │   ├── __init__.py
# │   │   ├── auth_routes.py
# │   │   ├── car_routes.py
# │   │   ├── booking_routes.py
# │   │   └── admin_routes.py
# │   ├── services/
# │   │   ├── __init__.py
# │   │   ├── pricing_service.py
# │   │   └── log_service.py
# │   └── utils/
# │       ├── __init__.py
# │       └── helpers.py
# └── .env


# =====================================================
# 📄 requirements.txt
# =====================================================
# flask
# flask_sqlalchemy
# flask_bcrypt
# flask_cors
# pymongo
# python-dotenv


# =====================================================
# 📄 config.py
# =====================================================
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///car_rental.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGO_URI = "mongodb://localhost:27017/"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")


# =====================================================
# 📄 run.py  (Entry Point)
# =====================================================
from app import create_app
from app.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# =====================================================
# 📁 app/__init__.py  (App Factory)
# =====================================================
from flask import Flask
from flask_cors import CORS
from .extensions import db, bcrypt, mongo
from config import Config
from .routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mongo.init_app(app)

    register_blueprints(app)
    return app


# =====================================================
# 📁 app/extensions.py  (All Extensions Here)
# =====================================================
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from pymongo import MongoClient


db = SQLAlchemy()
bcrypt = Bcrypt()

class Mongo:
    def __init__(self):
        self.client = None
        self.db = None
        self.car_meta = None
        self.logs = None

    def init_app(self, app):
        self.client = MongoClient(app.config['MONGO_URI'])
        self.db = self.client["car_rental_mongo"]
        self.car_meta = self.db["car_metadata"]
        self.logs = self.db["activity_logs"]

mongo = Mongo()


# =====================================================
# 📁 app/models/user.py
# =====================================================
from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# =====================================================
# 📁 app/models/car.py
# =====================================================
from app.extensions import db

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    price_per_day = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)


# =====================================================
# 📁 app/models/booking.py
# =====================================================
from datetime import datetime
from app.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50), default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# =====================================================
# 📁 app/models/__init__.py
# =====================================================
from .user import User
from .car import Car
from .booking import Booking


# =====================================================
# 📁 app/services/pricing_service.py
# =====================================================
def calculate_price(price_per_day, start_date, end_date):
    days = (end_date - start_date).days + 1
    return days * price_per_day


# =====================================================
# 📁 app/services/log_service.py
# =====================================================
from datetime import datetime
from app.extensions import mongo


def log_activity(action, data):
    mongo.logs.insert_one({
        "action": action,
        "data": data,
        "timestamp": datetime.utcnow()
    })


# =====================================================
# 📁 app/utils/helpers.py
# =====================================================
from datetime import datetime


def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()


# =====================================================
# 📁 app/routes/__init__.py
# =====================================================
from .auth_routes import auth_bp
from .car_routes import car_bp
from .booking_routes import booking_bp
from .admin_routes import admin_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(car_bp, url_prefix='/api')
    app.register_blueprint(booking_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')


# =====================================================
# 📁 app/routes/auth_routes.py
# =====================================================
from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models import User
from app.services.log_service import log_activity

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(name=data['name'], email=data['email'], password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    log_activity('REGISTER', {'email': data['email']})
    return jsonify({'message': 'User registered'})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        log_activity('LOGIN', {'user_id': user.id})
        return jsonify({'message': 'Login successful', 'user_id': user.id})

    return jsonify({'error': 'Invalid credentials'}), 401


# =====================================================
# 📁 app/routes/car_routes.py
# =====================================================
from flask import Blueprint, request, jsonify
from app.extensions import db, mongo
from app.models import Car
from app.services.log_service import log_activity

car_bp = Blueprint('cars', __name__)


@car_bp.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify([
        {
            'id': c.id,
            'brand': c.brand,
            'model': c.model,
            'category': c.category,
            'price_per_day': c.price_per_day,
            'is_available': c.is_available
        } for c in cars
    ])


@car_bp.route('/cars', methods=['POST'])
def add_car():
    data = request.json

    car = Car(
        brand=data['brand'],
        model=data['model'],
        category=data.get('category'),
        price_per_day=data['price_per_day']
    )
    db.session.add(car)
    db.session.commit()

    mongo.car_meta.insert_one({
        'car_id': car.id,
        'color': data.get('color'),
        'fuel_type': data.get('fuel_type'),
        'transmission': data.get('transmission'),
        'features': data.get('features', [])
    })

    log_activity('ADD_CAR', {'car_id': car.id})
    return jsonify({'message': 'Car added'})


# =====================================================
# 📁 app/routes/booking_routes.py
# =====================================================
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Car, Booking
from app.services.pricing_service import calculate_price
from app.services.log_service import log_activity
from app.utils.helpers import parse_date

booking_bp = Blueprint('booking', __name__)


@booking_bp.route('/book', methods=['POST'])
def book_car():
    data = request.json
    car = Car.query.get(data['car_id'])

    if not car or not car.is_available:
        return jsonify({'error': 'Car not available'}), 400

    start_date = parse_date(data['start_date'])
    end_date = parse_date(data['end_date'])
    total_price = calculate_price(car.price_per_day, start_date, end_date)

    booking = Booking(
        user_id=data['user_id'],
        car_id=car.id,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price
    )

    car.is_available = False
    db.session.add(booking)
    db.session.commit()

    log_activity('BOOK_CAR', {'booking_id': booking.id})
    return jsonify({'message': 'Booking confirmed', 'total_price': total_price})


# =====================================================
# 📁 app/routes/admin_routes.py
# =====================================================
from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Car, Booking
from app.services.log_service import log_activity

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/bookings', methods=['GET'])
def all_bookings():
    bookings = Booking.query.all()
    return jsonify([
        {
            'booking_id': b.id,
            'user_id': b.user_id,
            'car_id': b.car_id,
            'start_date': str(b.start_date),
            'end_date': str(b.end_date),
            'total_price': b.total_price,
            'status': b.status
        } for b in bookings
    ])


@admin_bp.route('/car/<int:car_id>/return', methods=['PUT'])
def return_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({'error': 'Car not found'}), 404

    car.is_available = True
    db.session.commit()

    log_activity('RETURN_CAR', {'car_id': car_id})
    return jsonify({'message': 'Car marked available'})
