from flask import Flask, request, jsonify
from decimal import Decimal

app = Flask(__name__)

# Sample in-memory product list
products = [
    {'id': 1, 'name': 'Apple', 'price': Decimal('10'), 'units': 'units', 'taken': 0, 'payable': Decimal('0.0')},
    {'id': 2, 'name': 'Banana', 'price': Decimal('20'), 'units': 'units', 'taken': 0, 'payable': Decimal('0.0')},
   {'id': 3, 'name': 'Potato', 'price': Decimal('20'), 'units': 'units', 'taken': 0, 'payable': Decimal('0.0')},

]

# Helper function to find a product by ID
def find_product(product_id):
    return next((product for product in products if product['id'] == product_id), None)

# Route to get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': products})

# Route to get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = find_product(product_id)
    if product:
        return jsonify({'product': product})
    return jsonify({'message': 'Product not found'}), 404

# Route to create a new product
@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        data = request.form.to_dict()

        # Input validation
        if not all(key in data for key in ('name', 'price', 'unit', 'taken', 'payable')):
            return jsonify({'message': 'Missing required fields'}), 400

        try:
            new_product = {
                'id': len(products) + 1,
                'name': data['name'],
                'price': Decimal(str(data['price'])),
                'unit': data['unit'],
                'taken': int(data['taken']),
                'payable': Decimal(str(data['payable'])),
            }
            products.append(new_product)
            return jsonify({'message': 'Product created successfully', 'product': new_product}), 201
        except ValueError:
            return jsonify({'message': 'Invalid price or payable format'}), 400
    else:
        return render_template('add.html')

# Route to update a product by ID
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = find_product(product_id)
    if product:
        data = request.get_json()
        product.update(data)
        return jsonify({'message': 'Product updated successfully', 'product': product})
    return jsonify({'message': 'Product not found'}), 404

# Route to delete a product by ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [product for product in products if product['id'] != product_id]
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
