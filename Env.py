import os
import gym
import random
import numpy as np 
from gym import spaces
import matplotlib.pyplot as plt


#Uncle will trade 

    
class Cryptoenv(gym.Env):
    def __init__(self,params):
        """
        df : The dataframe that we have created in the past 

        reward_range :
                    Not really usefull but needed, 
                    let’s make it be between 2 huge numbers 
                    Let’s make it between -10 millions and +10 millions.

        total_fees : Keep track of the total fees paid


        crypto_held : Keep track of the crypto held (Bitcoin in our case)
        
        episode : The number of our current episode (start at 1)

        graph_reward, graph_profit, graph_benchmark : render the result.

        action_space : 
                We set our action space between -1 and 1. 
                1 means using 100% of our USDT to buy BTC, 
                0 means doing nothing, 
                -1 means selling all of our BTC/USDT.

        """
        self.df=params.df
        self.fee=params.fee
        self.window=params.window
        self.max_step=params.max_step
        self.directory=params.directory
        self.max_balance=params.max_balance
        self.max_net_worth=params.initial_balance
        self.initial_balance=params.initial_balance
        
        self.total_fees=0
        self.crpyto_held=0
        self.episode=1
        
        #graph to render
        self.graph_reward=[]
        self.graph_profit=[]
        self.graph_benchmark=[]
        
        #action space
        self.action_space=spaces.Box(low=0,
                                     high=2,
                                     shape=(1,),
                                     dtype=np.float32)
        
        #observation space
        self.observation_space=spaces.Box(low=0,
                                           high=1,
                                           shape=(1,self.window),
                                           dtype=np.float32)
        
        self.reward_range=(-self.max_balance,self.max_balance)                

    def reset(self):
        """
        reset status of gym env

        start out step from a random point in our data frame

        balance is initial worth

        """
        self.balance=self.initial_balance
        self.net_worth=self.initial_balance
        self.total_fees=0
        self.crypto_held=0
        self.episode_reward=0

        self.current_step=random.choice(list(range(self.window,
                                                   len(self.df)-self.max_step)))
        self.start_step=self.current_step

        return self._next_observation()

    def _next_observation(self):
        #get last window size of tick datas from dataframe 
        #get another data i.e) index, close or anything we can.
        frame=np.array(self.df.open[self.current_step-self.window:self.current_step])
        
        obs=frame.reshape(-1,self.window)
#         obs=np.append(frame,[[self.balance/self.max_balance,
#                               self.net_worth/self.max_net_worth,
#                               0]],axis=0)
        
        return obs




    def _take_action(self,action):
        #set the current price
        current_price=random.uniform(self.df.open[self.current_step],
                                     self.df.close[self.current_step])

        if action>1:
            #buy
            crypto_bought=int(self.balance*action/current_price)
            self.total_fees+=crypto_bought*current_price*self.fee
            self.balance-=crypto_bought*current_price
            self.crypto_held+=crypto_bought

        if action<1:
            #sell
            crypto_sold=-self.crypto_held*action
            self.total_fees+=crypto_sold*current_price*self.fee
            self.balance+=crypto_sold*current_price
            self.crypto_held-=crypto_sold

        self.net_worth=self.balance+self.crypto_held*current_price

        if self.net_worth>self.max_net_worth:
            self.max_net_worth=self.net_worth

    def step(self,action,end=True):
        #execute one time step 

        self._take_action(action)

        self.current_step+=1

        #calculate reward
        profit=self.net_worth-self.initial_balance
        profit_percent=profit/self.initial_balance*100

        benchmark=(self.df.open[self.current_step]/
                   self.df.open[self.start_step])*100

        diff=profit_percent-benchmark
        #reward as quadratic function.
        reward=np.sign(diff)*(diff)**2

        if self.current_step>=self.max_step+self.start_step:
            end = True
        else:
            end = False


        done=self.net_worth<=0 or end #

        if done and end:
            self.episode_reward=reward
            self._render_episode()
            self.graph_profit.append(profit_percent)
            self.graph_benchmark.append(benchmark)
            self.graph_reward.append(reward)
            self.episode+=1

        obs=self._next_observation()

        return obs,reward,done,{}

    def render(self,print_step=True,graph=False,*args):
        price=self.df.open[self.current_step]
        profit=self.net_worth-self.initial_balance
        profit_percent=profit/self.initial_balance*100
        benchmark=(self.df.open[self.current_step]/
                   self.df.open[self.start_step])*100

        if print_step:
            print("______________________________") #30
            print('\nStep:'.ljust(15),'{0:}'.format(self.current_step).rjust(15))
            print('\nPrice:'.ljust(15),'{0:.1f}'.format(price).rjust(15))
            print('\nCrypto held:'.ljust(15),'{0:.1f}'.format(self.crypto_held).rjust(15))
            print('\nBalance:'.ljust(15),'{0:.1f}'.format(self.balance).rjust(15))
            print('\nNetWorth:'.ljust(15),'{0:.1f}'.format(self.max_net_worth).rjust(15))
            print('\nProfit:'.ljust(15),'{0:.1f}'.format(profit).rjust(15))
            print('\n','{0:.1f}%'.format(profit_percent).rjust(30))

        if graph:
            fig=plt.figure()
            fig.suptitle('Training graph')

            high=plt.subplot(2,1,1)
            high.set(ylabel='Gain')
            plt.plot(self.graph_profit,label='Uncle profit')
            plt.plot(self.graph_benchmark,label='Bench profit')
            high.legend(loc='upper left')

            low=plt.subplot(2,1,2)
            low.set(xlabel='Episode',ylabel='Reward')
            plt.plot(self.graph_reward,label='reward')

            plt.show()

        return profit_percent,benchmark

    def _render_episode(self):
        direc=self.directory
        os.makedirs(direc, exist_ok=True)
        filename = os.path.join(direc, 'render.txt')
        with open(filename, 'a') as f:
            f.write('\n______________________________\n')
            f.write('\nEpisode:  {0:}'.format(self.episode))
            f.write('\nReward:  {0:}'.format(self.episode_reward))
            f.close()















        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    