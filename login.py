import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_session import Session
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
current_user = None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/main_menu')
def main_menu():
    return render_template("mainMenu.html")
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    conn_users = sqlite3.connect('user_info.db')
    cursor_users = conn_users.cursor()

    conn_items = sqlite3.connect("items.db")
    cursor_items = conn_items.cursor()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_check')
        
        if ' ' in username or ' ' in password or ' ' in password_confirm:
            flash("Username and password must not contain spaces.", 'error')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('Passwords do not match. Try Again', category= 'error')
            return render_template('register.html')
    
        cursor_users.execute("SELECT COUNT(*) FROM logins WHERE username = ?", (username,))
        count = cursor_users.fetchone()[0]

        if count != 0:
            flash('Username already exists. Please choose a different one.', 'warning')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password.encode('utf-8'), rounds = 13)
        
        cursor_users.execute("""INSERT INTO logins (username, password, player_health, player_atk, player_def, player_currency, player_kills, player_deaths, player_waveflag)
                            VALUES (?,?,?,?,?,?,?,?,?)
                            """,(username, password_hash, 100, 1, 1, 100, 0, 0, 1))
        conn_users.commit()

        cursor_items.execute("SELECT * FROM game_items WHERE identifer = 'BM'")
        rows = cursor_items.fetchall()

        for row in rows:
            cursor_users.execute("""INSERT INTO user_moves(user, move_name)
                                 VALUES(?,?)
                                 """, (username, row[0]))
        
        conn_items.commit()
        conn_users.commit()
        conn_items.close()
        conn_users.close()

        flash('REGISTRATION COMPLETE. Please log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    conn_users = sqlite3.connect('user_info.db')
    cursor_users = conn_users.cursor()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if ' ' in username or ' ' in password:
            flash("Username and password must not contain spaces.", 'error')
            return render_template('login.html')

        cursor_users.execute("SELECT COUNT(*) FROM logins WHERE username = ?", (username,))
        count = cursor_users.fetchone()[0]
        if count == 0:
            flash('Username Not Found.', 'warning')
            return render_template('login.html')
        
        cursor_users.execute("SELECT password FROM logins WHERE username = ?", (username,))
        user_password_hash = cursor_users.fetchone()[0]

        conn_users.commit()
        conn_users.close()

        if check_password_hash(user_password_hash, password):
            flash('LOGIN SUCCESSFUL. Enjoy your adventure!', 'success')
            current_user = username
            return redirect(url_for('main_menu'))
        
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/start-new-game', methods=['POST'])
def map():
    return redirect('/leaderboard')

@app.route('/start-map', methods=['POST'])
def startMap():
    return redirect('/gameMap')

@app.route('/gameMap')
def mapRender():
    return render_template('map.html')

@app.route('/start-battle', methods=['POST'])
def battle():
    return redirect('/shop')

@app.route('/combat')
def combatRender():
    return render_template('login.html')

# @app.route('/shop')
# def shopRender():
#     return render_template('shop.html')

@app.route("/shop")
def display():
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    username = current_user
    # Assuming 'image_id' is the name of the item
    cursor.execute(
        'SELECT player_currency FROM logins WHERE username = ?',
        (username,))
    result = cursor.fetchone()
    if result:
        player_currency = result[0]
    else:
        player_currency = 0
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
            username = current_user
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
        return jsonify({'error': error_msg}), 400

@app.route('/leaderboard')
def leaderboard():
    conn_users = sqlite3.connect('user_info.db')
    cursor_users = conn_users.cursor()

    cursor_users.execute("SELECT username, player_kills, player_deaths FROM logins")
    rows = cursor_users.fetchall()

    kdr_list = []
    for row in rows:
        username, kills, deaths = row
        kdr = get_KDR(kills, deaths)
        kdr_display = f"{kills}-{deaths}"
        
        kdr_list.append((username,kdr_display,kdr))
        sorted_kdr_list = sorted(kdr_list, key=lambda x: x[2], reverse=True)

    return render_template('leaderboard.html', kdr_list=sorted_kdr_list)

def get_KDR(kills, deaths):
    if kills > 0 and deaths == 0:
        return (100 * kills)
    elif deaths == 0:
        return (0)
    else:
        return (kills/deaths)
    
@app.route('/clear_session')
def clear_session():
    session.pop('_flashes',None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
