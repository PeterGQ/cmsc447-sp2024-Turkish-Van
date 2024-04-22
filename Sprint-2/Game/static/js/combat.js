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

    console.log(player)

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
        var lastChoiceIndex = getItemIndex(lastChoice);
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
    //Player goes first'
    playerTurn(enemyIndex)
    //Enemies go in ascending order of list
    enemiesTurn()
    document.getElementById('choices').innerHTML = "";
    document.getElementById('enemies').innerHTML = "";
}

//playerTurn()
//Logic for player taking their turn
function playerTurn(enemyIndex) {
    //Attack based moves (damage = (atk_stat * atk_buf_of_move) / target_def)
    var moveIndex = getItemIndex(lastChoice);
    var isAtk = isAttack(moveIndex);
    var damageAmount = 0;
    if (isAttack && items[moveIndex].atk_buf == null) {
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
        if (enemies[i].hp < 0) {
            return;
        }
        
        //Getting random move choice for enemy
        choice = Math.floor(Math.random() * enemies[i].moves.length);
        moveIndex = getItemIndex(enemies[i].moves[choice]);
        isAtk = isAttack(moveIndex);
        
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
        else if (!isAtk && items[enemyIndex].atk_buff != null && items[moveIndex].atk_buff != 0) {
            player.set('atk', items[moveIndex].atk_buff);
        }
        else if (!isAtk && items[enemyIndex].def_buff != null && items[moveIndex].def_buff != 0) {
            player.set('def', items[moveIndex].def_buff);
        }
    }
}

//displayEnemies()
//Displays the enemies to fight
function displayEnemies() {
    var enemyIconPosition = document.getElementById('characters');
    for (var i = 0; i < enemies.length; i++) {
        enemyIconPosition.innerHTML += '<div class="col" id="' + enemies[i].name + '"> <div class="row">' + enemies[i].name + '<div id="' + enemies[i].name + ' HP">' +
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
    if (items[index].atk_buf == null && items[index].def_buf == null && items[index].hp_buff == null) {
        return true;
    }
    else if (items[index].atk_buf != null && items[index].def_buf == null && items[index].hp_buff == null) {
        return true;
    }
    else {
        return false;
    }
}