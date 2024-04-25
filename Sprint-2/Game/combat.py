from flask import Flask, render_template, request
import sqlite3
import json

app = Flask(__name__)

currentPlayer = {}

@app.route("/")
def combat():
    conn1 = sqlite3.connect('items.db')
    conn2 = sqlite3.connect('enemies.db')
    
    
    itemData = conn1.execute('SELECT * FROM game_items').fetchall()
    enemyData = conn2.execute('SELECT * FROM enemies').fetchall()
    
    
    conn1.close()
    conn2.close()
    
    loadPlayer("Tester")
    
    itemsArray = getAllItems(itemData)
    enemiesArray = getEnemiesForWave(enemyData)
        
    items_json = json.dumps(itemsArray)
    enemies_json = json.dumps(enemiesArray)
    player_json = json.dumps(currentPlayer)
    print(enemiesArray)
    return render_template('combat.html', enemiesData=enemies_json, itemData=items_json, playerData=player_json)

@app.route('/returnToMap/', methods = ['GET', 'POST'])
def returnToMap():
    print("in function")
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
                    if (isMove and (drop not in currentPlayer['moves'])):
                        currentPlayer['moves'].append(drop)
                        conn2.execute('INSERT INTO user_moves VALUES (?, ?)', (currentPlayer['username'], drop))
                        conn2.commit()
                    #If the player doesn't have this item yet
                    elif (not isMove and (drop not in currentPlayer['inventory'])):
                        conn2.execute('INSERT INTO user_inventory VALUES (?, ?, ?)', (currentPlayer['username'], drop, enemy['drops'][drop]))
                        conn2.commit()
                    elif (not isMove and (drop in currentPlayer['inventory'])):
                        item = conn2.execute('SELECT * FROM user_inventory WHERE user = ? AND item_name = ?', (currentPlayer['username'], drop)).fetchall()
                        print(item)
                        newAmount = item[0][2] + enemy['drops'][drop]
                        conn2.execute('UPDATE user_inventory SET quantity = ? WHERE user = ? AND item_name = ?', (newAmount, currentPlayer['username'], drop))
                        conn2.commit()
            
            currentPlayer['currency'] += totalEarned
            conn2.execute('UPDATE logins SET player_currency = ? WHERE username = ?', (currentPlayer['currency'], currentPlayer['username']))
            currentPlayer['wave'] += 1
            conn2.execute('UPDATE logins SET player_waveflag = ? WHERE username = ?', (currentPlayer['wave'], currentPlayer['username']))
            conn2.commit()
            
            conn2.close() 
            print(enemies)
            
    return render_template('dummy.html')

def loadPlayer(user):
    conn = sqlite3.connect('user_info.db')
    
    loginInfo = conn.execute('SELECT * FROM logins WHERE username = ?', (user,)).fetchone()
    inventory = conn.execute('SELECT * FROM user_inventory WHERE user = ?', (user,)).fetchall()
    moves = conn.execute('SELECT * FROM user_moves WHERE user = ?', (user,)).fetchall()
    treasure = conn.execute('SELECT * FROM user_treasure WHERE user = ?', (user,)).fetchall()
    
    currentPlayer['username'] = loginInfo[0]
    currentPlayer['hp'] = loginInfo[2]
    currentPlayer['atk'] = loginInfo[3]
    currentPlayer['def'] = loginInfo[4]
    currentPlayer['currency'] = loginInfo[5]
    currentPlayer['kills'] = loginInfo[6]
    currentPlayer['deaths'] = loginInfo[7]
    currentPlayer['wave'] = loginInfo[8]
    currentPlayer['inventory'] = {}
    currentPlayer['moves'] = []
    currentPlayer['treasure'] = []
    
    for item in inventory:
        currentPlayer['inventory'][item[1]] = item[2]
    
    for move in moves:
        currentPlayer['moves'].append(move[1])
    
    for relic in treasure:
        currentPlayer['treasure'].append(relic[1])
    
    conn.close()

def getEnemiesForWave(enemyData):
    enemiesArray = []
    for entry in enemyData:
        waveString = str(currentPlayer['wave']) + ":"
        print(entry)
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
    print(rawData)
    enemyDrops = {}
    #Only getting the move names
    for entry in rawData:
        print(enemyName)
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