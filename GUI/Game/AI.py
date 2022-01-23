"""

Much of this code was learned from the Mario RL tutorial on PyTorch's documentation page. Various code snippets were
used to assist the implementation of our AI.

Sources:
https://pytorch.org/tutorials/intermediate/mario_rl_tutorial.html
"""

import torch

from torch import nn

import numpy as np
import time, datetime
import matplotlib.pyplot as plt
from pathlib import Path
from collections import deque
import random, datetime, os, copy

import GUI.Game.player as PLAYER
import GUI.Pets.petClass as PETS
import  GUI.Game.gameCycle as GAME

class environment():
    
    def __init__(self, board):
        self.board= board

        self.petKey={}
        val=0
        for x in PETS.Masterlist.keys():
            self.petKey[x]=val
            val= val + 1

        self.state=[]
        self.update_state()

    # turn the above variables into arrays of inputs to feed into the neural network
    def update_state(self):
        # array of pets in team
        petArray = []
        for x in self.board.player.team:
            if x is None:
                # input nonfactor pet that has an index outside the array of possibel pets
                petArray.append([len(self.petKey), 0, 0, 0])
            else:
                petArray.append([self.petKey[x.type], x.exp, x.health, x.attack])

        # array of pets in Lineup
        Lineup = []
        for z in self.board.petLineup:
            if z is None:
                # input nonfactor pet that has an index outside the array of possible pets
                Lineup.append([len(self.petKey), 0, 0, 0])
            else:
                Lineup.append([self.petKey[z.type], z.exp, z.health, z.attack])

        for t in range(5 - len(Lineup)):
            Lineup.append([len(self.petKey), 0, 0, 0])

        # array of pets frozen
        frozenPets = []
        for y in self.board.player.frozen_pets:
            frozenPets.append([self.petKey[y.type], y.exp, y.health, y.attack])

        for r in range(5 - len(frozenPets)):
            frozenPets.append([len(self.petKey), 0, 0, 0])

        # make a 2-d 4x16 array for a 2d convolutional neural network
        self.state = [[self.board.round, self.board.money, self.board.player.lives, self.board.player.wins]] + petArray + frozenPets + Lineup


    #converts numerical action input into an actual action on the board
    def step(self, action):
        actnum=action
        #draft portion
        if action>=0 and action<=24:
            self.board.draftPet(action//5, action % 5)

        # Sell portion
        elif action >= 25 and action <= 29:
            self.board.sell(action%5)

        # freeze portion
        elif action >= 30 and action <= 34:
            self.board.freezePet(action % 5)


        # Thaw portion
        elif action >= 35 and action <= 39:
            self.board.thawPet(action % 5)

        # Merge
        elif action >= 40 and action <= 64:
            actnum=actnum-40
            self.board.mergePetLineup(action // 5, action % 5)

        # Reroll
        elif action == 65:
            self.board.reroll()

        elif action==66:
            return self.state

        self.update_state()
        new_state= environment(self.board)

        return new_state.state



    #return true iff valid move
    def check_action(self, action):
        #draft portion
        actnum = action
        if action >= 0 and action <= 24:

            if self.board.money <3:
                return False
            elif self.board.petLineup[actnum//5] is None:
                return False
            elif self.board.player.team[action%5] is not None and self.board.player.team[action%5].type !=self.board.petLineup[actnum//5].type:
                return False
            else:
                return True
        #Sell portion
        elif action>=25 and action<=29:
            if self.board.player.team[action%5] is None:
                return False
            else:
                return True
        #freeze portion
        elif action>=30 and action<=34:
            if self.board.petLineup[action % 5] is None:
                return False
            else:
                return True

        #Thaw portion
        elif action>=35 and action<=39:
            if self.board.petLineup[action % 5] is None:
                return False
            else:
                return True

        #Merge
        elif action>=40 and action<=64:
            actnum = actnum - 40
            if self.board.player.team[actnum // 5] is None:
                return False
            elif self.board.player.team[action % 5] is None:
                return False
            elif self.board.player.team[action % 5].type != self.board.player.team[actnum // 5]:
                return False
            else:
                return True

        #Reroll
        elif action==65:
            if self.board.money<1:
                return False
            else:
                return True
        #end draft
        elif action==66:
            return True








class agent():

    def __init__(self, state_dim, action_dim, save_dir):
        self.state_dim=state_dim
        self.action_dim=action_dim
        self.save_dir=save_dir
        self.use_cuda = torch.cuda.is_available()

        #NN stuff
        self.net= agentNet(self.state_dim, self.action_dim).float()
        if self.use_cuda:
            self.net = self.net.to(device="cuda")

        self.exploration_rate = 1
        self.exploration_rate_decay = 0.99999975
        self.exploration_rate_min = 0.1
        self.curr_step = 0

        self.save_every = 10000

        #Cache objects
        self.memory= deque(maxlen= 100000)
        self.batch_size=32

        #policy modification
        self.gamma=0.9

        #model update
        self.optimizer= torch.optim.Adam(self.net.online.parameters(), lr=0.00025)
        self.loss_fn = torch.nn.SmoothL1Loss()

        #variables for controlling learnind and sync rates
        self.burnin = 1e4
        self.learn_every = 3
        self.sync_every = 1e4


    #the agents main method for acting in the environment
    def act(self, state, env):

        old_state = copy.deepcopy(state)
        #Exploring new options
        if np.random.rand() < self.exploration_rate:
            action_idx = np.random.randint(self.action_dim)
            while not env.check_action(action_idx):
                action_idx = np.random.randint(self.action_dim)



        #Relying on previous information
        else:

            if self.use_cuda:
                state= torch.tensor(state).cuda()
            else:
                state= torch.tensor(state)
            state= state.unsqueeze(0)
            state = state.unsqueeze(0)
            state = state.type(torch.float)
            #print(state)
            action_values= self.net(state, model="online")
            action_idx= torch.argmax(action_values, axis=1).item()

            trys=0
            while not env.check_action(action_idx):

                action_values = self.net(state, model="online")
                action_idx = torch.argmax(action_values, axis=1).item()

                #trys to do some learning to keep from making illegal moves
                self.cache(old_state, old_state, action_idx, -10, 0)
                q,loss= self.learn()
                #print("explore rate:"+ str(self.exploration_rate))
                # reduce exploring
                self.exploration_rate = self.exploration_rate * self.exploration_rate_decay
                self.exploration_rate = max(self.exploration_rate_min, self.exploration_rate)

                self.curr_step = self.curr_step + 1


                trys=trys+1
                #print("NN Legal move attempts:" +str(trys))
                #print(action_idx)


        #reduce exploring
        self.exploration_rate = self.exploration_rate * self.exploration_rate_decay
        self.exploration_rate = max(self.exploration_rate_min, self.exploration_rate)

        self.curr_step= self.curr_step + 1


        return action_idx

    #stores recent experience for later use
    def cache(self, state, next_state, action, reward, done):



        if self.use_cuda:
            state = torch.tensor(state).cuda()
            next_state = torch.tensor(next_state).cuda()
            action = torch.tensor([action]).cuda()
            reward = torch.tensor([reward]).cuda()
            done = torch.tensor([done]).cuda()
        else:
            state = torch.tensor(state)
            next_state = torch.tensor(next_state)
            action = torch.tensor([action])
            reward = torch.tensor([reward])
            done = torch.tensor([done])

        self.memory.append((state, next_state, action, reward, done,))

    #recall random experiences from memory
    def recall(self):
        batch= random.sample(self.memory, self.batch_size)
        state, next_state, action, reward, done = map(torch.stack, zip(*batch))
        return state, next_state, action.squeeze(), reward.squeeze(), done.squeeze()

    def td_estimate(self, state, action):

        current_Q= self.net(state.unsqueeze(1).float(), model="online")[
            np.arange(0, self.batch_size), action
        ]
        return  current_Q

    @torch.no_grad()
    def td_target(self, reward, next_state, done):
        next_state_Q= self.net(next_state.unsqueeze(1).float(), model="online")
        best_action= torch.argmax(next_state_Q, axis=1)
        next_Q= self.net(next_state.unsqueeze(1).float(), model="target")[
            np.arange(0, self.batch_size), best_action
        ]
        return (reward+ (1- done.float())* self.gamma * next_Q).float()


    def update_Q_online(self, td_estimate, td_target):
        loss = self.loss_fn(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def sync_Q_target(self):
        self.net.target.load_state_dict(self.net.online.state_dict())

    #stores the trained model for later use
    def save(self):
        save_path = (
                self.save_dir / f"agent_net_{int(self.curr_step // self.save_every)}.chkpt"
        )
        torch.save(
            dict(model=self.net.state_dict(), exploration_rate=self.exploration_rate),
            save_path,
        )
        print(f"agentNet saved to {save_path} at step {self.curr_step}")


    def learn(self):
        if self.curr_step % self.sync_every == 0:
            self.sync_Q_target()

        if self.curr_step % self.save_every == 0:
            self.save()

        if self.curr_step < self.burnin:
            return None, None

        if self.curr_step % self.learn_every != 0:
            return None, None


        state, next_state, action, reward, done = self.recall()

        #estimates from memory
        td_est = self.td_estimate(state, action)

        #finds the target from memory
        td_tgt = self.td_target(reward, next_state, done)

        #backpropogates
        loss = self.update_Q_online(td_est, td_tgt)

        return (td_est.mean().item(), loss)


class agentNet(nn.Module):
    def __init__(self, input_dim, output_dim):

        super().__init__()

        #the NN design
        self.online = nn.Sequential(
            nn.LazyConv2d( out_channels=32, kernel_size=3, stride=3),
            nn.ReLU(),
            nn.LazyConv2d(out_channels=64, kernel_size=1, stride=2),
            nn.ReLU(),
            nn.LazyConv2d(out_channels=64, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.LazyLinear(512),
            nn.ReLU(),
            nn.Linear(512, output_dim),
        )

        #keeps track of the NN locally
        self.target= nn.Sequential(
            nn.LazyConv2d( out_channels=32, kernel_size=3, stride=3),
            nn.ReLU(),
            nn.LazyConv2d(out_channels=64, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.LazyConv2d(out_channels=64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.LazyLinear(512),
            nn.ReLU(),
            nn.Linear(512, output_dim),
        )

        #turns off autograd to keep target static
        for p in self.target.parameters():
            p.requires_grad=False

    #progresses the model
    #shoudl not be used manually tho
    def forward(self, input, model):
        if model=="online":
            return self.online(input)
        elif model == "target":
            return self.target(input)




class MetricLogger:
    def __init__(self, save_dir):
        self.save_log = save_dir / "log"
        with open(self.save_log, "w") as f:
            f.write(
                f"{'Episode':>8}{'Step':>8}{'Epsilon':>10}{'MeanReward':>15}"
                f"{'MeanLength':>15}{'MeanLoss':>15}{'MeanQValue':>15}"
                f"{'TimeDelta':>15}{'Time':>20}\n"
            )
        self.ep_rewards_plot = save_dir / "reward_plot.jpg"
        self.ep_lengths_plot = save_dir / "length_plot.jpg"
        self.ep_avg_losses_plot = save_dir / "loss_plot.jpg"
        self.ep_avg_qs_plot = save_dir / "q_plot.jpg"

        # History metrics
        self.ep_rewards = []
        self.ep_lengths = []
        self.ep_avg_losses = []
        self.ep_avg_qs = []

        # Moving averages, added for every call to record()
        self.moving_avg_ep_rewards = []
        self.moving_avg_ep_lengths = []
        self.moving_avg_ep_avg_losses = []
        self.moving_avg_ep_avg_qs = []

        # Current episode metric
        self.init_episode()

        # Timing
        self.record_time = time.time()

    def log_step(self, reward, loss, q):
        self.curr_ep_reward += reward
        self.curr_ep_length += 1
        if loss:
            self.curr_ep_loss += loss
            self.curr_ep_q += q
            self.curr_ep_loss_length += 1

    def log_episode(self):
        "Mark end of episode"
        self.ep_rewards.append(self.curr_ep_reward)
        self.ep_lengths.append(self.curr_ep_length)
        if self.curr_ep_loss_length == 0:
            ep_avg_loss = 0
            ep_avg_q = 0
        else:
            ep_avg_loss = np.round(self.curr_ep_loss / self.curr_ep_loss_length, 5)
            ep_avg_q = np.round(self.curr_ep_q / self.curr_ep_loss_length, 5)
        self.ep_avg_losses.append(ep_avg_loss)
        self.ep_avg_qs.append(ep_avg_q)

        self.init_episode()

    def init_episode(self):
        self.curr_ep_reward = 0.0
        self.curr_ep_length = 0
        self.curr_ep_loss = 0.0
        self.curr_ep_q = 0.0
        self.curr_ep_loss_length = 0

    def record(self, episode, epsilon, step):
        mean_ep_reward = np.round(np.mean(self.ep_rewards[-100:]), 3)
        mean_ep_length = np.round(np.mean(self.ep_lengths[-100:]), 3)
        mean_ep_loss = np.round(np.mean(self.ep_avg_losses[-100:]), 3)
        mean_ep_q = np.round(np.mean(self.ep_avg_qs[-100:]), 3)
        self.moving_avg_ep_rewards.append(mean_ep_reward)
        self.moving_avg_ep_lengths.append(mean_ep_length)
        self.moving_avg_ep_avg_losses.append(mean_ep_loss)
        self.moving_avg_ep_avg_qs.append(mean_ep_q)

        last_record_time = self.record_time
        self.record_time = time.time()
        time_since_last_record = np.round(self.record_time - last_record_time, 3)

        print(
            f"Episode {episode} - "
            f"Step {step} - "
            f"Epsilon {epsilon} - "
            f"Mean Reward {mean_ep_reward} - "
            f"Mean Length {mean_ep_length} - "
            f"Mean Loss {mean_ep_loss} - "
            f"Mean Q Value {mean_ep_q} - "
            f"Time Delta {time_since_last_record} - "
            f"Time {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
        )

        with open(self.save_log, "a") as f:
            f.write(
                f"{episode:8d}{step:8d}{epsilon:10.3f}"
                f"{mean_ep_reward:15.3f}{mean_ep_length:15.3f}{mean_ep_loss:15.3f}{mean_ep_q:15.3f}"
                f"{time_since_last_record:15.3f}"
                f"{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'):>20}\n"
            )

        for metric in ["ep_rewards", "ep_lengths", "ep_avg_losses", "ep_avg_qs"]:
            plt.plot(getattr(self, f"moving_avg_{metric}"))
            plt.savefig(getattr(self, f"{metric}_plot"))
            plt.clf()



def draftPhaseBot(roundnumber, player, actor):
    board = GAME.draftBoard(roundnumber, player)

    env=environment(board)
    action: int=0

    # 2d arrays of entries to be loaded into the cache
    to_cache=[]
    to_cache_index=0



    while action != 66 or to_cache_index<=20:
        #print("Cache Index: "+ str(to_cache_index))
        to_cache.append([0, 0, 0, 0, 0])
        to_cache[to_cache_index][0]= copy.deepcopy(env.state)
        action= actor.act(env.state, env)

        env.step(action)
        env.update_state()



        to_cache[to_cache_index][1]= copy.deepcopy(env.state)
        to_cache[to_cache_index][2]= action

        #does fill in the reward if the bot wastes money
        if action == 66 and env.board.money>0:
            to_cache[to_cache_index][3]= -1

        #rewards drafting more
        if action >=0 and action <= 24:
            to_cache[to_cache_index][3] = 1

        # penalizes selling if there are still empty slots
        if action >= 0 and action <= 24 and None in env.board.player.team:
            to_cache[to_cache_index][3] = -3

        to_cache_index= to_cache_index +1



    return to_cache











