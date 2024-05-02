import sqlite3

conn = sqlite3.connect('user_info.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE logins (
            username VARCHAR UNIQUE NOT NULL,
            password VARCHAR NOT NULL,
            player_health INT,
            player_atk INT,
            player_def INT,
            player_currency INT,
            player_kills INT,
            player_deaths INT,
            player_waveflag INT
            )
            """)

conn.commit()


cur.execute("""CREATE TABLE user_inventory(
            user VARCHAR NOT NULL,
            item_name TEXT NOT NULL,
            quantity INT NOT NULL,

            PRIMARY KEY (user, item_name),
            FOREIGN KEY (user) REFERENCES login(usename),
            FOREIGN KEY (item_name) REFERENCES game_items(name)
            )
            """)

cur.execute("""CREATE TABLE user_moves(
            user VARCHAR NOT NULL,
            move_name TEXT NOT NULL,

            PRIMARY KEY (user, move_name),
            FOREIGN KEY (user) REFERENCES login(usename),
            FOREIGN KEY (move_name) REFERENCES game_items(name)
            )
            """)

conn.commit()