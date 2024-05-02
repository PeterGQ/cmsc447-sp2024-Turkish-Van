from login import get_KDR, get_item_info_from_db, loadPlayer, current_player_data
import sqlite3


#When the kills are greater than 0, and the deaths are greater than 0
def testNormalCaseGetKDR():
    kills = 5
    deaths = 2
    kdr = get_KDR(kills, deaths)
    if (kdr == (kills/deaths)):
        return True
    else:
        return False
    
#When the kills are greater than 0, and the deaths are equal to 0
def testEdgeCase1GetKDR():
    kills = 5
    deaths = 0
    kdr = get_KDR(kills, deaths)
    if (kdr == (kills*1.1)):
        return True
    else:
        return False
    
#When the kills are equal to 0, and the deaths are equal to 0
def testEdgeCase2GetKDR():
    kills = 0
    deaths = 0
    kdr = get_KDR(kills, deaths)
    if (kdr == (0)):
        return True
    else:
        return False

#When the item asked for is in the database
def testNormalCaseGetItemInfoDromDB():
    image_id = "Herbal Tonic"
    result = get_item_info_from_db(image_id)
    if (result[0] == "Restores 15 HP"):
        return True
    else:
        return False

#When the item asked for is not in the database
def testErrorCaseGetItemInfoDromDB():
    image_id = "Jade"
    result = get_item_info_from_db(image_id)
    if (result == None):
        return True
    else:
        return False

#When the player indicated is in the database
def testNormalCaseLoadPlayer():
    loadPlayer("Tester")
    if (current_player_data['username'] == "Tester" and current_player_data['hp'] == 100 and current_player_data['atk'] == 1 and current_player_data['def'] == 1 and current_player_data['currency'] == 180 
         and current_player_data['kills'] == 13 and current_player_data['deaths'] == 0 and current_player_data['wave'] == 5 and current_player_data['inventory'] != None and current_player_data['moves'] != None):
        return True
    else:
        return False

##When the player indicated is in the database
def testErrorCaseLoadPlayer():
    current_player_data = None
    loadPlayer("hi")
    if (current_player_data == None):
        return True
    else:
        return False

def testNormalCase2GetEnemiesForWave():
    return False

if __name__ == "__main__":
    if (testNormalCaseGetKDR()):
        print("Normal case for get_KDR() succeeded.")
    else:
        print("Normal case for get_KDR() failed.")
    if (testEdgeCase1GetKDR()):
        print("Edge case 1 for get_KDR() succeeded.")
    else:
        print("Edge case 1 for get_KDR() failed.")
    if (testEdgeCase2GetKDR()):
        print("Edge case 2 for get_KDR() succeeded.")
    else:
        print("Edge case 2 for get_KDR() failed.")
    if (testNormalCaseGetItemInfoDromDB()):
        print("Normal case for get_item_info_from_db() succeeded.")
    else:
        print("Normal case for get_item_info_from_db() failed.")
    if (testErrorCaseGetItemInfoDromDB()):
        print("Error case for get_item_info_from_db() succeeded.")
    else:
        print("Error case for get_item_info_from_db() failed.")
    if (testNormalCaseLoadPlayer()):
        print("Normal case for loadPlayer() succeeded.")
    else:
        print("Normal case for loadPlayer() failed.")
    if (testErrorCaseLoadPlayer()):
        print("Error case for loadPlayer() succeeded.")
    else:
        print("Error case for loadPlayer() failed.")
    if (testNormalCaseLoadPlayer()):
        print("Normal case for loadPlayer() succeeded.")
    else:
        print("Normal case for loadPlayer() failed.")
    if (testErrorCaseLoadPlayer()):
        print("Error case for loadPlayer() succeeded.")
    else:
        print("Error case for loadPlayer() failed.")
    
    
    