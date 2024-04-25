from flask import Flask, render_template,  request, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/")
def display():
    return render_template('shop.html')

def get_item_info_from_db(image_id):
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    # Assuming 'image_id' is the name of the item
    cursor.execute('SELECT description, hp_buff, atk_buff, def_buff, duration, cooldown, price FROM shop_items WHERE name = ?', (image_id,))

    item = cursor.fetchone()
    conn.close()
    return item
@app.route('/get_item_info', methods=['GET'])
def get_item_info():
    print("hola")
    image_id = request.args.get('image_id')  # Assuming image ID is passed as a query parameter
    if image_id is None:
        return jsonify({'error': 'Image ID not provided'}), 400

    print(image_id)
    item = get_item_info_from_db(image_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    print("name")
    # Assuming the database schema matches the returned columns
    description, hp_buff, atk_buff, def_buff, duration, cooldown, price = item
    print(description)

    # Return item information as JSON response
    return jsonify({
        # 'name': name,
        'description': description,
        'hp_buff': hp_buff,
        'atk_buff': atk_buff,
        'def_buff': def_buff,
        'duration': duration,
        'cooldown': cooldown,
        'price': price
    })

if __name__ == "__main__":
    app.run(debug=True)