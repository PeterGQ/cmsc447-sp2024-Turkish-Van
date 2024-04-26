const baseAtkDamage = 20;
const maxPlayerHealth = 100;

var items;
var player;
var enemies;
var lastChoice = "";
var enemyMaxHps = [];
var lastingEffects = []; //Map to keep track of cooldowns 
var cooldowns = new Map(); //Map to keep track of cooldowns per character (key is characterName, value is list of moves)

//importItems()
//Imports the items database to be referenced later
function importItems(data) {
    items = JSON.parse(data);
    console.log(items);
}


//importEnemies
//Imports the enemies from the python backend
function importEnemies(data) {
    enemies = JSON.parse(data);
    console.log(enemies);
    displayEnemies();
    
    //Storying max hp to be printed later
    for (var i = 0; i < enemies.length; i++) {
        enemyMaxHps.push(enemies[i].hp);
    }
    console.log(enemyMaxHps);
}

//importPlayer
//Imports the player from the python backend
function importPlayer(data) {
    parsedJson = JSON.parse(data);
    //Converting playerData to map
    player = new Map(Object.entries(parsedJson));

    //Converting inventory to nested map
    inventory = new Map(Object.entries(player.get('inventory')));
    player.set('inventory', inventory);

    console.log(player);

    //Printing username and hp above player sprite
    document.getElementById("playerName").innerHTML = player.get('username');
    document.getElementById("playerHP").innerHTML = player.get('hp')+ "/100";
}

//getOptions()
//Lists available items/attacks for player to use
function getOptions(aOrI) {
    var newChoices = document.getElementById('choices');
    document.getElementById('enemies').innerHTML = "";
    newChoices.style.display = "inherit";
    lastChoice = "";
    //Option for if they choose attack, lists move they have
    if (aOrI == 1) {
        newChoices.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Attacks </a> </li>');
        for (var i = 0; i < player.get('moves').length; i++) {
            document.getElementById('attack').style.color = "#7f7dab"
            document.getElementById('items').style.color = "#9290C3"
            newChoices.innerHTML += '<li class="nav-item"><button class ="choice" id="'+ player.get('moves')[i] + '" onClick=\"getConfirmation(1, '+ i +')\">'
                + player.get('moves')[i] + '</button></li>';
        }
            
    }
    //Option for if they choose item, lists items they have
    else {
        newChoices.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Items </a> </li>');
        document.getElementById('items').style.color = "#7f7dab"
        document.getElementById('attack').style.color = "#9290C3"
        var i = 0;
        if (player.get("inventory").size > 0) {
            player.get("inventory").forEach((value, key) => {
                    newChoices.innerHTML += '<li class="nav-item"><button class ="choice" id="' + key + '" onClick=\"getConfirmation(0, \''+ key +'\')\">' +
                        key + " x" + value + '</button></li>';
            });
        }
        else {
            newChoices.innerHTML += "You have no items!";
        }
    }
}

//getConfirmation()
//Creates button for user to either choose enemy to attack/confirm they're using the right thing
function getConfirmation(aOrI, index) {
    var htmlElement = document.getElementById('enemies');
    htmlElement.style.display = "inherit";
    if(aOrI == 1) {
        document.getElementById(player.get("moves")[index]).style.color = "#7f7dab";
        if (lastChoice != "" && lastChoice != player.get("moves")[index]) {
            document.getElementById(lastChoice).style.color = "#9290C3";
        }
        lastChoice = player.get("moves")[index];
        console.log(lastChoice);
        var lastChoiceIndex = getItemIndex(lastChoice);
        console.log(lastChoiceIndex);
        console.log(isAttack(lastChoiceIndex));
        //Printing enemies to attack
        if (isAttack(lastChoiceIndex)) {
            htmlElement.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Enemies </a> </li>');
            for (var i = 0; i < enemies.length; i++) {
                if (enemies[i].hp > 0) {
                    htmlElement.innerHTML += '<li class=\"nav-item\"><button class =\"choice\" id=\'attack' + i + '\' onClick="startTurn(' + i +')">' + enemies[i].name + '</button></li>';
                }
            }
        }
        //Printing confirm button to ensure you want to buff yourself
        else {
            htmlElement.innerHTML = '<div class="confirm">' +
                                '<li class="nav-item"><button class ="choice" id=\'çonfirm\' onClick=\"startTurn(-1)\"> Confirm </button></li></div>';
        }
    }
    //Printing confirm button to ensure player wants to 
    else {
        document.getElementById(index).style.color = "#7f7dab";
        if (lastChoice != "" && lastChoice != index) {
            document.getElementById(lastChoice).style.color = "#9290C3";
        }
        lastChoice = index;
        htmlElement.innerHTML = '<div class="confirm">' +
                                '<li class="nav-item"><button class ="choice" id=\'çonfirm\' onClick=\"startTurn(-1)\"> Confirm </button></li></div>';
    }
}

//startTurn()
//Runs playerTurn and enemiesTurn
function startTurn(enemyIndex) {

    document.getElementById("log").innerHTML = "";

    //Player goes first'
    playerTurn(enemyIndex)
    //Enemies go in ascending order of list
    enemiesTurn()
    
    var gameState = checkWinOrLoss();

    if (gameState == -1) {
        document.getElementById('choices').innerHTML = "";
        document.getElementById('enemies').innerHTML = "";
    }
    else if (gameState == 0) {
        document.getElementById('game').innerHTML = "";
        generateEndScreen(gameState);
    }
    else if (gameState == 1) {
        document.getElementById('game').innerHTML = "";
        generateEndScreen(gameState);
    }
}

//playerTurn()
//Logic for player taking their turn
function playerTurn(enemyIndex) {
    //Attack based moves (damage = (atk_stat * atk_buf_of_move) / target_def)
    var moveIndex = getItemIndex(lastChoice);
    var isAtk = isAttack(moveIndex);
    var damageAmount = 0;
    updateLog(player.get('username'), lastChoice);
    if (isAttack && items[moveIndex].atk_buf == null) {
        console.log(enemyIndex);
        damageAmount = (player.get('atk'))/(enemies[enemyIndex].def) * baseAtkDamage;
        console.log(damageAmount); 
        enemies[enemyIndex].hp -= damageAmount;
        updateHealth(enemyIndex);
    }
    else if (isAtk && items[moveIndex].atk_buf != null) {
        damageAmount = (items[moveIndex].atk_buf * player.get('atk'))/(enemies[enemyIndex].def) * baseAtkDamage;
        console.log(damageAmount);
        enemies[enemyIndex].hp -= damageAmount;
        updateHealth(enemyIndex);
    }

    //Applying buffs to self
    else if (!isAtk && items[moveIndex].hp_buff != null && items[moveIndex].hp_buff != 0) {
        if (player.get('hp') + items[moveIndex].hp_buff < maxPlayerHealth) {
            player.set('hp',player.get('hp') + items[moveIndex].hp_buff);
        }
        else {
            player.set('hp', maxPlayerHealth);
        }
    }
    else if (!isAtk && items[enemyIndex].atk_buff != null && items[moveIndex].atk_buff != 0) {
        player.set('atk', items[moveIndex].atk_buff);
    }
    else if (!isAtk && items[enemyIndex].def_buff != null && items[moveIndex].def_buff != 0) {
        player.set('def', items[moveIndex].def_buff);
    }
}

//enemiesTurn()
//Iterates through the enemy array and lets each take their turn
function enemiesTurn() {
    var choice = 0;
    var moveIndex = 0;
    var isAtk = 0;
    var damageAmount = 0;
    for (var i = 0; i < enemies.length; i++) {
        //Skips turn if dead
        if (enemies[i].hp > 0) {
            //Getting random move choice for enemy
            choice = Math.floor(Math.random() * enemies[i].moves.length);
            moveIndex = getItemIndex(enemies[i].moves[choice]);
            isAtk = isAttack(moveIndex);
            
            updateLog(enemies[i].name, enemies[i].moves[choice]);
            //Attack based moves (damage = (atk_stat * atk_buf_of_move) / target_def)
            if (isAtk && items[moveIndex].atk_buf == null) {
                damageAmount = enemies[i].atk/(player.get('def')) * baseAtkDamage;
                console.log(damageAmount); 
                player.set('hp', player.get('hp') - damageAmount);
                updateHealth(-1);
            }
            else if (isAtk && items[moveIndex].atk_buf != null) {
                damageAmount = (items[moveIndex].atk_buf * enemies[i].atk)/(player.get('def')) * baseAtkDamage;
                console.log(damageAmount);
                player.set('hp', player.get('hp') - damageAmount);
                updateHealth(-1);
            }
            
            //Applying buffs to self
            else if (!isAtk && items[moveIndex].hp_buff != null && items[moveIndex].hp_buff != 0) {
                if (player.get('hp') + items[moveIndex].hp_buff < maxPlayerHealth) {
                    player.set('hp',player.get('hp') + items[moveIndex].hp_buff);
                }
                else {
                    player.set('hp', maxPlayerHealth);
                }
            }
            else if (!isAtk && items[moveIndex].atk_buff != null && items[moveIndex].atk_buff != 0) {
                player.set('atk', items[moveIndex].atk_buff);
            }
            else if (!isAtk && items[moveIndex].def_buff != null && items[moveIndex].def_buff != 0) {
                player.set('def', items[moveIndex].def_buff);
            }
        }
    }
}

//displayEnemies()
//Displays the enemies to fight
function displayEnemies() {
    var enemyIconPosition = document.getElementById('characters');
    for (var i = 0; i < enemies.length; i++) {
        enemyIconPosition.innerHTML += '<div class="col" id="' + enemies[i].name + '"> <div class="row name">' + enemies[i].name + '</div><div class="row" id="' + enemies[i].name + ' HP">' +
        enemies[i].hp + "/" + enemies[i].hp + '</div> <div class="row"> <div class = "p-10"> <image src="' + enemies[i].icon + 
            '" class="float-start"> <break> </div> </div> </div>';
    }
}

//updateHealth
//Updates the health of player and enemies and removes sprites as health drops below 0
function updateHealth(index) {
    var htmlId = "";
    var hpPosition = "";
    
    //Updating enemy health
    if (index >= 0) {
        htmlId = enemies[index].name + ' HP';
        hpPosition = document.getElementById(htmlId);
        hpPosition.innerHTML = enemies[index].hp + "/" + enemyMaxHps[index];
        //Removing sprite of dead enemy
        if (enemies[index].hp < 0) {
            htmlId = enemies[index].name;
            document.getElementById(htmlId).innerHTML = "";
        }
    }
    //Updating player health
    else {
        htmlId = 'playerHP';
        hpPosition = document.getElementById(htmlId);
        hpPosition.innerHTML = player.get('hp') + "/" + maxPlayerHealth;
    }
}

//getItemIndex
//Gets the index of the move/item from the items array to get stats of item/move
function getItemIndex(itemName) {
    for (var i = 0; i < items.length; i++) {
        if (items[i].name == itemName) {
            console.log("Value is " + i);
            return i;
        }
    }
    console.log("getItemIndex(): Didn't find value");
    return -1;
}

//isAttack
//Checks if a move is an attack or not
function isAttack(index) {
    console.log(items[index].atk);
    if (items[index].atk > 0) {
        return true;
    }
    else {
        return false;
    }
}

//checkWinOrLoss()
//Returns 1 for win, 0 for loss, -1 for still going
function checkWinOrLoss() {
    var enemiesDead = true;
    for (var i = 0; i < enemies.length; i++) {
        if (enemies[i].hp > 0) {
            enemiesDead = false;
            i = enemies.length;
        }
    }
    if (enemiesDead) {
        return 1;
    }

    else if (player.get('hp') <= 0) {
        return 0;
    }
    
    else {
        return -1;
    }
}

function updateLog(name, move) {
    logPosition = document.getElementById("log");
    logPosition.innerHTML += '<li>' + name + ' used ' + move + "</li>";
}

function generateEndScreen(playerWon) { 
    var game = document.getElementById('game');
    game.innerHTML += '<div class="container px-5">';
    if (!playerWon) {
        game.innerHTML += '<div class="row justify-content-center"> <div class = "col-4 align-self-center game-condition">You Have Fallen </div></div>';
        game.innerHTML += '<div class="row justify-content-center"> <div class = "col-4 align-self-center align-content-center">';
        game.innerHTML += '<div class="row justify-content-center"><div class="col-4 endScreen text-center align-self-center">' +
                          '<form action="returnToMap" method="POST"><div class="mb-3">' +
                          '<input type="hidden" class="form-control" name="winCondition" value="0"></div>' + '<button class ="returnButton">Return to the Map</button></form></div></div></div>';
    }
    else {
        game.innerHTML += '<div class="row justify-content-center"><div class="col-4 align-self-center game-condition"> You Have Ascended to Victory </div></div>';
        game.innerHTML += '<div class="row justify-content-center"> <div class="col-4 endScreen align-self-center"> <div class="dropsTitle"> Spoils of Battle </div> <ul id="drops"> ';
        game.innerHTML += '<div class="row justify-content-center"><div class="col-4 endScreen text-center align-self-center">' +
                          '<form action="returnToMap" method="POST"><div class="mb-3">' +
                          '<input type="hidden" class="form-control" name="winCondition" value="1"></div>' + '<button class ="returnButton">Return to the Map</button></form></div></div></div>';
        var drops = document.getElementById('drops');
        for (var i = 0; i < 3; i++) {
            drops.innerHTML += '<li> Item ' + i +  '</li>';
        }
    }
} 