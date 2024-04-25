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
            goldDrop INT,
            
            PRIMARY KEY (name))
            """)

enemy_list = [
    ("Goblin", "1:2 2:2 3:1", "/static/assets/characters/goblin.png" , 30, 1, 1, 10),
    ("Goblin Brute", "3:1", "/static/assets/characters/goblin_brute.png", 60, 1.5, .5, 5),
    ("Goblin Mage", "2:1 3:1", "/static/assets/characters/goblin_mage.png", 30, 1, .5, 5),
]
cur.executemany("INSERT INTO enemies VALUES (?, ?, ?, ?, ?, ?, ?)", enemy_list)
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

cur.execute("""CREATE TABLE enemy_drops(
            enemy TEXT NOT NULL,
            drop_name TEXT NOT NULL,
            quantity INT NOT NULL,

            PRIMARY KEY (enemy, drop_name),
            FOREIGN KEY (enemy) REFERENCES enemies(name),
            FOREIGN KEY (drop_name) REFERENCES game_items(name)
            )
            """)

enemy_drop_list = [
    #Goblin's item/move drops
    ("Goblin", "Goblin Blood Vial", 1),
    ("Goblin", "Goblin Warcry", 1),
    #Goblin Brute's item/move drops
    ("Goblin Brute", "Goblin Blood Vial", 1),
    ("Goblin Brute", "Goblin Warcry", 1),
    ("Goblin Brute", "Goblin Cleave", 1),
    
    #Goblin Mage's item/move drops
    ("Goblin Mage", "Herbal Tonic", 1),
    ("Goblin Mage", "Goblin Spellshield", 1)
]

cur.executemany("INSERT INTO enemy_drops VALUES (?, ?, ?)", enemy_drop_list)
conn.commit()

conn.close()
