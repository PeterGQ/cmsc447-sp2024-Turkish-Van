from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    return render_template('part9.html')
    # Example query to retrieve player information
    cursor.execute("SELECT username,player_healh, player_currency, player_atk, player_def FROM logins WHERE userID = ?", (1,))
    player_data = cursor.fetchone()  # Assuming you only expect one row

    conn.close()

    # Pass player data to the HTML template
    return render_template('part9.html', player_data=player_data)


# add a border to the map, should cover the watermark and include the title of the game
# add img when you hover over the button

if __name__ == "__main__":
    app.run(debug=True)