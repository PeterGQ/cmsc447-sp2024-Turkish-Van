Game Title and Brief Description: 
"Dark Ascent" is a turn-based RPG game set in a mysterious world infested with goblins. Players must use strategy to embark on an adventure and overcome these goblins. The game features three types of goblins, namely the standard goblin, the warrior goblin, and the wizard goblin. To progress through the game, players must face three increasingly challenging waves of combat. Players can visit the in-game shop to buy items and unlock powerful goblin moves to gain an advantage in battle. The game also includes a leaderboard to encourage competition and engagement among players. Players must first register or log in to access the game to ensure a personalized gaming experience.

How to Play: 
To ensure that your progress is saved, it is necessary to log in or register to the website. Once you have completed this step, you will be able to either start a new game or continue a saved game from the main menu. You can navigate through the game world by using either the mouse or touch controls, whether it be entering combat or going to the shop. While in the shop, you can select the item you wish to purchase and press "confirm" to complete the transaction. During combat, you must select your actions from the available options and target enemies. It is important to manage your resources strategically, upgrade your skills, and equip items to gain an advantage in combat. If you wish to check the leaderboard, simply go to the main menu and click on the leaderboard. Lastly, when you are finished playing, exit the game through the main menu.

Game Modes and Features:
Single-player campaign mode with three difficulty levels,
Three distinct goblin classes to battle against,
In-game shop for items and abilities,
Leaderboard to compete with other players,
Save and load functionality

Code Structure:
/Game: This folder holds the game's main files and subfolders.
    ___.py: The main entry point of the game.
    items.db: The database file tables relating to the game items and their stats.
    user_info.db: The database file tables relating to the user/play information. Used to save player information as they go in and out of the game.
    enemies.db: The database file tables relating to the enemies including their assets, moves, and drops
        Each of these databases has its own py file to load them.
/Game/static: This folder holds all the game's static assets and files.
    images/: Contains subfolders for character sprites, backgrounds, UI elements, and other visual assets.
    css/: Contains CSS files for styling the game's HTML elements.
    fonts/: Contains various font files used in the game.
    js/: Contains JavaScript files used for client-side scripting and game logic.
/Game/templates: This folder holds all the HTML files for the game, which define the game's user interface and web pages.
    combat.html: Contains the HTML template for the combat screen, including player and enemy health bars, ability buttons, and combat-related UI elements.
    leaderboard.html: Contains the HTML template for the leaderboard screen, displaying top-ranking players and their scores.
    login.html: Contains the HTML template for the login screen, allowing players to log in or register for the game.
    mainMenu.html: Contains the HTML template for the main menu screen, providing options to start a new game, continue a saved game, or access other game features.
    map.html: Contains the HTML template for the game's map, displaying various locations, points of interest, and player progress.
    register.html: Contains the HTML template for the registration screen, allowing new players to create an account and join the game.
    shop.html: Contains the HTML template for the in-game shop, allowing players to purchase items, abilities, or upgrades using in-game currency.

