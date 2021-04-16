import os
import torch
import numpy as np
import torch.optim as optim
from torch.distributions import Categorical

#agent에서 policy를 받아와야함. agent와 env는 따로 노는게 맞음.



class Uncle():
    def __init__(self,policy,params):
        self.policy=policy
        self.optimizer=optim.Adam(self.policy.parameters(),
                                  lr=params.learning_rate,
                                  weight_decay=params.weight_decay)
    
    
    
    def select_action(self,state):
        state=torch.FloatTensor(state)       
        action_state=self.policy.forward(state)
        choice_distribution=Categorical(action_state)
        action=choice_distribution.sample()
        
        action_probability=choice_distribution.log_prob(action)
        self.policy.policy_history.append(action_probability)
        return action.item()
    
    
    
    def update_policy(self):
        R=0
        rewards=list()
        reward_sum=0
        #reward를 env로 부터 가져와야함???? 
        for r in reversed(self.policy.reward_episode):
            R=r+self.policy.gamma*R
            rewards.insert(0,R)
            reward_sum+=R
            
        rewards=torch.FloatTensor(rewards)
        
        #layer normalization rewards
        rewards=(rewards-rewards.mean())/(rewards.std()+float(np.finfo(np.float32).eps))
        
        policy_history=torch.stack(self.policy.policy_history)
        
        loss=torch.sum(torch.mul(policy_history,rewards).mul(-1),dim=-1)
        self.optimizer.zero_grad()
        loss.sum().backward()
        self.optimizer.step()

        self.policy.loss_history.append(loss.sum().item())
        self.policy.reward_history.append(np.sum(self.policy.reward_episode))
        self.policy.reset_episode()
        
        
    