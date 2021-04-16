import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions import Categorical

# policy model train data from trade agent 
class MLP_Policy(nn.Module):
    def __init__(self, state_space,action_space,params):
        super(MLP_Policy, self).__init__()
        """
        state_space : observation space
        action_space : action space
        """
        self.input_size=state_space.shape[-1]
        self.output_size=3  #sell pend buy

        self.linear1=nn.Linear(self.input_size,128,bias=False)
        self.relu=nn.LeakyReLU()
        self.linear2=nn.Linear(128,self.output_size,bias=False)
        self.softmax=nn.Softmax(dim=-1)
        
        self.dropout_rate=params.dropout_rate
        self.dropout=nn.Dropout(p=self.dropout_rate)
        self.gamma=params.gamma
        
        #Episode of policy
        self.policy_history=None
        self.reward_episode=None
        self.reward_episode_local=None
        
        self.reset_episode()
        
        self.loss_history=list()
        self.reward_history=list()
        self.reward_history_local=list()
        
    def reset_episode(self):
        self.policy_history=list()
        self.reward_episode=list()
        self.reward_episode_local=list()
#         print('we reset_policy')
        
    def forward(self,x):
        x=self.linear1(x)
        x=self.dropout(x)
        x=self.relu(x)
        x=self.linear2(x)
        x=self.softmax(x)
        
        return x
        
    def save_model(self):
        """ 
        directory need
        """
        
    def plot_result(self):
        """
        policy history and reward 
        """
