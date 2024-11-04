from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barcodes.db'
db = SQLAlchemy(app)


class TestProduct(db.Model):
    __tablename__ = 'Test_Product'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    barcode = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=True, unique=True)
    category = db.Column(db.String(10), nullable=True, unique=True)
    manufacturer = db.Column(db.String(20), nullable=True, unique=True)
    brand = db.Column(db.String(20), nullable=True, unique=True)
    timestamp = db.Column(db.String(20), nullable=True, unique=True)


with app.app_context():
    db.session.query(TestProduct).delete()
    db.session.commit()

@app.route('/')
def get_all_products():
    # Query all products
    products = TestProduct.query.all()

    return render_template('index.html', products=products)

tester_products = [
    {
        'barcode': '000001',
        'title': 'Semi-Skimmed Milk',
        'category': 'Food, Dairy',
        'manufacturer': 'Waitrose',
        'brand': 'Waitrose',
    },
    {
        'barcode': '000002',
        'title': 'Whole Wheat Bread',
        'category': 'Food, Bakery',
        'manufacturer': 'Hovis',
        'brand': 'Hovis',
    },
    {
        'barcode': '000003',
        'title': 'Sparkling Water',
        'category': 'Beverage, Water',
        'manufacturer': 'Perrier',
        'brand': 'Perrier',
    },
    {
        'barcode': '000004',
        'title': 'Organic Bananas',
        'category': 'Food, Fruit',
        'manufacturer': 'Dole',
        'brand': 'Dole',
    },
    {
        'barcode': '000005',
        'title': 'Dark Chocolate 70%',
        'category': 'Food, Confectionery',
        'manufacturer': 'Lindt',
        'brand': 'Lindt',
    }
]


with app.app_context():
    db.create_all()
    for prod in tester_products:
        new_product = TestProduct(
            barcode=prod['barcode'],
            title=prod['title'],
            category=prod['category'],
            manufacturer=prod['manufacturer'],
            brand=prod['brand'],
            timestamp=datetime.now().strftime("%d/%m/%y %H:%M")
        )
        db.session.add(new_product)
    db.session.commit()

if __name__ == '__main__':
    app.run(host="172.20.10.7", port=5000, debug=True)