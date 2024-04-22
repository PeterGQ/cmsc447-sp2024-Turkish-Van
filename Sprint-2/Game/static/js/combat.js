var attacks;
var items;
var player;
var enemies;
var lastChoice = "";
//The parameter aOrI indicates item (0) or attack (1)
function importItems(data) {
    items = JSON.parse(data);
    console.log(items);
}

function importEnemies(data) {
    enemies = JSON.parse(data);
    console.log(enemies);
    enemyIconPosition = document.getElementById('characters');
    for (var i = 0; i < enemies.length; i++) {
        enemyIconPosition.innerHTML += '<div class="col" id="' + enemies[i].name + '"> <div class="row">' + enemies[i].name + '<div id="' + enemies[i].name + ' HP">' +
        enemies[i].hp + "/" + enemies[i].hp + '</div> <div class="row"> <div class = "p-10"> <image src="' + enemies[i].icon + 
            '" class="float-start"> <break> </div> </div> </div>';
    }
}

function importPlayer(data) {
    parsedJson = JSON.parse(data);
    //Converting playerData to map
    player = new Map(Object.entries(parsedJson));

    //Converting inventory to nested map
    inventory = new Map(Object.entries(player.get('inventory')));
    player.set('inventory', inventory);

    //console.log(player); //For debugging

    //Printing username and hp above player sprite
    document.getElementById("playerName").innerHTML = player.get('username');
    document.getElementById("playerHP").innerHTML = player.get('hp')+ "/100";
}

function getOptions(aOrI, playerData) {
    var moves = ['Slash', 'Defend', 'Deep Breath'];
    var newChoices = document.getElementById('choices');
    document.getElementById('enemies').innerHTML = "";
    newChoices.style.display = "inherit";
    lastChoice = ""
    if (aOrI == 1) {
        newChoices.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Attacks </a> </li>');
        for (var i = 0; i < moves.length; i++) {
            document.getElementById('attack').style.color = "#7f7dab"
            document.getElementById('items').style.color = "#9290C3"
            newChoices.innerHTML += '<li class="nav-item"><button class ="choice" id="'+ player.get('moves')[i] + '" onClick=\"getConfirmation(1, '+ i +')\">'
                + player.get('moves')[i] + '</button></li>';
        }
            
    }
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
function getConfirmation(aOrI, index) {
    var htmlElement = document.getElementById('enemies');
    htmlElement.style.display = "inherit";
    if(aOrI == 1) {
        document.getElementById(player.get("moves")[index]).style.color = "#7f7dab";
        if (lastChoice != "" && lastChoice != player.get("moves")[index]) {
            document.getElementById(lastChoice).style.color = "#9290C3";
        }
        lastChoice = player.get("moves")[index];
        htmlElement.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Enemies </a> </li>');
        for (var i = 0; i < enemies.length; i++) {
            htmlElement.innerHTML += '<li class=\"nav-item\"><button class =\"choice\" id=\'attack' + i + '\' onClick="startTurn(' + i +')">' + enemies[i].name + '</button></li>';
        }
    }
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

function startTurn(index) {
    //Player goes first
    //Enemies go in ascending order of list
}