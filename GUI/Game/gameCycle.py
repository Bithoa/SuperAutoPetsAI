import copy
import random


import GUI.Pets.petClass as PETS
import GUI.Game.player as PLAYER


#TODO
#- add in the events for each type of ability proc
def battlePhase(p1, p2):
    team1= copy.deepcopy(p1)
    petnum1=0
    for x in team1:
        if x is not None:
            petnum1 = petnum1 + 1
    team2= copy.deepcopy(p2)
    petnum2=0
    for y in team2:
        if y is not None:
            petnum2 = petnum2 + 1

    #beginning of battle effects


    #battle cycle continues until one team runs out of pets
    while petnum1 != 0 and petnum2 != 0:

        #finds the foremost pet in each party
        team1First= None
        for x in team1:
            if x is not None:
                team1First=x

        team2First = None
        for y in team2:
            if y is not None:
                team2First = y


        #they attack eachother simultaneously
        team1First.damage(team2First.attack + team2First.temp_attack)
        team2First.damage(team1First.attack + team1First.temp_attack)

        cleared=clearCarcasses(p1,p2)
        petnum1= petnum1 - cleared[0]
        petnum2= petnum2 - cleared[1]

    #clearing off the temp values for both teams
    for z in p1:
        z.temp_attack=0
        z.temp_health=0

    for q in p2:
        q.temp_attack=0
        q.temp_health=0

    if petnum2 == 0 and petnum1 == 0:
        return ["draw", "draw"]
    elif petnum2 == 0:
        return ["win", "lose"]
    else:
        return ["lose", "win"]


#clears our all of the pets that have 0 health
#returns number of pets removed from each side
#TODO Implement the Faint event here
def clearCarcasses(t1, t2):
    cleared= [0,0]
    for x in range(len(t1)):
        if t1[x] is not None and t1[x].health <= 0:
            #Put Faint here
            t1[x]= None
            cleared[0]= cleared[0]+1


    for x in range(len(t2)):
        if t2[x] is not None and t2[x].health <= 0:
            #Put Faint here
            t2[x]= None
            cleared[1] = cleared[1] + 1

    return cleared

def clearPlayerCarcassess(players):

    for x in range(len(players)):
        if players[x].lives<= 0:
            players.pop(x)





def draftPhasePlayer(roundnumber, player):
    board= draftBoard(roundnumber,player)
    finished= False
    print("Why hello there " + player.name)

    while finished is False:

        board.render()

        choice= input("What would you like to do? (draft/sell/freeze/thaw/merge/reroll/nothing)")

        if choice == "draft":
            if board.money<3:
                print("You do not have sufficient resources to do this. Please try again.")
                continue

            draftChoice= input("Which victim would you like to buy? (give index)")
            draftGoal= input("And where would you like to put said victim? (give index)")

            board.draftPet(int(draftChoice), int(draftGoal))
        elif choice == "sell":
            sellChoice= input("Which pet would you like to so callously sell? (give index)")

            board.sell(int(sellChoice))

        elif choice == "freeze":
            freezeChoice= input("Which pet would you like to mercilessly freeze? (give index)")

            board.freezePet(int(freezeChoice))

        elif choice == "thaw":
            thawChoice= input("Which pet would you like to mercifully thaw? (give index)")

            board.thawPet(int(thawChoice))

        elif choice == "merge":
            mergee= input("Which would you like to sacrifice as food? (give index)")
            merger= input("Which would you like to feed the blood of its brethren? (give index)")

            board.mergePetLineup(int(mergee), int(merger))

        elif choice == "reroll":

            board.reroll()

        elif choice == "nothing":
            finishChoice = input("Would you like to finish you turn? (y/n)")
            if finishChoice == "Y":
                finished = True

        else:
            print("I am sorry but this is not a recognized command you incompetent. Try again.")
            continue

        finishChoice= input("Would you like to finish you turn? (y/n)")
        if finishChoice == "Y":
            finished = True



def gameCycle(playerNum, botNum):
    players=[]

    for pnum in range(playerNum):
        players.append(PLAYER.player("team"+str(pnum), [None] * 5))

    roundnumber=0

    while len(players) != 0:
        roundnumber= roundnumber + 1
        print("Round :" + str(roundnumber))

        #drafting phase
        for drafter in players:
            draftPhasePlayer(roundnumber, drafter)

        #battle phase
        for i in range(len(players)//2):
            results= battlePhase(players[2*i].team, players[2*i + 1].team)
            if results[0] == "win":
                players[2 * i].wins= players[2 * i].wins + 1
                players[2 * i].last_battle= True

                players[2 * i + 1].lives= players[2*i + 1].lives - (roundnumber//3 +1)
                players[2 * i + 1].last_battle= False

            elif results[0] == "lose":
                players[2 * i+1].wins = players[2 * i+1].wins + 1
                players[2 * i+1].last_battle = True

                players[2 * i].lives = players[2 * i].lives - (roundnumber // 3 + 1)
                players[2 * i].last_battle = False

            else:
                players[2 * i + 1].last_battle = True
                players[2 * i].last_battle = True

        clearPlayerCarcassess(players)








class draftBoard:

    def __init__(self, round, player):
        self.round= round
        self.player=player
        self.petLineup= [None] * min(3+round//5, 5)
        self.frozen_pets= player.frozen_pets
        self.frozen_items= player.frozen_items
        self.itemLineup= [None] * 3
        self.money= 10
        self.tier= ((round-1)//2)+1
        self.catcount = 0


        self.petFill()

    #just team and lineup for now
    def render(self):
        teamLine=""
        for x in self.player.team:
            if x is not None:
                teamLine= teamLine + "| LVL."+ str(x.level) + "." + str(x.exp) + " " + x.type + "("+ str(x.attack+x.temp_attack) + "/" + str(x.health+x.temp_health) + ") "
            else:
                teamLine= teamLine + "|        "
        lineup= ""
        for y in self.petLineup:
            lineup = lineup + "| " + y.type + "(" + str(y.attack + y.temp_attack) + "/" + str(y.health + y.temp_health) + ") "

        print(teamLine + "|")
        print(lineup + "|")

    #frozen is a list of the indices of the shop that are frozen
    def petFill(self):
        index=0
        for ice in self.player.frozen_pets:
            self.petLineup[index]=ice
            index= index + 1

        while index < len(self.petLineup):
            self.petLineup[index]= self.genPet()
            index=index + 1


    def genPet(self):

        pool=PETS.Tier1.keys()
        for x in range(self.tier):

            if x + 1 == 2:
                pool = pool + PETS.Tier2.keys()
            elif x + 1 == 3:
                pool = pool + PETS.Tier3.keys()
            elif x + 1 == 4:
                pool = pool + PETS.Tier4.keys()
            elif x + 1 == 5:
                pool = pool + PETS.Tier5.keys()
            elif x + 1 == 6:
                pool = pool + PETS.Tier6.keys()

        pool= list(pool)
        return PETS.Pet(pool[random.randint(0, len(pool)-1)], 1, self.player)


    #will autp merge if there is a pet at the index that is the same type
    def draftPet(self, lineup_index, team_index):
        self.money= self.money - 3
        drafted= self.petLineup[lineup_index]
        goal= self.player.team[team_index]

        if goal is None:
            self.player.team[team_index] = drafted
            self.petLineup[lineup_index] = None
        elif goal.type is drafted.type:

            self.player.team[team_index].exp = drafted.exp + 1 + goal.exp
            self.petLineup[lineup_index] = None
            self.player.team[team_index].level = 1 + (self.player.team[team_index].exp + 1 // 2)



    #merges index one -->> into index 2
    #assumes that the two pets are the same type
    #takes care of level-up as well
    def mergePetLineup(self, index1, index2):

        pet1= self.player.team[index1]
        pet2= self.player.team[index2]

        self.player.team[index2].exp= pet2.exp + 1 + pet1.exp
        self.player.team[index1]= None
        self.player.team[index2].level= 1 + (self.player.team[index2].exp- 1 // 2)







    #def buyItem(self):

    #the input "mapping" should be a string consisting of the numbers 0,1,2,3,4, and 5. These number correspond to the
    # indices in the previous ordering, and the order of them in the string determines the new ordering
    def petOrdering(self, mapping):
        neworder= [None] * len(self.player.team)
        index=0
        for x in mapping:
            neworder[index]=  self.player.team[int(x)]
            index= index + 1

        self.player.team=neworder


    def freezePet(self, index):
        self.player.frozen_pets.add(self.petLineup[index])

    def thawPet(self, index):
        self.player.frozen_pets.remove(self.petLineup[index])


    #def freezeItem(self):

    def reroll(self):
        self.money= self.money - 1
        self.petFill()


    def sell(self, index):
        self.money= self.money + self.player.team[index].level
        self.player.team[index]= None

    #AI functions

    #def step(self):

    #def reset(self):

    #def action_space(self):



