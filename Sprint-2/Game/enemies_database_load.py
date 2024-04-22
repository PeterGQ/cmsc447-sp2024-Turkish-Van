import sqlite3

conn = sqlite3.connect('enemies.db')
cur = conn.cursor()

#Wave Identifier Syntax: "(Wave Number):(Number Of Enemy Types)"
cur.execute("""CREATE TABLE enemies (
            name TEXT NOT NULL,
            waveIdentifier TEXT NOT NULL,
            icon TEXT,
            hp INT,
            atk INT,
            def INT,
            
            PRIMARY KEY (name))
            """)

enemy_list = [
    ("Goblin", "1:2 2:2 3:1", "/static/assets/characters/goblin.png" , 30, 1, .5),
    ("Goblin Brute", "3:1", "/static/assets/characters/goblin_brute.png", 60, 1.5, .5),
    ("Goblin Mage", "2:1 3:1", "/static/assets/characters/goblin_mage.png", 30, 1, .5),
    
]
cur.executemany("INSERT INTO enemies VALUES (?, ?, ?, ?, ?, ?)", enemy_list)
conn.commit()

cur.execute("""CREATE TABLE enemy_moves(
            enemy TEXT NOT NULL,
            move_name TEXT NOT NULL,

            PRIMARY KEY (enemy, move_name),
            FOREIGN KEY (enemy) REFERENCES enemies(name),
            FOREIGN KEY (move_name) REFERENCES game_items(name)
            )
            """)

enemy_move_list = [
    #Goblin's oves
    ("Goblin", "Sword Slash"),
    ("Goblin", "Guard Stance"),
    
    #Goblin Brute's moves
    ("Goblin Brute", "Sword Slash"),
    ("Goblin Brute", "Guard Stance"),
    ("Goblin Brute", "Goblin Warcry"),
    ("Goblin Brute", "Goblin Cleave"),
    
    #Goblin Mage's moves
    ("Goblin Mage", "Restorative Strike"),
    ("Goblin Mage", "Guard Stance"),
    ("Goblin Mage", "Goblin Spellshield")
]

cur.executemany("INSERT INTO enemy_moves VALUES (?, ?)", enemy_move_list)
conn.commit()
conn.close()