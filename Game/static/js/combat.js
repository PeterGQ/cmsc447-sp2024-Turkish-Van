const baseAtkDamage = 20;
const maxPlayerHealth = 100;

var items;
var player = null;
var enemies;
var numKilled = 0;
var lastChoice = "";
var enemyMaxHps = [];
var lastingEffects; //Map to keep track of move durations
var cooldowns; //Map to keep track of move cooldowns per character 

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/*---------------------------------------------------------------------------------------
    GETTING DATA FROM BACKEND AND STARTUP STUFF
-----------------------------------------------------------------------------------------*/
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
    
    //Storing max hp to be printed later
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

function setUpCooldownsAndDurations() {
    lastingEffects = new Map();
    lastingEffects.set(player.get('username'), new Map());

    cooldowns = new Map();
    cooldowns.set(player.get('username'), new Map());


    for (var i = 0; i < enemies.length; i++) {
        lastingEffects.set(enemies[i].name, new Map());
        cooldowns.set(enemies[i].name, new Map());
    }
    console.log(lastingEffects);
    console.log(cooldowns);
}

/*---------------------------------------------------------------------------------------
    UPDATING INTERACTABLE UI ELEMENTS
-----------------------------------------------------------------------------------------*/

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
        document.getElementById('attack').style.color = "#7f7dab"
        document.getElementById('items').style.color = "#9290C3"
        for (var i = 0; i < player.get('moves').length; i++) {
            newChoices.innerHTML += '<li class="nav-item"><button class ="choice" id="'+ player.get('moves')[i] + '" onClick=\"getConfirmation(1, '+ i +')\">'
                + player.get('moves')[i] + '</button></li>';
        }
            
    }
    //Option for if they choose item, lists items they have
    else {
        newChoices.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Items </a> </li>');
        document.getElementById('items').style.color = "#7f7dab";
        document.getElementById('attack').style.color = "#9290C3";
        var i = 0;
        if (player.get("inventory").size > 0) {
            player.get("inventory").forEach((value, key) => {
                if (value > 0) {    
                    newChoices.innerHTML += '<li class="nav-item"><button class ="choice" id="' + key + '" onClick=\"getConfirmation(0, \''+ key +'\')\">' +
                        key + " x" + value + '</button></li>';
                }
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
        if (isAttack(lastChoiceIndex) && !cooldowns.get(player.get('username')).has(lastChoice)) {
            htmlElement.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Enemies </a> </li>');
            for (var i = 0; i < enemies.length; i++) {
                if (enemies[i].hp > 0) {
                    htmlElement.innerHTML += '<li class=\"nav-item\"><button class =\"choice\" id=\'attack' + i + '\' onClick="startTurn(' + i +')">' + enemies[i].name + '</button></li>';
                }
            }
        }
        else if (!cooldowns.get(player.get('username')).has(lastChoice)) {
            htmlElement.innerHTML = '<div class="confirm">' +
                                '<li class="nav-item"><button class ="choice" id=\'çonfirm\' onClick=\"startTurn(-1)\"> Confirm </button></li></div>';
        }
        //Printing confirm button to ensure you want to buff yourself
        else {
            htmlElement.innerHTML = '<div class="confirm">' +
                                '<div class ="choice" id=\'çonfirm\'> You have ' + cooldowns.get(player.get('username')).get(lastChoice) +' turn(s) until you can use that!</div>';
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


/*---------------------------------------------------------------------------------------
    GAME LOGIC
-----------------------------------------------------------------------------------------*/

//startTurn()
//Runs playerTurn and enemiesTurn
async function startTurn(enemyIndex) {
    document.getElementById('choices').innerHTML = "";
    document.getElementById('enemies').innerHTML = "";
    document.getElementById("log").innerHTML = "";
    await toggleUI();
    //Player goes first'
    await playerTurn(enemyIndex);
    //Enemies go in ascending order of list
    await enemiesTurn();
    await decrementDurationAndCooldown();
    var gameState = checkWinOrLoss();
        
    if (gameState == 0) {
        document.getElementById('game').innerHTML = "";
        generateEndScreen(gameState);
    }
    else if (gameState == 1) {
        document.getElementById('game').innerHTML = "";
        generateEndScreen(gameState);
    }
    else {
        await toggleUI();
    }
    
}

//playerTurn()
//Logic for player taking their turn
async function playerTurn(enemyIndex) {
    //Attack based moves (damage = (atk_stat * atk_buf_of_move) / target_def)
    var moveIndex = getItemIndex(lastChoice);
    var isAtk = isAttack(moveIndex);
    var damageAmount = 0;
    
    var isItm = isItem(lastChoice);
    
    updateLog(player.get('username'), lastChoice);
    if (isAtk) {
        console.log(enemyIndex);
        damageAmount = calculateAttack(player.get('atk'), items[moveIndex].atk, enemies[enemyIndex].def);
        enemies[enemyIndex].hp -= damageAmount;
        updateHealth(enemyIndex);
    }
    if (isItem) {
        if (player.get('inventory').get(lastChoice) > 0) {
            player.get('inventory').set(lastChoice, player.get('inventory').get(lastChoice) - 1);
        }
    }
    addDurationAndCooldown(moveIndex);
    await sleep(1000);
    console.log(player);
}

//enemiesTurn()
//Iterates through the enemy array and lets each take their turn
async function enemiesTurn() {
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
            if (isAtk) {
                damageAmount = calculateAttack(enemies[i].atk, items[moveIndex].atk, player.get('def'));
                player.set('hp', player.get('hp') - damageAmount);
                updateHealth(-1);
            }
            //Applying buffs to self
            addDurationAndCooldownEnemy(i, moveIndex, choice);
            await sleep(1000);
        }
    }
}
//calculateAttack()
//Returns damage value based on parameters
function calculateAttack(attackerAtk, moveAtk, targetDef) {
    return parseInt(((attackerAtk * moveAtk)/(targetDef)) * baseAtkDamage);
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

/*-------------------------------------------------------------------------------------------------
    HELPER FUNCTIONS
--------------------------------------------------------------------------------------------------*/

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
        if (enemies[index].hp <= 0) {
            htmlId = enemies[index].name;
            document.getElementById(htmlId).innerHTML = "";
            numKilled++;
        }
    }
    //Updating player health
    else {
        htmlId = 'playerHP';
        hpPosition = document.getElementById(htmlId);
        hpPosition.innerHTML = player.get('hp') + "/" + maxPlayerHealth;
    }
}
/*-------------------------------------------------------------------------------------------------
    HELPER FUNCTIONS
--------------------------------------------------------------------------------------------------*/

//getItemIndex
//Gets the index of the move/item from the items array to get stats of item/move
function getItemIndex(itemName) {
    for (var i = 0; i < items.length; i++) {
        if (items[i].name == itemName) {
            return i;
        }
    }
    console.log("getItemIndex(): Didn't find value");
    return -1;
}

//isAttack
//Checks if a move is an attack or not
function isAttack(index) {
    if (items[index].atk > 0) {
        return true;
    }
    else {
        return false;
    }
}

function isItem(name) {
    if (player.get('inventory').has(name)) {
        return true;
    }
    console.log("isItem(): " + false);
    return false;
}

function addDurationAndCooldown(moveIndex) {
    console.log(moveIndex);
    if (items[moveIndex].hp_buff != null && items[moveIndex].hp_buff > 0) {
        if ((player.get('hp') + items[moveIndex].hp_buff) < maxPlayerHealth) {
            player.set('hp', player.get('hp') + items[moveIndex].hp_buff);
        }
        else {
            player.set('hp', maxPlayerHealth);
        }
        updateHealth(-1);
        console.log("HP:" + player.get('hp'));
    }
    if (items[moveIndex].atk_buff != null && items[moveIndex].atk_buff > 0) {
            player.set('atk', player.get('atk') * items[moveIndex].atk_buff);
    }
    if (items[moveIndex].def_buff != null && items[moveIndex].def_buff > 0) {
        player.set('def', player.get('def') * items[moveIndex].def_buff);

    }
    if (items[moveIndex].duration != null && items[moveIndex].duration > 0 && items[moveIndex].duration != 100) {
        lastingEffects.get(player.get('username')).set(items[moveIndex].name, items[moveIndex].duration);
    }
    if (items[moveIndex].cooldown != null && items[moveIndex].cooldown > 0) {
        cooldowns.get(player.get('username')).set(items[moveIndex].name, items[moveIndex].cooldown);
    }
}

function addDurationAndCooldownEnemy(characterIndex, moveIndex, enemyOption) {
    //Applying item effects to the specified enemy
    if (items[moveIndex].hp_buff != null && items[moveIndex].hp_buff > 0) {
        if (enemies[characterIndex].hp + items[moveIndex].hp_buff < maxPlayerHealth) {
            enemies[characterIndex].hp = enemies[characterIndex].hp + items[moveIndex].hp_buff;
        }
        else {
            enemies[characterIndex].hp = enemyMaxHps[characterIndex];
        }
        updateHealth(characterIndex);
    }
    if (items[moveIndex].atk_buff != null && items[moveIndex].atk_buff > 0) {
        enemies[characterIndex].atk = enemies[characterIndex].atk * items[moveIndex].atk_buff;
    }
    if (items[moveIndex].def_buff != null && items[moveIndex].def_buff > 0) {
        enemies[characterIndex].def = enemies[characterIndex].def * items[moveIndex].def_buff;
    }
    if (items[moveIndex].duration != null && items[moveIndex].duration > 0 && items[moveIndex].duration != 100) {
        lastingEffects.get(enemies[characterIndex].name).set(items[moveIndex].name, items[moveIndex].duration);
    }

    if (items[moveIndex].cooldown != null && items[moveIndex].cooldown > 0) {
        cooldowns.get(enemies[characterIndex].name).set(items[moveIndex].name, items[moveIndex].cooldown);
        //Removing move from enemy's moves to prevent it from using it, will be added back later
        firstPartWithoutMove = enemies[characterIndex].moves.slice(0, enemyOption);
        secondPartWithoutMove = enemies[characterIndex].moves.slice(enemyOption + 1, enemies[characterIndex].moves.length);
        enemies[characterIndex].moves = firstPartWithoutMove.concat(secondPartWithoutMove);
        console.log(enemies);
    }
}

function decrementDurationAndCooldown() {
    //Iterating through players durations and cooldowns, decrementing and removing them
    cooldowns.get(player.get('username')).forEach((value, key) => {
        
        //Decrementing the cooldown and making it available when done
        cooldowns.get(player.get('username')).set(key, --value);
        if (value <= 0) {
            cooldowns.get(player.get('username')).delete(key);
        }
    });

    lastingEffects.get(player.get('username')).forEach((value, key) => {
        //Decrementing the duration and resetting bonuses when duration ends
        lastingEffects.get(player.get('username')).set(key, --value);
        if (value <= 0) {
            var itemIndex = getItemIndex(key);
            if (items[itemIndex].hp_buff != null && items[itemIndex].hp_buff > 0) {
                player.set('hp', player.get('hp') - items[itemIndex].hp_buff);
                updateHealth(characterIndex);
            }
            if (items[itemIndex].atk_buff != null && items[itemIndex].atk_buff > 0) {
                player.set('atk', player.get('atk') / items[itemIndex].atk_buff);
            }
            if (items[itemIndex].def_buff != null && items[itemIndex].def_buff > 0) {
                player.set('def', player.get('def') / items[itemIndex].def_buff);
            }
            lastingEffects.get(player.get('username')).delete(key);
            document.getElementById("log").innerHTML += '<li> Effects of ' + key + 
                        ' wore off for ' + player.get('username') + "</li>";
        }
    });

    //Iterating through enemy moves
    for (var i = 0; i < enemies.length; i++) {
        cooldowns.get(enemies[i].name).forEach((value, key) => {
            cooldowns.get(enemies[i].name).set(key, --value);
            if (value <= 0) {
                enemies[i].moves.push(key);
                cooldowns.get(enemies[i].name).delete(key);
            }
        });
        lastingEffects.get(enemies[i].name).forEach((value, key) => {
            lastingEffects.get(enemies[i].name).set(key, --value);
            if (value <= 0 || enemies[i].hp <= 0) {
                var itemIndex = getItemIndex(key);
                if (items[itemIndex].hp_buff != null && items[itemIndex.hp_buff] > 0) {
                    enemies[i].hp = enemies[i].hp - items[itemIndex].hp_buff;
                    updateHealth(characterIndex);
                }
                if (items[itemIndex].atk_buff != null && items[itemIndex].atk_buff > 0) {
                    enemies[i].atk = enemies[i].atk / items[itemIndex].atk_buff;
                }
                if (items[itemIndex].def_buff != null && items[itemIndex].def_buff > 0) {
                    enemies[i].def = enemies[i].def / items[itemIndex].def_buff;
                }

                lastingEffects.get(enemies[i].name).delete(key);
                if (enemies[i].hp > 0) {
                    document.getElementById("log").innerHTML += '<li> Effects of ' + key + 
                        ' wore off for ' + enemies[i].name + "</li>";
                }
            }
        });
    }
    console.log(lastingEffects);
    console.log(cooldowns);
}

function updateLog(name, move) {
    logPosition = document.getElementById("log");
    logPosition.innerHTML += '<li>' + name + ' used ' + move + "</li>";
}

function toggleUI() {
    actions = document.getElementById("actions");
    console.log(actions.style.display);
    if (actions.style.display == null || actions.style.display == "inherit") {
        actions.style.display = "none";
    }
    else {
        actions.style.display = "inherit";
    }
}

function generateEndScreen(playerWon) { 
    var game = document.getElementById('game');
    game.innerHTML += '<div class="container px-5">';
    if (!playerWon) {
        game.innerHTML += '<div class="row justify-content-center"> <div class = "col-4 align-self-center game-condition">You Have Fallen </div></div>';
        game.innerHTML += '<div class="row justify-content-center"> <div class = "col-4 align-self-center align-content-center">';
        game.innerHTML += '<div class="row justify-content-center"><div class="col-4 endScreen text-center align-self-center">' +
                            '<button class ="returnButton" onclick="leave(0)">Return to the Map</button></div></div></div>';
    }
    else {
        game.innerHTML += '<div class="row justify-content-center"><div class="col-4 align-self-center game-condition"> You Have Ascended to Victory </div></div>';
        game.innerHTML += '<div class="row justify-content-center"> <div class="col-4 endScreen align-self-center"> <div class="dropsTitle"> Spoils of Battle </div> <ul id="drops"> ';
        game.innerHTML += '<div class="row justify-content-center"><div class="col-4 endScreen text-center align-self-center">' +
                          '<button class ="returnButton" onclick="leave(1)">Return to the Map</button></div></div></div>';
        var drops = document.getElementById('drops');
        for (var i = 0; i < 3; i++) {
            drops.innerHTML += '<li> Item ' + i +  '</li>';
        }
    }
} 

//leave()
//Goes back to the map and updates the inventory
//winLossRun (win == 1, loss == 0, run == -1)
function leave(winLossRun) {
    if (winLossRun == -1) {
        var leaveConfirmed = confirm("Are you sure you want to run? You won't die, but you will lose all progress in the fight and any items you used.");
        if (!leaveConfirmed) {
            console.log("The player lost the will to fight."); // Log cancellation
            return; // Exit the function to avoid resetting the game
        }
    }
    console.log("Leaving combat")
    jsonibleInventory = []
    player.get('inventory').forEach((value, key) => {
        jsonibleInventory.push({'name': key, 'quantity': value});
        console.log(key);
    });
    console.log(JSON.stringify({condition: winLossRun, inventory: jsonibleInventory}))
    const requestData = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
        condition: winLossRun,
        kills: numKilled,
        inventory: jsonibleInventory}),
    };

  // Make the fetch request
  fetch('/returnToMap', requestData)
    .then(response => {
      if (response.ok) {
        window.location.href = '/returnToMap'
      }
      else {
        throw new Error('Error was not ok. Status: ' + response.status);
      }
    })
    .then(response => {
      
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
      // Handle errors
    });
}