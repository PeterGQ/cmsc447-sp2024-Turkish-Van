import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/main_temp')
def main_temp():
    return "This would be the main menu"
    

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
            cursor_users.execute("""INSERT INTO user_inventory (user, item_name, quantity)
                                 VALUES(?,?,?)
                                 """, (username, row[0], 1))
        
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
            return redirect(url_for('main_temp'))
        
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')

    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)
