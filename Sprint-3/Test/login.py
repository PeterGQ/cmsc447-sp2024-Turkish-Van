import random
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, flash, redirect, url_for, session, json, jsonify
from flask_session import Session
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
current_user = ""
current_player_data = None
starting_moves = ['Sword Slash', 'Guard Stance', 'Restorative Strike']
starting_stats = [100, 1, 1, 100, 0, 0, 1]

@app.route('/')
def index():
    return redirect(url_for('login'))

##----------------------------------------------------------------------
#LOGIN AND REGISTRATION
#-----------------------------------------------------------------------
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
    global current_user
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

#----------------------------------------------------------------------------------
# MAIN MENU
#----------------------------------------------------------------------------------
@app.route('/render-menu', methods=['POST'])
def renderMenu():
    return redirect(url_for('main_menu'))
@app.route('/main_menu')
def main_menu():
    loadPlayer(current_user)
    newPlayer = 0
    if (len(current_player_data['inventory']) == 0 and len(current_player_data['moves']) == 3 and current_player_data['currency'] == 100):
        newPlayer = 1
    
    return render_template("mainMenu.html", newPlayerFlag = newPlayer)

@app.route('/load-game', methods = ['POST'])
def load_user():
    if request.method == 'POST':
        print(current_user)
        loadPlayer(current_user)
        print(current_player_data['moves'])
        if (len(current_player_data['moves']) == 0):
            flash('You haven\'t started a game yet!')
            return redirect(url_for('main_menu'))
        return redirect('/start-map')
    return redirect('/')

@app.route('/new-game', methods = ['POST'])
def new_game():
    if request.method == 'POST':
        global starting_stats
        global starting_moves
        conn_users = sqlite3.connect('user_info.db')
        #Deleting any data that's there
        #try:
        conn_users.execute("DELETE FROM user_moves WHERE user = ?", (current_user,))
        conn_users.commit()
        #except Error as e:
        #    print(f"No data from user_moves to delete")
        #    conn_users.rollback()
        try:
            conn_users.execute("DELETE FROM user_inventory WHERE user = ?", (current_user,))
            conn_users.commit()
        except Error as e:
            print(f"No data from user_inventory to delete")
            conn_users.rollback()
            
        #Adding starting moves and setting player data to default, because they shouldn't have anything
        conn_users.execute('UPDATE logins SET player_health = ?, player_atk = ?, player_def = ?, player_currency = ?, player_kills = ?, player_deaths = ?, player_waveflag = ?'
                            + 'WHERE username = ?', (starting_stats[0], starting_stats[1], starting_stats[2], starting_stats[3], starting_stats[4], starting_stats[5], starting_stats[6], current_user))
        for i in range(len(starting_moves)):
            conn_users.execute("INSERT INTO user_moves (user, move_name) VALUES (?, ?)",(current_user, starting_moves[i]))
        conn_users.commit()
        conn_users.close()

        loadPlayer(current_user)
        return redirect('/start-map')
    return redirect('/')


#----------------------------------------------------------------------------------
# LEADERBOARD
#----------------------------------------------------------------------------------
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
        return (1.1 * kills)
    elif deaths == 0:
        return (0)
    else:
        return (kills/deaths)
    
@app.route('/clear_session')
def clear_session():
    session.pop('_flashes',None)
    return redirect(url_for('login'))
current_player_data = {}


#----------------------------------------------------------------------------
# MAP
#----------------------------------------------------------------------------
@app.route('/start-map', methods=['GET', 'POST'])
def startMap():
    return redirect('/gameMap')

@app.route('/gameMap')
def mapRender():
    loadPlayer(current_user)
    print(current_user)
    itemNames = []
    itemQuantities = []
    for itemName, itemQuantity in current_player_data['inventory'].items():
        itemNames.append(itemName)
        itemQuantities.append(itemQuantity)

    return render_template('map.html', hp = current_player_data['hp'], currency = current_player_data['currency'], 
                           moves = current_player_data['moves'], itemNames = itemNames, itemQuantities = itemQuantities, len=len(itemNames))

@app.route('/start-battle', methods=['POST'])
def battle():
    return redirect('/combat')

@app.route('/start-shop', methods=['POST'])
def start_shop():
    return redirect('/shop')

#----------------------------------------------------------------------------
# SHOP
#----------------------------------------------------------------------------
@app.route("/shop")
def display():
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    username = current_user
    print(username)
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
                (currency_value,username))
            conn.commit()
            conn.close()
            conn = sqlite3.connect('user_info.db')
            cursor = conn.cursor()
            username = current_user
            # Assuming 'image_id' is the name of the item
            cursor.execute(
                'SELECT player_currency FROM logins WHERE username = ?',
                (username,))
            result = cursor.fetchone()
            print(currency_value)
            print(current_user)
            print(result)
            conn.close()
            image_id = req_data['item']
            print("image_id")
            conn = sqlite3.connect('user_info.db')
            cursor = conn.cursor()

            if image_id == 'Goblin Spellshield':
                cursor.execute('INSERT INTO user_moves VALUES (?, ?)',
                               (username, image_id))
                conn.commit()
                print("not in db")
            else:
                query = 'SELECT * FROM user_inventory WHERE user = ? AND item_name = ?'
                cursor.execute(query, (username, image_id))
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


#----------------------------------------------------------------------------
# COMBAT
#------------------------------------------------------------------------------
@app.route("/combat")
def combat():
    conn1 = sqlite3.connect('items.db')
    conn2 = sqlite3.connect('enemies.db')
    loadPlayer(current_user)
    
    itemData = conn1.execute('SELECT * FROM game_items').fetchall()
    enemyData = conn2.execute('SELECT * FROM enemies').fetchall()
    
    
    conn1.close()
    conn2.close()
    
    itemsArray = getAllItems(itemData)
    enemiesArray = getEnemiesForWave(enemyData)
        
    items_json = json.dumps(itemsArray)
    enemies_json = json.dumps(enemiesArray)
    player_json = json.dumps(current_player_data)
    return render_template('combat.html', enemiesData=enemies_json, itemData=items_json, playerData=player_json)

@app.route('/returnToMap/', methods = ['GET', 'POST'])
def returnToMap():
    if request.method == 'POST':
        winCondition = -1
        inventory = []
        kills = 0
        req_data = request.get_json()
        print(req_data)
        #Ensuring the data is valid, in which case grab it
        if (req_data and 'inventory' in req_data and 'condition' in req_data and 'kills' in req_data):
            winCondition = req_data['condition']
            inventory = req_data['inventory']
            kills = req_data['kills']
        else:
            raise ValueError('Invalid JSON data')
        
        conn1 = sqlite3.connect('enemies.db')
        conn2 = sqlite3.connect('user_info.db')
        conn3 = sqlite3.connect('items.db')
        
        for i in range(len(inventory)):
            conn2.execute('UPDATE user_inventory SET quantity = ? WHERE user = ? AND item_name = ?', (inventory[i]['quantity'], current_player_data['username'], inventory[i]['name']))
            conn2.commit()
        
        current_player_data['kills'] += kills
        conn2.execute('UPDATE logins SET player_kills = ? WHERE username = ?', (current_player_data['kills'], current_player_data['username']))
        conn2.commit()
        
        #If the user won the game
        if (winCondition == 1):
            #Getting data to transfer currency and items dropped from enemy    
            enemyData = conn1.execute('SELECT * FROM enemies').fetchall()
            itemData =  conn3.execute('SELECT * FROM game_items').fetchall()
            
            enemies = getEnemiesForWave(enemyData)
            items = getAllItems(itemData)
            
            
            
            #Getting gold and rewards for player
            totalEarned = 0
            for enemy in enemies:
                totalEarned += enemy['goldDrop']
                for drop in enemy['drops'].keys():
                    for i in range(len(items)):
                        isMove = False
                        if (drop == items[i]['name']):
                            if ("FM" in items[i]['identifier']):
                                isMove = True
                                break
                            else:
                                break
                    if (isMove and (drop not in current_player_data['moves'])):
                        current_player_data['moves'].append(drop)
                        conn2.execute('INSERT INTO user_moves VALUES (?, ?)', (current_player_data['username'], drop))
                        conn2.commit()
                    #If the player doesn't have this item yet
                    elif (not isMove and (drop not in current_player_data['inventory'])):
                        conn2.execute('INSERT INTO user_inventory VALUES (?, ?, ?)', (current_player_data['username'], drop, enemy['drops'][drop]))
                        current_player_data['inventory'][drop] = enemy['drops'][drop]
                        conn2.commit()
                    elif (not isMove and (drop in current_player_data['inventory'])):
                        item = conn2.execute('SELECT * FROM user_inventory WHERE user = ? AND item_name = ?', (current_player_data['username'], drop)).fetchall()
                        newAmount = item[0][2] + enemy['drops'][drop]
                        conn2.execute('UPDATE user_inventory SET quantity = ? WHERE user = ? AND item_name = ?', (newAmount, current_player_data['username'], drop))
                        conn2.commit()
            
            current_player_data['currency'] += totalEarned
            conn2.execute('UPDATE logins SET player_currency = ? WHERE username = ?', (current_player_data['currency'], current_player_data['username']))
            current_player_data['wave'] += 1
            conn2.execute('UPDATE logins SET player_waveflag = ? WHERE username = ?', (current_player_data['wave'], current_player_data['username']))
            conn2.commit()
            
        elif (winCondition == 0):
            conn2 = sqlite3.connect('user_info.db')
            current_player_data['deaths'] += 1
            conn2.execute('UPDATE logins SET player_deaths = ? WHERE username = ?', (current_player_data['deaths'], current_player_data['username']))
            conn2.commit()

        #Closing all connections
        conn1.close()
        conn2.close()
        conn3.close()
        
    return redirect("/start-map")

def loadPlayer(user):
    conn = sqlite3.connect('user_info.db')
    
    loginInfo = conn.execute('SELECT * FROM logins WHERE username = ?', (user,)).fetchone()
    inventory = conn.execute('SELECT * FROM user_inventory WHERE user = ?', (user,)).fetchall()
    moves = conn.execute('SELECT * FROM user_moves WHERE user = ?', (user,)).fetchall()
    
    if (loginInfo != None):
        current_player_data['username'] = loginInfo[0]
        current_player_data['hp'] = loginInfo[2]
        current_player_data['atk'] = loginInfo[3]
        current_player_data['def'] = loginInfo[4]
        current_player_data['currency'] = loginInfo[5]
        current_player_data['kills'] = loginInfo[6]
        current_player_data['deaths'] = loginInfo[7]
        current_player_data['wave'] = loginInfo[8]
        current_player_data['inventory'] = {}
        current_player_data['moves'] = []
    
        for item in inventory:
            current_player_data['inventory'][item[1]] = item[2]

        for move in moves:
            current_player_data['moves'].append(move[1])
    
    conn.close()

def getEnemiesForWave(enemyData):
    print(enemyData)
    enemiesArray = []
    if (current_player_data['wave'] <= 3):
        for entry in enemyData:
            waveString = str(current_player_data['wave']) + ":"
            if (waveString in entry[1]):
                waveNumberIndex = entry[1].find(waveString)
                numEnemyType = int(entry[1][(waveNumberIndex + 2):(waveNumberIndex+3)])
                enemyMoves = getEnemyMoves(entry[0])
                enemyDrops = getEnemyDrops(entry[0])
                for i in range(numEnemyType): 
                    enemiesArray.append({'name': entry[0] + " " + str(i + 1), 'icon': entry[2], 'hp': entry[3], 'atk': entry[4], 'def': entry[5], 'goldDrop':entry[6], 'moves': enemyMoves, 'drops': enemyDrops})
    else:
        for i in range(3):
            enemyBeingAdded = random.randint(0, len(enemyData)-1)
            enemyMoves = getEnemyMoves(enemyData[enemyBeingAdded][0])
            enemyDrops = getEnemyDrops(enemyData[enemyBeingAdded][0])
            enemiesArray.append({'name': enemyData[enemyBeingAdded][0] + " " +str(i+1), 'icon': enemyData[enemyBeingAdded][2], 'hp': enemyData[enemyBeingAdded][3], 'atk': enemyData[enemyBeingAdded][4], 'def': enemyData[enemyBeingAdded][5], 'goldDrop':enemyData[enemyBeingAdded][6], 'moves': enemyMoves, 'drops': enemyDrops})
    return enemiesArray


def getEnemyMoves(enemyName):
    conn = sqlite3.connect('enemies.db')
    
    rawData = conn.execute('SELECT * FROM enemy_moves WHERE enemy = ?', (enemyName,)).fetchall()
    enemyMoves = []
    #Only getting the move names
    for entry in rawData:
        enemyMoves.append(entry[1]);
    return enemyMoves

def getEnemyDrops(enemyName):
    conn = sqlite3.connect('enemies.db')
    
    rawData = conn.execute('SELECT * FROM enemy_drops WHERE enemy = ?', (enemyName,)).fetchall()
    enemyDrops = {}
    #Only getting the move names
    for entry in rawData:
        enemyDrops[entry[1]] = entry[2]
    return enemyDrops
    
def getAllItems(itemData):
    itemsArray = []
    for entry in itemData:
        itemsArray.append({'name': entry[0], 'description': entry[1], 'identifier': entry[2], 'icon': entry[3], 'atk': entry[4], 'hp_buff': entry[5],
                    'atk_buff': entry[6], 'def_buff': entry[7], 'duration': entry[8], 'cooldown': entry[9], 'price': entry[10]})
    return itemsArray
    

if __name__ == "__main__":
    app.run(debug=True)