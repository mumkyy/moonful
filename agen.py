import torch
import numpy as np
from collections import deque
from breath_predictor import User
import random
from model import Linear_Qnet, QTrainer
import csv

BATCH_SIZE = 5
MAX_MEMORY = 100000
LR = 0.001

class Agent:

    def __init__(self) -> None:
        self.n_opens = 0
        self.epsilon = 0
        self.gamma = 0.8
        self.n_opens = 0
        self.memory = self.memory_init('mems.csv')
        self.model = self.model_init('model/model.pth')
        self.trainer = QTrainer(self.model,LR,self.gamma)

    def get_state(self,user):
        return user.get_state()

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def get_action(self,state):
        self.epsilon = 80 - self.n_opens
        final_move = 0
        if random.randint(0,200) < self.epsilon:
            move = random.randint(1,10)
            final_move = move
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move = move
        
        return final_move
    
    def memory_save(self, path):
        with open(path, 'w', newline='') as mems_file:
            writer = csv.writer(mems_file)
            for entry in self.memory:
                state, action, reward, next_state, done = entry
                serialized_entry = [
                    *state,  # State components as a list
                    action,  # Action (single value)
                    reward,  # Reward (single value)
                    *next_state,  # Next state components as a list
                    int(done),  # Convert done to 0 or 1
                ]
                writer.writerow(serialized_entry)

    def memory_init(self, path):
        memory = deque(maxlen=MAX_MEMORY)
        try:
            with open(path, 'r') as mems_file:
                reader = csv.reader(mems_file)
                for row in reader:
                    state = list(map(float, row[:10]))
                    action = int(float(row[10]))  # Convert action to int
                    reward = float(row[11])
                    next_state = list(map(float, row[12:22]))
                    done = bool(int(row[22]))  # Convert done to bool
                    memory.append((state, action, reward, next_state, done))
        except FileNotFoundError:
            pass  # Handle the case when the file is not found
        return memory
        
    def model_init(self,path):
        model = Linear_Qnet(10,10,1)
        try:
            model.load_state_dict(torch.load(path))
            model.train()
            return model

        except:
            return model
        
    
