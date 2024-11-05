from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import subprocess
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barcodes.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(10), nullable=True)
    manufacturer = db.Column(db.String(20), nullable=True)
    brand = db.Column(db.String(20), nullable=True)
    timestamp = db.Column(db.String(20), nullable=True)

with app.app_context():
    db.create_all()

def run_command_with_output_after(command: str) -> subprocess.CompletedProcess[str] | subprocess.CalledProcessError:
    """

    :param command:
    :return:
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as e:
        return e

def make_api_call(barcode: str):
    """

    :param barcode:
    """
    # todo this section is for ean-search.org
    # apiToken = "584c14adf603758ea9d11b4d7f4db7012d8b659a"
    # t = json.loads(run_command_with_output_after(f'curl '
    #     f'"https://api.ean-search.org/api?token={apiToken}&op=barcode-lookup&'
    #     f'format=json&ean={barcode}"').stdout)

    t = json.loads(run_command_with_output_after(f'curl '
        f'"https://api.barcodelookup.com/v3/products?barcode={barcode}&formatted=y&key=9ozsxx49ntgcezx81ze2dy83z12w43"').stdout)

    # Extract relevant data and save to the database
    product_data = t['products'][0]

    new_product = Product(
        barcode=barcode,
        title=product_data['title'],
        category=product_data['category'],
        manufacturer=product_data['manufacturer'],
        brand=product_data['brand'],
        timestamp=datetime.now().strftime("%d/%m/%y %H:%M")
    )
    db.session.add(new_product)
    db.session.commit()

    print("Data saved to database.")
    print(json.dumps(t, indent=3))

@app.route('/submit', methods=['GET'])
def submit():
    """

    :return:
    """
    data = request.args.get('data')
    if data:
        make_api_call(data)
        return "Product data found and stored in database", 200
    else:
        return "No data received", 400


@app.route('/')
def get_all_products():
    # Query all products
    products = Product.query.all()

    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
