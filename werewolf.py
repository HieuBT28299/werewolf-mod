from characters import *
import random

#generate player list
players = list()
alivePlayersTuple = list()
fhand = open('players.txt')
for line in fhand:
    pl = line.strip()
    players.append(pl)
fhand.close()
random.shuffle(players)
playersNum = len(players)
for i in range(playersNum):
    pltup = (i, players[i])
    alivePlayersTuple.append(pltup)
print(alivePlayersTuple)



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
        char = Werewolf(player=players[i])
    elif (roles[i] == CHAR_VILLAGER):
        char = Villager(player=players[i])
    elif (roles[i] == CHAR_SEER):
        char = Seer(player=players[i])
    elif (roles[i] == CHAR_GUARD):
        char = Guard(player=players[i])
    characters.append(char)

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

def getCharacter(charName):
    for char in characters:
        if char.name == charName:
            return char

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

def dayTimeStartText():
    s = 'LAST NIGHT, SOMETHING HAPPENED'
    return s

def playerKilled(id):
    charToKill = characters[id]
    charToKill.killed()
    for pltup in alivePlayersTuple:
        if pltup[0] == id:
            alivePlayersTuple.remove(pltup)
    print(characters[id].info())

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

#start the game
days = 1
# printAliveCharacters()
while days == 1:
    ################################ NIGHT TIME ################################
    
    allPlayersStatus()
    killedLastNight.clear()
    if (days == 1):
        print('Cupid and others //')
        playerKilled(5)
    if exist(CHAR_GUARD):
        guard = getCharacter(CHAR_GUARD)
        print(characterTurn(CHAR_GUARD))
        printAliveCharacters()
        inp = input('Who do you want to protect? id = ')
        id = validateIntInput(inp)
        protectedChar = characters[id]
        guard.skill(protectedChar)
        allPlayersStatus()
    if exist(CHAR_WOLF):
        print(characterTurn(CHAR_WOLF))
        printAliveCharacters()
        wolfpack = WolfPack()
        inp = input('Who do you ALL want to kill? id = ')
        id = validateIntInput(inp)
        killedChar = characters[id]
        wolfpack.skill(killedChar)
        allPlayersStatus()
    if exist(CHAR_SEER):
        seer = getCharacter(CHAR_SEER)
        print(characterTurn(CHAR_SEER))
        printAliveCharacters()
        inp = input('Who do you want to see through? id = ')
        id = validateIntInput(inp)
        seenChar = characters[id]
        seer.skill(seenChar)
        allPlayersStatus()
    
    ################################ DAY TIME ################################
    
    print(dayTimeStartText())
    print(killedLastNight)
    printAliveCharacters()
    inp = input('Who do you ALL want to hang/kill? id = ')
    id = validateIntInput(inp)
    hangedChar = seenChar = characters[id]
    hangedChar.killed()
    resetAfterDay()
    allPlayersStatus()
    days += 1