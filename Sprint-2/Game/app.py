from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('game.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

@app.route("/")
def display():
    conn = get_db_connection()
    players = conn.execute('SELECT * FROM player_scores ORDER BY score DESC').fetchall()
    conn.close()
    return render_template('mainMenu.html', players=players)

if __name__ == "__main__":
    app.run(debug=True)
