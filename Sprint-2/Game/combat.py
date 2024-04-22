from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)

class Player:
    def __init__(self, basics, inv, moves, treas): 
        self.loginInfo = basics
        self.inventory = inv
        self.moves = moves
        self.treasure = treas

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
    
    itemsArray = []
    enemiesArray = []
    
    for entry in itemData:
        itemsArray.append({'name': entry[0], 'description': entry[1], 'identifier': entry[2], 'icon': entry[3], 'hp_buff': entry[4],
                    'atk_buff': entry[5], 'def_buff': entry[6], 'duration': entry[7], 'cooldown': entry[8], 'price': entry[9]})
    for entry in enemyData:
        waveString = str(currentPlayer['wave']) + ":"
        print(entry)
        if (waveString in entry[1]):
            waveNumberIndex = entry[1].find(waveString)
            numEnemyType = int(entry[1][(waveNumberIndex + 2):(waveNumberIndex+3)])
            enemyMoves = getEnemyMoves(entry[0])
            for i in range(numEnemyType): 
                enemiesArray.append({'name': entry[0] + " " + str(i + 1), 'icon': entry[2], 'hp': entry[3], 'atk': entry[4], 'def': entry[5], 'moves': enemyMoves})
        
    items_json = json.dumps(itemsArray)
    enemies_json = json.dumps(enemiesArray)
    player_json = json.dumps(currentPlayer)
    print(enemiesArray)
    return render_template('combat.html', enemiesData=enemies_json, itemData=items_json, playerData=player_json)

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

def getEnemyMoves(enemyName):
    conn = sqlite3.connect('enemies.db')
    
    rawData = conn.execute('SELECT * FROM enemy_moves WHERE enemy = ?', (enemyName,)).fetchall()
    enemyMoves = []
    #Only getting the move names
    for entry in rawData:
        enemyMoves.append(entry[1]);
    return enemyMoves
    
    

if __name__ == "__main__":
    app.run(debug=True)