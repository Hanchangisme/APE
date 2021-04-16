import os
import time

import Env
import Policy
import Agent

import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class Params:
    df=pd.read_csv('btcusd.csv')
    max_balance:int=10000000000 
    initial_balance:int=500000 #money i have..
    window=50
    
    directory = 'logs'
    fee:int=0.0003
    max_step:int=4000
    episode:int=1000
    

    dropout_rate=0.6
    gamma=0.99
    
    learning_rate=1e-2
    weight_decay=1e-3

def train(agent,env,params,render=False):
    for episode in range(params.episode):
        state=env.reset()
        
        step=0
        done=False
        
        for each_step in range(params.max_step):
            if render:
                env.render()
            
            action=agent.select_action(state)
            
            state,reward,done,_=env.step(action)
            
            agent.policy.reward_episode.append(reward)
            
            if done:
                break
        
        agent.update_policy()
        time.sleep(0.01)
        if episode%100==0:
            print('========================================')
            print('\n\n\n\n\n\n')
            print('Episode: {0:5d}\n'.format(episode))
            print('reward :  {0:.2f}'.format(np.mean(agent.policy.reward_episode)))
            print('\n\n\n\n\n\n')
            print('========================================')
            #save구현

def run():
    render=True
    params=Params()
    env=Env.Cryptoenv(params)
    state_space,action_space=env.observation_space,env.action_space
    policy=Policy.MLP_Policy(state_space,action_space,params)
    agent=Agent.Uncle(policy,params)
    
    train(agent,env,params,render)
    
if __name__=="__main__":
    run()