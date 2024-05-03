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
Accessing the Game: 

The game can be accessed by running login.py within the Sprint3/Game folder

Minimum System Requirements:

    Display: 16:9 aspect ratio monitor or wider, supporting at least 1280 x 720 resolution.
    Operating System: Windows, macOS, Linux, or Chrome OS with the latest updates installed.
    Web Browser: Latest versions of Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari (for macOS users).
    Internet Connection: A stable internet connection is required to access GitHub and play the game.
    GitHub Account: Users need to have a GitHub account or be willing to create one.

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

Programming Languages and Libraries:

Programming Languages

    Python: The primary programming language used for server-side logic, handling game mechanics, player input, and database operations.
    JavaScript: Used for client-side scripting and interactivity in the game's web interface.
    HTML and CSS: Used for structuring and styling the game's web pages.
Frameworks and Libraries

    Flask: A lightweight web framework for Python, used to create the game's web server and handle HTTP requests.
    SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library, used for interacting with the game's database.
   
Credits and Acknowledgments

Credits

    Stephen Aldred: Lead Game Developer
    Noelle Alston: Backend Developer and UI Designer
    Peter Gatira: Game Developer and UI Designer
    Bhojraj Pandey: Game Developer and Quality Assurance Analyst

Acknowledgments

We would also like to express our gratitude to the following external resources and open-source libraries used in the game's development:
        
    Flask (https://flask.palletsprojects.com/)
    SQLAlchemy (https://www.sqlalchemy.org/)
    
Contact Information and Support:
For any questions, comments, or support inquiries, please reach out to our development team via the following channels:
    
    Stephen Aldred: saldred1@umbc.edu
    Noelle Alston: bn74019@umbc.edu
    Peter Gatira: pgatira1@umbc.edu
    Bhojraj Pandey: nn13856@umbc.edu
