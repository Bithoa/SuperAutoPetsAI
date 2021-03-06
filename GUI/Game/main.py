"""

Runs best with CUDA enabled

"""



import GUI.Game.gameCycle as GAME
import GUI.Pets.petClass as PETS
import GUI.Game.player as PLAYER



import GUI.Game.AI as AI
import torch
import torchvision
import torchaudio
from pathlib import Path
import random, datetime, os, copy


PATH=""


print("Hello, and welcome to our game!")
print("All of the commands should be zero indexed, with the first slot being the leftmost on the console")
saved= input("Would you like to run bots on a saved model?(y/n)")

bot_num= int(input("How many bots would you like to play with?"))
player_num= int(input("How many players would you like to play with?"))
ep_num=int(input("How many episodes would you like to do?"))

use_cuda = torch.cuda.is_available()
print(f"Using CUDA: {use_cuda}")
#print(torch.cuda.current_device())

save_dir = Path("checkpoints") / datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
save_dir.mkdir(parents=True)

RoboJenkins = AI.agent(state_dim=(None, 4, 16), action_dim=67, save_dir=save_dir)
if saved == "y":

    RoboJenkins.net.online.load_state_dict(torch.load(PATH))
    RoboJenkins.net.online.eval()
    RoboJenkins.net.target.load_state_dict(torch.load(PATH))
    RoboJenkins.net.target.eval()

PaulBunyan = AI.MetricLogger(save_dir)

for x in range(ep_num):
    winner=GAME.gameCycle(player_num, bot_num, RoboJenkins, PaulBunyan)

    print("The winner waaaasssssss ....... "+ winner.name+"!!!!!")

    PaulBunyan.record(episode=x, epsilon=RoboJenkins.exploration_rate, step=RoboJenkins.curr_step)

print("All done!")

#Test
"""
x= ['a','b','c']
r=['t', 'f', x]
b=x
b.append('z')
print(r)


player= PLAYER.player("tester", [None]*5, False)
player2= PLAYER.player("tester2", [None]*5, False)
team1=[PETS.Pet("Pig", 1, player), None, None, PETS.Pet("Fish", 1, player), PETS.Pet("Mosquito", 1, player)]
team2=[PETS.Pet("Sloth", 1, player), PETS.Pet("Sloth", 1, player), PETS.Pet("Mosquito", 1, player), None, None]
player.team=team1
player2.team=team2
ans=GAME.battlePhase( team1, team2)
print(ans[0]+"|"+ans[1])

sample= AI.environment(GAME.draftBoard(3,player),player)

for x in sample.state:
    print(x)

"""