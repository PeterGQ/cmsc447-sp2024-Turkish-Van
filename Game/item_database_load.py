import sqlite3

conn = sqlite3.connect('items.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE game_items (
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            identifer TEXT NOT NULL,
            icon TEXT,
            atk INT,
            hp_buff INT,
            atk_buff INT,
            def_buff INT,
            duration INT,
            cooldown INT,
            price INT )
            """)

item_list = [
    #Health Items
    ("Herbal Tonic", "Restores 15 HP", "SH_WDA_UI", r"Icons\Herbal Tonic.png", 0, 15, None, None, 100, 0, 5),
    ("Potion of Healing", "Restores 35 HP", "SH_WDA_UI", r"Icons\Potion of Healing.png", 0, 35, None, None, 100, 0, 15),
    ("Elixir of Vitality", "Restores 60 HP and increases the player’s attack strength by 15 percent for 2 turns.", "SH_WDA_UI", r"Icons\Elixir of Vitality.png", 0, 60, 1.15, None, 2, 0, 30),
    ("Divine Blessing", "Fully restores health (100 HP) and provides a damage reduction effect of 50 percent for 2 turns.", "SH_WDA_UI", r"Icons\Divine Blessing.png", 0, 100, None, 0.5, 2, 0, 50),

    #Strength and Defense Items
    ("Longsword Upgrade: Balanced Hilt", "An upgrade that permanently increases the player’s attack by 15% when equipped", "SH_EQ", r"Icons\Longsword Upgrade Balanced Hilt.png", 0, None, 1.15, None, 100, 0, 15),
    ("Longsword Upgrade: Sharpened Blade", "An upgrade that increases the player’s attack by 30%", "SH_EQ", r"Icons\Longsword Upgrade Sharpened Blade.png", 0, None, 1.30, None, 100, 0, 45),
    ("Leather Armlet", "A basic accessory that reduces incoming damage by 10% when equipped.", "SH_EQ", r"Icons\Leather Armlet.png", 0, None, None, .10, 100, 0, 10),
    ("Guardian’s Breastplate", "An upgraded accessory that reduces incoming damage by 25%", "SH_EQ", r"Icons\Guardian’s Breastplate.png", 0, None, None, .25, 100, 0, 40),
    ("Goblin Blood Vial", " A vial containing goblin blood that, when consumed the players strength increase by 15 percent and defense by 10 percent", "SH_WDA_UI", r"Icons\Goblin Blood Vial.png", 0, None, 1.15, 0.10, 4, 0, 30),
    ("Elixir of Fortitude", "A special elixir that provides a 15 percent boost to the player's defense for 5 turns.", "SH_WDA_UI", r"Icons\Elixir of Fortitude.png", 0, None, None, .15, 100, 0, 40),
    ("Iron Skin Potion", "A potion that grants the player increased resistance to physical damage, reducing it by 20 percent for 4 turns.", "SH_WDA_UI", r"Icons\Iron Skin Potion.png", 0, None, None, .20, 4, 0, 35),
    ("Warrior's Draught", "A simple draught that provides a reliable boost to the player's attack strength. When consumed, it grants a 10 percent increase in attack strength for 3 turns", "SH_WDA_UI", r"Icons\Warrior's Draught.png", 0, None, 1.10, None, 3, 0, 10),

    #Moves
    ("Sword Slash", "A simple but effective attack that deals moderate damage to a single enemy.", "BM", r"Icons\Sword Slash.png", 1, None, None, None, 1, 0, 0),
    ("Guard Stance", "A defensive stance that reduces incoming damage by 10 percent for 2 turns.", "BM", r"Icons\Guard Stance.png", 0, None, None, 0.10, 2, 2, 0),
    ("Restorative Strike", "A special attack that deals light damage to an enemy and restores 10 HP. 4 Turn Cooldown", "BM", r"Icons\Restorative Strike.png", 1, 10, 1.05, None, 1, 4, 0),
    ("Goblin Cleave", "A quick attack with moderate damage, similar to a standard goblin attack. It cannot be used for the next 3 turns", "FM_WDO", r"Icons\Goblin Cleave.png", 1.5, None, None, None, 1, 3, 0),
    ("Goblin Warcry", "A move inspired by the goblin warriors that increases both strength and defense by 15 percent for 2 turns.  It cannot be used for the next 4 turns.", "FM_WDT", r"Icons\Goblin Warcry.png", 0, None, 1.15, .15, 2, 4, 0),
    ("Goblin Spellshield", "A move inspired by wizard goblins that makes the player invincible for 2 turns. It cannot be used for the next 10 turns.", "FM_SH", r"Icons\Goblin Spellshield.png", 0, None, None, 0, 2, 10, 100),

]
cur.executemany("INSERT INTO game_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", item_list)
conn.commit()


cur.execute("""CREATE TABLE shop_items (
            shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            identifer TEXT NOT NULL,
            icon TEXT,
            atk INT,
            hp_buff INT,
            atk_buff INT,
            def_buff INT,
            duration INT,
            cooldown INT,
            price INT )
            """)
cur.execute("SELECT * FROM game_items WHERE identifer LIKE '%SH%'")
rows = cur.fetchall()
cur.executemany("INSERT INTO shop_items (name, description, identifer, icon, atk, hp_buff, atk_buff, def_buff, duration, cooldown, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ", rows)
conn.commit()

conn.close()