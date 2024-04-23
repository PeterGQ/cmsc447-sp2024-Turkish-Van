import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
current_user = None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/main_temp')
def main_temp():
    return render_template("main_temp.html")
    
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
            return redirect(url_for('main_temp'))
        
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

if __name__ == '__main__':
    app.run(debug=True)
