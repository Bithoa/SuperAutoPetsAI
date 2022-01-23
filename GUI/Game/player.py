


class player:

    def __init__(self, name, team, robot):
        self.name= name
        self.team= team
        self.petNum=0
        #fill pet num
        for x in self.team:
            if x is not None:
                petNum=petNum + 1

        #humber of food can buffs used on animals


        self.cans= 0
        self.wins= 0
        self.lives= 10

        self.frozen_pets=set()

        self.frozen_items=set()

        #-1 is lost last battle, 0 for draw, 1 if won
        self.last_battle= 0

        #whether or not it is a bot
        self.bot=robot
        self.roboCache=[]
