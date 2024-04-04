from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route("/")
def display():
    return render_template('combat.html')

if __name__ == "__main__":
    app.run(debug=True)