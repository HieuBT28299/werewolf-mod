from characters import *
import random

#generate player list
players = list()
fhand = open('players.txt')
for line in fhand:
    pl = line.strip()
    players.append(pl)
fhand.close()
random.shuffle(players)
playersNum = len(players)

#get roles
roles = list()
fhand = open('config.txt')
for line in fhand:
    quantity = int(line.split()[1])
    for i in range(quantity):
        roles.append(line.split()[0])
print(roles)
fhand.close()

#match characters
characters = list()
for i in range(playersNum):
    if (roles[i] == CHAR_WOLF):
        char = Werewolf(player=players[i], id=i+1)
    elif (roles[i] == CHAR_VILLAGER):
        char = Villager(player=players[i], id=i+1)
    elif (roles[i] == CHAR_SEER):
        char = Seer(player=players[i], id=i+1)
    elif (roles[i] == CHAR_GUARD):
        char = Guard(player=players[i], id=i+1)
    characters.append(char)

#list of alive players
alivePlayersTuple = list()

#update list of alive players
def updateAlivePlayersTuple():
    alivePlayersTuple.clear()
    for char in characters:
        if char.alive:
            pltup = (char.id, char.player)
            alivePlayersTuple.append(pltup)


def teamStatus():
    s = TEAM_WOLF + ' ' + str(count(TEAM_WOLF))
    s += '\n'
    s += TEAM_HUMAN + ' ' + str(count(TEAM_HUMAN))
    return s

def count(team):
    count = 0
    for char in characters:
        if char.alive and char.team == team:
            count += 1
    return count

def allPlayersStatus():
    print(teamStatus())
    for char in characters:
        print(char.info())

def alivePlayersStatus():
    print(teamStatus())
    for char in characters:
        if char.alive:
            print(char.info())

def getCharacterByRole(charName):
    for char in characters:
        if char.name == charName:
            return char

def getCharacterById(id):
    return characters[id-1]

def exist(role):
    return role in roles

def printAliveCharacters():
    print('People alive:')
    for pltup in alivePlayersTuple:
        print(pltup[0], pltup[1])

def characterTurn(char):
    s = '======='
    s += char
    s += '\'S TURN'
    s += '======='
    return s

def nightTimeStartText(days):
    s = '=============================== \n'
    s += 'NIGHT {} STARTED. CLOSE YOUR EYES \n'.format(days)
    s += '==============================='
    return s

def dayTimeStartText():
    s = '=============================== \n'
    s += 'LAST NIGHT, SOMETHING HAPPENED \n'
    s += '==============================='
    return s

def printNightVictims():
    n = len(killedLastNight)
    s = '======='
    print(s, n, 'PEOPLE DEAD:', killedLastNight, s)

# def playerKilled(id):
#     charToKill = getCharacterById(id)
#     charToKill.killed()
#     for pltup in alivePlayersTuple:
#         if pltup[0] == id:
#             alivePlayersTuple.remove(pltup)
#     print(getCharacterById(id).info())

def validateIntInput(inp):
    r = -1
    try:
        r = int(inp)
    except:
        r = -1
    finally:
        return r

def resetAfterDay():
    for char in characters:
        char.resetAfterDay()

#Function supported
def isWolfPackDisabled():
    for char in characters:
        if char.team == TEAM_WOLF and char.disabled:
            return True
    return False


#start the game
days = 1
# printAliveCharacters()
while days <= 2:
    ################################ NIGHT TIME ################################
    
    updateAlivePlayersTuple()
    allPlayersStatus()
    killedLastNight.clear()
    print(nightTimeStartText(days))
    if (days == 1):
        print('Cupid and others //')
        # playerKilled(5)
    if exist(CHAR_GUARD):
        guard = getCharacterByRole(CHAR_GUARD)
        print(characterTurn(CHAR_GUARD))
        printAliveCharacters()
        inp = input('Who do you want to protect? id = ')
        id = validateIntInput(inp)
        protectedChar = getCharacterById(id)
        guard.skill(protectedChar)
        # allPlayersStatus()
    if count(TEAM_WOLF) > 0:
        print(characterTurn(CHAR_WOLF))
        printAliveCharacters()
        wolfpack = WolfPack(disabled=isWolfPackDisabled())
        inp = input('Who do you ALL want to kill? id = ')
        id = validateIntInput(inp)
        killedChar = getCharacterById(id)
        wolfpack.skill(killedChar)
        # allPlayersStatus()
    if exist(CHAR_SEER):
        seer = getCharacterByRole(CHAR_SEER)
        print(characterTurn(CHAR_SEER))
        printAliveCharacters()
        inp = input('Who do you want to see through? id = ')
        id = validateIntInput(inp)
        seenChar = getCharacterById(id)
        seer.skill(seenChar)
        # allPlayersStatus()
    
    ################################ DAY TIME ################################
    
    print(dayTimeStartText())
    printNightVictims()
    updateAlivePlayersTuple()
    printAliveCharacters()
    inp = input('Who do you ALL want to hang/kill? id = ')
    id = validateIntInput(inp)
    hangedChar = seenChar = getCharacterById(id)
    hangedChar.killed()
    resetAfterDay()
    alivePlayersStatus()
    days += 1