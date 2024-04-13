from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)


@app.route("/")
def combat():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    
    data = conn.execute('SELECT * FROM game_items').fetchall()
    itemsArray = []
    conn.close()
    for entry in data:
        itemsArray.append({'name': entry[0], 'description': entry[1], 'identifier': entry[2], 'icon': entry[3], 'hp_buff': entry[4],
                    'atk_buff': entry[5], 'def_buff': entry[6], 'duration': entry[7], 'cooldown': entry[8], 'price': entry[9]})
        print(entry[0])
    items_json = json.dumps(itemsArray)
    print(items_json)
    return render_template('combat.html', data=items_json)

if __name__ == "__main__":
    app.run(debug=True)