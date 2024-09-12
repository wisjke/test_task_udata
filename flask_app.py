from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load product data from JSON file
with open('menu_items.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Root endpoint to display a welcome message
@app.route('/')
def index():
    return "Use /all_products to see all products."

# Endpoint to return all products
@app.route('/all_products/', methods=['GET'])
def get_all_products():
    return jsonify(products)

# Endpoint to return information about a specific product by name
@app.route('/products/<string:product_name>', methods=['GET'])
def get_product(product_name):
    product = next((prod for prod in products if prod['name'].lower() == product_name.lower()), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint to return specific field of a specific product
@app.route('/products/<string:product_name>/<string:product_field>', methods=['GET'])
def get_product_field(product_name, product_field):
    product = next((prod for prod in products if prod['name'].lower() == product_name.lower()), None)
    if product:
        field_value = product.get(product_field)
        if field_value:
            return jsonify({product_field: field_value})
        else:
            return jsonify({"error": f"Field '{product_field}' not found in product '{product_name}'"}), 404
    else:
        return jsonify({"error": "Product not found"}), 404

# Handle favicon request
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return an empty response with a 204 No Content status

if __name__ == '__main__':
    app.run(debug=True)
