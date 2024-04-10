from flask import Flask, render_template
import sqlite3
app = Flask(__name__)

@app.route('/')
def main_menu():
    return render_template('mainMenu.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
@app.route('/restArea')
def restArea():
    return render_template('restArea.html')

@app.route('/ranking')
def ranking():
  return render_template('ranking.html')

@app.route('/register')
def treasure():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
