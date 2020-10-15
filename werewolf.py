from characters import *
import random
import time

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
    elif (roles[i] == CHAR_WITCH):
        char = Witch(player=players[i], id=i+1)
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

#start logging
def startLogging(fname="gamelog.txt"):
    f = open(fname, "w")
    f.write("Game started")
    f.write('\n')
    f.close()

def nightLogging(days, fname="gamelog.txt"):
    f = open(fname, "a")
    f.write('NIGHT {} STARTED'.format(days))
    f.write('\n')
    f.close()

def eventLogging(action, subject, obj, fname="gamelog.txt"):
    f = open(fname, "a")
    f.write("{} {} {} -> {}".format(subject.name, subject.player, action, obj.player))
    f.write('\n')
    f.close()

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
        time.sleep(.100)

def characterTurn(charName):
    time.sleep(1)
    s = '\n======='
    s += charName
    s += '\'S TURN'
    s += '======='
    return s

def nightTimeStartText(days):
    time.sleep(1)
    s = '=============================== \n'
    s += 'NIGHT {} STARTED. CLOSE YOUR EYES \n'.format(days)
    s += '==============================='
    return s

def dayTimeStartText():
    time.sleep(1)
    s = '\n=============================== \n'
    s += 'LAST NIGHT, SOMETHING HAPPENED \n'
    s += '===============================\n'
    return s

def printNightVictims():
    n = len(killedLastNight)
    s = '======='
    print(s, n, 'PEOPLE DEAD:', killedLastNight, s)
    time.sleep(1)

# def playerKilled(id):
#     charToKill = getCharacterById(id)
#     charToKill.killed()
#     for pltup in alivePlayersTuple:
#         if pltup[0] == id:
#             alivePlayersTuple.remove(pltup)
#     print(getCharacterById(id).info())

def validateIntInput(inp):
    r = 0
    try:
        r = int(inp)
    except:
        r = 0
    finally:
        return r

def isIdValid(id):
    return (id > 0 and id <= playersNum)

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
startLogging()
# printAliveCharacters()
while days <= 2:
    ################################ NIGHT TIME ################################
    
    updateAlivePlayersTuple()
    killedLastNight.clear()
    print(nightTimeStartText(days))
    nightLogging(days)
    
    if (days == 1):
        #TO-DO
        print('Cupid and others //')
        # playerKilled(5)
    
    if exist(CHAR_GUARD):
        guard = getCharacterByRole(CHAR_GUARD)
        print(characterTurn(CHAR_GUARD))
        printAliveCharacters()
        inp = input('Who do you want to protect? id = ')
        id = validateIntInput(inp)
        if isIdValid(id):
            protectedChar = getCharacterById(id)
            guard.skill(protectedChar)
            eventLogging(ACTION_PROTECT, guard, protectedChar)
    
    if count(TEAM_WOLF) > 0:
        print(characterTurn(CHAR_WOLF))
        printAliveCharacters()
        wolfpack = WolfPack(disabled=isWolfPackDisabled())
        inp = input('Who do you ALL want to kill? id = ')
        id = validateIntInput(inp)
        if isIdValid(id):            
            killedByWolfPack = getCharacterById(id)
            wolfpack.skill(killedByWolfPack)
            eventLogging(ACTION_KILL, wolfpack, killedByWolfPack)

    if exist(CHAR_WITCH):
        witch = getCharacterByRole(CHAR_WITCH)
        print(characterTurn(CHAR_WITCH))
        witch.skill(killedByWolfPack)
        if witch.kill > 0:
            printAliveCharacters()
            inp = input('Do you want to kill anyone? (press 0 to skip) id = ')
            id = validateIntInput(inp)
            if isIdValid(id):
                killedByWitch = getCharacterById(id)
                witch.skill_kill(killedByWitch)
        else:
            print('NO KILL POWER LEFT')
    
    if exist(CHAR_SEER):
        seer = getCharacterByRole(CHAR_SEER)
        print(characterTurn(CHAR_SEER))
        printAliveCharacters()
        inp = input('Who do you want to see through? id = ')
        id = validateIntInput(inp)
        if isIdValid(id):
            seenChar = getCharacterById(id)
            seer.skill(seenChar)
        # allPlayersStatus()
    
    ################################ DAY TIME ################################
    
    print(dayTimeStartText())
    printNightVictims()
    updateAlivePlayersTuple()
    printAliveCharacters()
    inp = input('Who do you ALL want to hang/kill? (press 0 to skip) id = ')
    id = validateIntInput(inp)
    if isIdValid(id):
        hangedChar = getCharacterById(id)
        hangedChar.killed()
    resetAfterDay()
    alivePlayersStatus()
    days += 1

#TO-DO NEXT:
#DEV CHARACTER CUPID
#DEV CHARACTER HUNTER
#LOG GAME INFO AFTER EVERY DAY TO ROLLBACK
#LOG GAME EVENTS TO EXPLAIN AT GAME END