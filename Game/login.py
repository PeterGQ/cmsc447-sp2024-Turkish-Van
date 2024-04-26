import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, session, json
from flask_session import Session
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
current_user = ""
current_player_data = None

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
current_player_data = {}

@app.route('/load-game')
def load_user():
    print(current_user)
    loadPlayer(current_user)
    return redirect(url_for('combat'))

@app.route("/combat", methods = ['GET'])
def combat():
    print("in function")
    conn1 = sqlite3.connect('items.db')
    conn2 = sqlite3.connect('enemies.db')
    
    
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
        winCondition = request.form['winCondition']
        #If the user won the game
        if (winCondition == "1"):
            #Getting data to transfer currency and items dropped from enemy
            conn1 = sqlite3.connect('enemies.db')
            conn2 = sqlite3.connect('user_info.db')
            conn3 = sqlite3.connect('items.db')
            enemyData = conn1.execute('SELECT * FROM enemies').fetchall()
            itemData =  conn3.execute('SELECT * FROM game_items').fetchall()
            conn1.close()
            conn3.close()
            
            #Converting it to usable data
            enemies = getEnemiesForWave(enemyData)
            items = getAllItems(itemData)
            
            
            #Getting gold and rewards for player
            totalEarned = 0 #
            for enemy in enemies:
                #Amount of gold earned
                totalEarned += enemy['goldDrop']
                
                #Adding item/move drops to user inventory
                for drop in enemy['drops'].keys():
                    #Checking whether it's a move or item
                    for i in range(len(items)):
                        isMove = False
                        if (drop == items[i]['name']):
                            if ("FM" in items[i]['identifier']):
                                isMove = True
                                break
                            else:
                                break
                    #Inserting the move drop if the user doesn't have it already
                    if (isMove and (drop not in current_player_data['moves'])):
                        current_player_data['moves'].append(drop)
                        conn2.execute('INSERT INTO user_moves VALUES (?, ?)', (current_player_data['username'], drop))
                        conn2.commit()
                    #If the player doesn't have this item yet, make a new entry
                    elif (not isMove and (drop not in current_player_data['inventory'])):
                        conn2.execute('INSERT INTO user_inventory VALUES (?, ?, ?)', (current_player_data['username'], drop, enemy['drops'][drop]))
                        conn2.commit()
                    #If the player has this entry, update the quantity in the database
                    elif (not isMove and (drop in current_player_data['inventory'])):
                        item = conn2.execute('SELECT * FROM user_inventory WHERE user = ? AND item_name = ?', (current_player_data['username'], drop)).fetchall()
                        newAmount = item[0][2] + enemy['drops'][drop]
                        conn2.execute('UPDATE user_inventory SET quantity = ? WHERE user = ? AND item_name = ?', (newAmount, current_player_data['username'], drop))
                        conn2.commit()
                        
            #Updating the users gold
            current_player_data['currency'] += totalEarned
            conn2.execute('UPDATE logins SET player_currency = ? WHERE username = ?', (current_player_data['currency'], current_player_data['username']))
            current_player_data['wave'] += 1
            conn2.execute('UPDATE logins SET player_waveflag = ? WHERE username = ?', (current_player_data['wave'], current_player_data['username']))
            conn2.commit()
            
            conn2.close()
            
    redirect(url_for('main_menu'))

def loadPlayer(user):
    conn = sqlite3.connect('user_info.db')
    
    loginInfo = conn.execute('SELECT * FROM logins WHERE username = ?', (user,)).fetchone()
    inventory = conn.execute('SELECT * FROM user_inventory WHERE user = ?', (user,)).fetchall()
    moves = conn.execute('SELECT * FROM user_moves WHERE user = ?', (user,)).fetchall()
    treasure = conn.execute('SELECT * FROM user_treasure WHERE user = ?', (user,)).fetchall()
    
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
    current_player_data['treasure'] = []
    
    for item in inventory:
        current_player_data['inventory'][item[1]] = item[2]
    
    for move in moves:
        current_player_data['moves'].append(move[1])
    
    for relic in treasure:
        current_player_data['treasure'].append(relic[1])
    
    conn.close()

def getEnemiesForWave(enemyData):
    enemiesArray = []
    for entry in enemyData:
        waveString = str(current_player_data['wave']) + ":"
        if (waveString in entry[1]):
            waveNumberIndex = entry[1].find(waveString)
            numEnemyType = int(entry[1][(waveNumberIndex + 2):(waveNumberIndex+3)])
            enemyMoves = getEnemyMoves(entry[0])
            enemyDrops = getEnemyDrops(entry[0])
            for i in range(numEnemyType): 
                enemiesArray.append({'name': entry[0] + " " + str(i + 1), 'icon': entry[2], 'hp': entry[3], 'atk': entry[4], 'def': entry[5], 'goldDrop':entry[6], 'moves': enemyMoves, 'drops': enemyDrops})
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
        itemsArray.append({'name': entry[0], 'description': entry[1], 'identifier': entry[2], 'icon': entry[3], 'hp_buff': entry[4],
                    'atk_buff': entry[5], 'def_buff': entry[6], 'duration': entry[7], 'cooldown': entry[8], 'price': entry[9]})
    return itemsArray
    

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
