
import random

#TODO
#- make multiple maps from the names of units to their health, attack, and effect
#- make a function for each pet ability
#- make sure to trigger other abilites that may be triggered from the pet ability(like a damage ability would trigger a hurt ability)


# Summons currently represented as [0,0]s, if this messes with the KO-detection
# we can summon them as [1,1]s, add whatever, then -1/-1
Tier1 = {"Ant" : [2,1], "Beaver" : [2,2], "Cricket" : [1,2], "Duck" : [1,2], "Fish" : [2,3], "Horse" : [2,1], "Mosquito" : [2,2], "Otter" : [1,2], "Pig" : [3,1], "Sloth" : [1,1]
       }
Tier2 = {"Crab" : [3,3], "Dodo" : [2,3], "Elephant" : [3,5], "Flamingo" : [3,1], "Hedgehog" : [3,2], "Peacock" : [1,5], "Shrimp" : [2,3], "Spider" : [2,2], "Swan" : [3,3]
       }
Tier3 = {"Dog" : [2,2], "Badger" : [5,4], "Blowfish" : [3,5], "Camel" : [2,5], "Giraffe" : [2,5], "Kangaroo" : [1,2], "Ox" : [1,4], "Rabbit" : [3,2], "Sheep" : [2,2], "Snail" : [2,2], "Turtle" : [1,2]
         }
Tier4 = {"Bison" : [6,6], "Deer" : [1,1], "Dolphin" : [4,6], "Hippo" : [4,7], "Penguin" : [1,2], "Rooster" : [5,3], "Skunk" : [3,6], "Squirrel" : [2,2], "Worm" : [2,2]
         }
Tier5 = {"Monkey" : [1,2], "Cow" : [4,6], "Crocodile" : [8,4], "Rhino" : [5,8], "Scorpion" : [1,1], "Seal" : [3,8], "Shark" : [4,4], "Turkey" : [3,4]
         }
Tier6 = {"Cat" : [4,5], "Boar" : [8,6], "Dragon" : [6,8], "Fly" : [5,5], "Gorilla" : [6,9], "Leopard" : [10,4], "Mammoth" : [3,10], "Snake" : [6,6]
         }
Summons = {"Zombie Cricket" : [0,0], "Bus" : [0,0], "Zombie Fly" : [0,0], "Chick" : [0,0], "Ram" : [0,0], "Bee" : [0,0]
           }

Masterlist = {"Ant" : [2,1], "Beaver" : [2,2], "Cricket" : [1,2], "Duck" : [1,2], "Fish" : [2,3], "Horse" : [2,1], "Mosquito" : [2,2], "Otter" : [1,2], "Pig" : [3,1], "Sloth" : [1,1], "Crab" : [3,3], "Dodo" : [2,3], "Elephant" : [3,5], "Flamingo" : [3,1], "Hedgehog" : [3,2], "Peacock" : [1,5], "Shrimp" : [2,3], "Spider" : [2,2], "Swan" : [3,3], "Dog" : [2,2], "Badger" : [5,4], "Blowfish" : [3,5], "Camel" : [2,5], "Giraffe" : [2,5], "Kangaroo" : [1,2], "Ox" : [1,4], "Rabbit" : [3,2], "Sheep" : [2,2], "Snail" : [2,2], "Turtle" : [1,2], "Bison" : [6,6], "Deer" : [1,1], "Dolphin" : [4,6], "Hippo" : [4,7], "Penguin" : [1,2], "Rooster" : [5,3], "Skunk" : [3,6], "Squirrel" : [2,2], "Worm" : [2,2], "Monkey" : [1,2], "Cow" : [4,6], "Crocodile" : [8,4], "Rhino" : [5,8], "Scorpion" : [1,1], "Seal" : [3,8], "Shark" : [4,4], "Turkey" : [3,4], "Cat" : [4,5], "Boar" : [8,6], "Dragon" : [6,8], "Fly" : [5,5], "Gorilla" : [6,9], "Leopard" : [10,4], "Mammoth" : [3,10], "Snake" : [6,6]
         }

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


# TIER 1s
    def ant(self, team, enemy, draftboard):

        # choosing x random teammates will need to be coded
        target = team.random(1)
        target.temp_attack += 2*self.level
        target.temp_health += self.level

    def beaver(self, team, enemy, draftboard):
        targets = team.random(2)
        target[1].health += self.level
        target[2].health += self.level

    def cricket(self, team, enemy, draftboard):
        # however we implement summon
        team.summon("Zombie Cricket", [self.level,self.level])

    def duck(self, team, enemy, draftboard):
        for pet in draftboard.petLineup:
            pet.health += self.level

    def fish(self, team, enemy, draftboard):
        for pet in team:
            pet.attack += level
            pet.health += level

    def horse(self, team, enemy, draftboard, target):
        # takes in a target
        target.temp_attack += self.level

    def mosquito(self, team, enemy, draftboard):
        # same as team.random but choosing from opponent's lineup
        targets = enemy.random(self.level)
        for target in targets:
            # however we implement dealing/taking damage
            target.take_damage(self.level)

    def otter(self, team, enemy, draftboard):
        target = team.random(1)
        target.attack += self.level
        target.health += self.level

    def pig(self, team, enemy, draftboard):
        draftboard.money += self.level

# TIER 2s
    def crab(self, team, enemy, draftboard):
        max_health = 0
        for pet in team:
            if pet.health > max_health:
                max_health = pet.health
        self.health = max_health

    def dodo(self, team, enemy, draftboard):
        # need a self.infront(x) method
        target = self.infront(1)
        target.temp_attack += (self.attack + self.temp_attack) // 2

    def elephant(self, team, enemy, draftboard):
        targets = self.behind(self.level)
        for target in targets:
            target.take_damage(1)

    def flamingo(self, team, enemy, draftboard):
        targets = self.behind(2)
        for target in targets:
            target.temp_attack += self.level
            target.temp_health += self.level

    def hedgehog(self, team, enemy, draftboard):
        for target in team.lineup:
            target.take_damage(2 * self.level)
        for target in enemy.lineup:
            target.take_damage(2 * self.level)

    def peacock(self, team, enemy, draftboard):
        self.temp_attack += (2 * self.level)

    def shrimp(self, team, enemy, draftboard):
        target = team.random(1)
        target.health += self.level

    def spider(self, team, enemy, draftboard):
        team.summon(random.choice(Tier3))

    def swan(self, team, enemy, draftboard):
        draftboard.money += self.level

# TIER 3s
    def dog(self, team, enemy, draftboard):
        attack_or_health = random.choice(["Attack","Health"])
        if attack_or_health == "Attack":
            self.attack += self.level
        else:
            self.health += self.level

    def badger(self, team, enemy, draftboard):
        # We'll need this too
        targets = self.adjacent()
        for target in targets:
            target.take_damage((self.attack + self.temp_attack) * self.level)

    def blowfish(self, team, enemy, draftboard):
        target = enemy.random(1)
        target.take_damage(2 * self.level)

    def camel(self, team, enemy, draftboard):
        target = self.behind(1)
        target.temp_attack += self.level
        target.temp_health += (2 * self.level)

    def giraffe(self, team, enemy, draftboard):
        targets = self.infront(self.level)
        for target in targets:
            target.attack += 1
            target.health += 1

    def kangaroo(self, team, enemy, draftboard):
        self.temp_attack += (2 * self.level)
        self.temp_health += (2 * self.level)

    def ox(self, team, enemy, draftboard):
        self.temp_attack += (2 * self.level)
        self.item = "Melon"

    def rabbit(self, team, enemy, draftboard):
        target = team.random(1)
        target.health += self.level

    def sheep(self, team, enemy, draftboard):
        team.summon("Ram", [2 * self.level,2 * self.level])
        team.summon("Ram", [2 * self.level,2 * self.level])

    def snail(self, team, enemy, draftboard):
        for target in team.lineup():
            target.attack += (2 * self.level)
            target.health += self.level

    def turtle(self, team, enemy, draftboard):
        targets = self.behind(self.level)
        for target in targets:
            target.item = "Melon"

# TIER 4s
    def bison(self, team, enemy, draftboard):
        self.attack += (2 * self.level)
        self.attack += (2 * self.level)

    def deer(self, team, enemy, draftboard):
        team.summon("Bus", [5 * self.level,5 * self.level])
        for pet in team.lineup():
            if pet.type == "Bus":
                pet.item = "Pepper"

    def dolphin(self, team, enemy, draftboard):
        lowest_health = 51
        target = None
        for pet in enemy.lineup():
            if pet.health + pet.temp_health < lowest_health:
                lowest_health = pet.health + pet.temp_health
                target = pet
        target.take_damage(5 * self.level)

    def hippo(self, team, enemy, draftboard):
        self.attack += (2 * self.level)
        self.health += (2 * self.level)

    def penguin(self, team, enemy, draftboard):
        for pet in team.lineup():
            if pet.level >= 2:
                pet.attack += self.level
                pet.health += self.level

    def rooster(self, team, enemy, draftboard):
        for i in range (self.level):
            team.summon("Chick", [(self.attack + self.temp_attack) // 2,1])

    def skunk(self, team, enemy, draftboard):
        highest_health = 0
        target = None
        for pet in enemy.lineup()
            if pet.health + pet.temp_health > highest_health:
                highest_health = pet.health + pet.temp_health
                target = pet
        if self.level == 3:
            target.health = 1
        else:
            target.health = highest_health//3*(3-self.level)

    def squirrel(self, team, enemy, draftboard):
        # We'll need something that lets us set the price for just these items
        draftboard.itemLineup.cost -= self.level

    def worm(self, team, enemy, draftboard):
        self.attack += self.level
        self.health += self.level

# TIER 5s
    def monkey(self, team, enemy, draftboard):
        # We'll need to pick the frontmost pet
        target = team.front()
        target.attack += 3
        target.health += 3

    def cow(self, team, enemy, draftboard):
        draftboard.itemLineup = ["Milk", "Milk"]

    def crocodile(self, team, enemy, draftboard):
        # We'll need to pick rearmost enemy pet
        target = enemy.rear()
        target.take_damage(8 * self.level)

    def rhino(self, team, enemy, draftboard):
        # We'll need to pick frontmost enemy pet
        target = enemy.front()
        target.take_damage(5 * self.level)

    def seal(self, team, enemy, draftboard):
        targets = team.random(2)
        for target in targets:
            target.attack += self.level
            target.health += self.level

    def shark(self, team, enemy, draftboard):
        self.attack += (2 * self.level)
        self.health += self.level

    def turkey(self, team, enemy, draftboard, target):
        # takes in target like horse
        target.attack += (3 * self.level)
        target.health += (3 * self.level)

# TIER 6s
    def cat(self, team, enemy, draftboard):
        # I'm guessing we'll put the multiplier in draftboard? Can be changed
        draftboard.catcount += self.level

    def boar(self, team, enemy, draftboard):
        self.attack += (2 * self.level)
        self.health += (2 * self.level)

    def dragon(self, team, enemy, draftboard):
        for target in team.lineup():
            target.attack += self.level
            target.health += self.level

    def fly(self, team, enemy, draftboard, count=3):
        if count > 0:
            team.summon("Zombie Fly", [5 * self.level,5 * self.level])
            count -= 1

    def gorilla(self, team, enemy, draftboard):
        self.item = "Coconut"

    def leopard(self, team, enemy, draftboard):
        targets = enemy.random(self.level)
        for target in targets:
            target.take_damage((self.attack + self.temp_attack) // 2)

    def mammoth(self, team, enemy, draftboard):
        for pet in team.lineup():
            pet.temp_attack += (2 * self.level)
            pet.temp_health += (2 * self.level)

    def snake(self, team, enemy, draftboard):
        target = enemy.random(1)
        target.take_damage(5 * self.level)



    #account for maximum team size, and positioning
    # I think this may do better under team
    def summon(self, index, team):


