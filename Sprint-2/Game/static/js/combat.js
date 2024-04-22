var attacks;
var items;
var player;
var enemies;
var lastChoice = "";
//The parameter aOrI indicates item (0) or attack (1)
function importItems(data) {
    items = JSON.parse(data);
}

function importEnemies(data) {
    enemies = JSON.parse(data);
    enemyIconPosition = document.getElementById('characters');
    for (var i = 0; i < enemies.length; i++) {
        enemyIconPosition.innerHTML += '<div class="col" id="' + enemies[i].name + '"> <div class="row">' + enemies[i].name + '<div id="' + enemies[i].name + ' HP">' +
        enemies[i].hp + "/" + enemies[i].hp + '</div> <div class="row"> <div class = "p-10"> <image src="' + enemies[i].icon + 
            '" class="float-start"> <break> </div> </div> </div>';
    }
}

function importPlayer(data) {
    player = JSON.parse(data);
    console.log(player);
    document.getElementById("playerName").innerHTML = player['username'];
    document.getElementById("playerHP").innerHTML = player['hp'] + "/100";
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
            newChoices.innerHTML += '<li class="nav-item"><button class ="choice" id="'+ moves[i] + '" onClick=\"getConfirmation(1, '+ i +')\">'
                + moves[i] + '</button></li>';
        }
            
    }
    else {
        newChoices.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Items </a> </li>');
        for (var i = 0; i < items.length; i++) {
            document.getElementById('items').style.color = "#7f7dab"
            document.getElementById('attack').style.color = "#9290C3"
            newChoices.innerHTML += '<li class="nav-item"><button class ="choice" id="' + items[i].name + '" onClick=\"getConfirmation(0, '+ i +')\">' +
                items[i].name + " x" + i + '</button></li>';
        }
    }
}
function getConfirmation(aOrI, index) {
    var moves = ['Slash', 'Defend', 'Deep Breath'];
    var items = [['Potion', 2], ['Bomb', 1], ['Throwing Knife', 7], ['Pokeball', 8], ['Spaghetti', 5], ['Bread', 9]]
    var enemiesTest = ['Goblin', 'Goblin Mage', 'Goblin Brute'];
    var htmlElement = document.getElementById('enemies');
    htmlElement.style.display = "inherit";
    if(aOrI == 1) {
        document.getElementById(moves[index]).style.color = "#7f7dab"
        if (lastChoice != "" && lastChoice != moves[index][0]) {
            document.getElementById(lastChoice).style.color = "#9290C3"
        }
        lastChoice = moves[index];
        htmlElement.innerHTML = ('<li> <a class = \"colTitle\" aria-current="page"> Enemies </a> </li>');
        for (var i = 0; i < enemies.length; i++) {
            htmlElement.innerHTML += '<li class=\"nav-item\"><button class =\"choice\" id=\'attack' + i + '\' onClick="startTurn(' + i +')">' + enemies[i].name + '</button></li>';
        }
    }
    else {
        document.getElementById(items[index][0]).style.color = "#7f7dab";
        if (lastChoice != "" && lastChoice != items[index][0]) {
            document.getElementById(lastChoice).style.color = "#9290C3";
        }
        lastChoice = items[index][0];
        htmlElement.innerHTML = '<div class="confirm">' +
                                '<li class="nav-item"><button class ="choice" id=\'çonfirm\' onClick=\"startTurn(-1)\"> Confirm </button></li></div>';
    }
}

function startTurn(index) {
    //Player goes first
    //Enemies go in ascending order of list
}