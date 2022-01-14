
#TODO
#- make multiple maps from the names of units to their health, attack, and effect
#- make a function for each pet ability
#- make sure to trigger other abilites that may be triggered from the pet ability(like a damage ability would trigger a hurt ability)

Tier1={"ant" : [2,1],
       "pig"}
Tier2=

class Pet:
    def __init__(self, type, level, player):
        self.type= type
        #self.pipNum= pipNum
        self.level= level
        self.exp=0
        self.health=
        self.temp_health=
        self.attack=
        self.temp_attack=
        self.damage= 0
        self.item= None
        self.effect=




    def effect(self):

    # This should be the general input to the effect functions for every pet
    # (the self-player object, the enemy player objec, and the draftboard)
    #You can also assume that the function will be used at the exact right time it is supposed to
    def pig(self, team, enemy, draftboard):

        if self.level== 1:
            draftboard.money += 1
        elif self.level==2:
            draftboard.money += 2
        else:
            draftboard.money += 3



    def ant(self):



    def cricket(self):



    #account for maximum team size, and positioning
    def summon(self, index, ):


