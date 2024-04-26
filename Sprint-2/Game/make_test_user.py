import sqlite3

if __name__ == "__main__":
    conn_users = sqlite3.connect('user_info.db')
    cursor_users = conn_users.cursor()
    
    conn_items = sqlite3.connect('items.db')
    cursor_items = conn_items.cursor()

    cursor_users.execute("""INSERT INTO logins (username, password, player_health, player_atk, player_def, player_currency, player_kills, player_deaths, player_waveflag)
                                VALUES (?,?,?,?,?,?,?,?,?)
                                """,("Tester", "HahaTh1sSucks.", 100, 1, 1, 100, 0, 0, 1))

    cursor_items.execute("SELECT * FROM game_items WHERE identifer = 'BM'")
    rows = cursor_items.fetchall()

    for row in rows:
        cursor_users.execute("""INSERT INTO user_moves(user, move_name)
                                VALUES(?,?)
                                """, ("Tester", row[0]))
    cursor_items.execute("SELECT * FROM game_items WHERE identifer = 'SH_WDA_UI'")
    rows = cursor_items.fetchall()
    for row in rows:
        cursor_users.execute("""INSERT INTO user_inventory(user, item_name, quantity)
                                VALUES(?,?,?)
                                """, ("Tester", row[0], 1))

    conn_users.commit()
    conn_users.close()