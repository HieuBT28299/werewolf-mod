from constants import *

killedLastNight = list()

class Character:
    id = 0
    name = None
    player = None
    team = TEAM_HUMAN
    power = 0
    lastContactedCharId = 0
    disabled = False
    alive = True
    protected = False

    def skill(self):
        print('This person has no skills')
        return
    def passive(self):
        print('This person has no passive abilities')
        return
    
    def killed(self):
        self.alive = False
        killedLastNight.append(self.player)
        # print(killedLastNight)

    def guardProtected(self):
        self.protected = True

    def teamShown(self):
        return self.team

    def resetAfterDay(self):
        self.protected = False

    def aliveStatus(self):
        if self.alive:
            return 'ALIVE'
        return 'DEAD'

    def protectedStatus(self):
        if self.protected:
            return 'PROTECTED'
        return ''

    def info(self):
        return (str(self.id) + ' ' + self.name + ' ' + self.player + ' ' + self.team + ' ' + self.aliveStatus() + ' ' + self.protectedStatus())

class Villager(Character):
    def __init__(self, player = None, id = 0):
        self.id = id
        self.name = CHAR_VILLAGER
        self.team = TEAM_HUMAN
        self.power = 1
        self.player = player

class Werewolf(Character):
    def __init__(self, player = None, id = 0):
        self.id = id
        self.name = CHAR_WOLF
        self.team = TEAM_WOLF
        self.power = -3
        self.player = player

class WolfPack(Character):
    def __init__(self, player = None, id = 0, disabled = False):
        self.id = id
        self.name = MISC_WOLFPACK
        self.team = TEAM_WOLF
        self.disabled = disabled
    
    def skill(self, char):
        killable = (not char.protected) and (not self.disabled)
        if (killable):
            char.killed()
            print(char.player, 'has been killed by the Wolves')

class Seer(Character):
    def __init__(self, player = None, id = 0):
        self.id = id
        self.name = CHAR_SEER
        self.team = TEAM_HUMAN
        self.power = 7
        self.player = player

    def skill(self, char):
        print(char.player, 'belongs to', char.teamShown())

class Guard(Character):
    def __init__(self, player = None, id = 0):
        self.id = id
        self.name = CHAR_GUARD
        self.team = TEAM_HUMAN
        self.power = 3
        self.player = player

    def skill(self, char):
        if not self.disabled:
            char.guardProtected()
            self.lastContactedCharId = char.id
            print(char.player, 'has been protected')