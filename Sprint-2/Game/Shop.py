from flask import Flask, render_template,  request, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/")
def display():
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    username = "tester_login"
    # Assuming 'image_id' is the name of the item
    cursor.execute(
        'SELECT player_currency FROM logins WHERE username = ?',
        (username,))
    result = cursor.fetchone()
    player_currency = result[0]
    conn.close()
    return render_template('shop.html',currency=player_currency)

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

@app.route('/update_currency', methods=['POST'])
def updateData():
    try:
        # Extract JSON data from request
        req_data = request.get_json()
        if req_data and 'currency' in req_data:
            currency_value = req_data['currency']
            conn = sqlite3.connect('user_info.db')
            cursor = conn.cursor()
            username = "tester_login"
            # Assuming 'image_id' is the name of the item
            cursor.execute(
                'UPDATE logins SET player_currency = ? WHERE username = ?',
                (currency_value,username,))
            conn.close()

            image_id = req_data['item']
            print("image_id")
            conn = sqlite3.connect('user_info.db')
            cursor = conn.cursor()
            query = 'SELECT * FROM user_inventory WHERE user = ? AND item_name = ?'
            cursor.execute(query, (username,image_id))
            result = cursor.fetchone()  # Fetch one row (if exists)

            if result is None:
                cursor.execute('INSERT INTO user_inventory VALUES (?, ?, ?)',
                               (username, image_id, 1))
                conn.commit()
                print("not in db")
            else:
                item = conn.execute('SELECT * FROM user_inventory WHERE user = ? AND item_name = ?',
                                    (username, image_id)).fetchall()
                print("newAmount")
                newAmount = item[0][2] + 1
                cursor.execute('UPDATE user_inventory SET quantity = ? WHERE user = ? AND item_name = ?',
                             (newAmount, username, image_id))
                conn.commit()
                print("in db")
            conn.close()
            return jsonify({'success': True, 'currency': currency_value}), 200
        else:
            raise ValueError('Invalid JSON data')
    except Exception as e:
        error_msg = str(e)
        print('Error:', error_msg)
        return jsonify({'error': error_msg}), 400  # Bad Request
    # if ((drop not in currentPlayer['inventory'])):
    #     conn2.execute('INSERT INTO user_inventory VALUES (?, ?, ?)',
    #                   (currentPlayer['username'], drop, enemy['drops'][drop]))
    #     conn2.commit()
    # elif ((drop in currentPlayer['inventory'])):
    #     item = conn2.execute('SELECT * FROM user_inventory WHERE user = ? AND item_name = ?',
    #                          (currentPlayer['username'], drop)).fetchall()
    #     newAmount = item[0][2] + enemy['drops'][drop]
    #     conn2.execute('UPDATE user_inventory SET quantity = ? WHERE user = ? AND item_name = ?',
    #                   (newAmount, currentPlayer['username'], drop))
    #     conn2.commit()

if __name__ == "__main__":
    app.run(debug=True)