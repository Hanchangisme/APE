import os
import time
import random
from datetime import datetime

from ape import Session
from grannys_recipe import *


def main():
    # Environment varables.
    deltatime = 0.3 # Seconds
    
    # Initialize logger.
    os.makedirs('logs', exist_ok=True)
    filename = os.path.join('logs', 'burnt_cookies.txt')
    with open(filename, 'w') as f:
        f.write('')
    
    # Open session.
    sess = Session(leverage=125)
    
    # Register agents.
    rich_granny = GrannysBrownie(richness=100, timeout=10.0, verbose=True)
    #rich_granny = GrannysCookie(richness=1) # Richness = # of tickets.
    
    while True:
        # 1. Receive current value information.
        market_info = sess.get_current_price()
        pending_orders = sess.get_current_orders()
        current_positions = sess.get_current_positions()
        
        # 2. Generate list of orders with external agents.
        order_list, log_msg = rich_granny(
            market_info,
            pending_orders,
            current_positions,
        )
        num_lose = rich_granny.num_sonjeol
        num_win = rich_granny.num_eekjeol
        num_super_win = rich_granny.num_super_eekjeol
        
        # 3. Fetch generated orders.
        for order in order_list:
            if order.isrevoke:
                sess.revoke(pending_orders)
                order_list.remove(order)
        
#         print(order_list)
#         sess.order_batch(order_list)
#             print(order)
            if order.isopen:
                if order.iscurrent:
                    sess.open_current(order.size, order.islong)
                else:
                    sess.open(order.size, order.price, order.islong)
            else:
                if order.iscurrent:
                    sess.close_current(order.size, order.islong)
                else:
                    sess.close(order.size, order.price, order.islong)
        
        # TODO: Comment out before inserting real money.
        fieldnames = ['MODE', 'SIDE', 'LV', 'POS', 'AVAIL', 'AVG_PRICE']
        fields = [
            [
                current_positions['margin_mode'],
                pos['side'],
                pos['leverage'],
                pos['position'],
                pos['avail_position'],
                pos['avg_cost'],
            ] for pos in current_positions['holding']
        ]
        fields.insert(0, fieldnames)
        
        
        # Generate log messages.
        # TODO
        # 1. My profit + profit ratio!
        # 2. Current account info.
        # 3. Uptime & # of transactions generated.
        log_msg += (
            str(datetime.now())
            + '  Current Price: '
            + PrintPallete.UNDERLINE + str(market_info['last']) + PrintPallete.ENDC
            + '\n'
        )
        log_msg += ' # Loss | # Profit | # Super Profit\n'
        log_msg += '--------+----------+----------------\n'
        log_msg += (
            PrintPallete.FAIL + '{:^6d}' + PrintPallete.ENDC
            + '  |  '
            + PrintPallete.OKGREEN + '{:^6d}' + PrintPallete.ENDC
            + '  |    '
            + PrintPallete.OKCYAN + '{:^6d}\n' + PrintPallete.ENDC
        ).format(
            num_lose, num_win, num_super_win
        )
        log_msg += 'Current Positions\n'
        log_msg += '-----------------\n'
        for f in fields:
            line = '{:^5s}   {:^5s}   {:^3s}   {:^7s}   {:^7s}    {:10s}\n'.format(*f)
            log_msg += line
        log_msg += '\n'
        
        if len(pending_orders) > 0:
            log_msg += 'Pending Orders ID      SIZE     PRICE\n'
            log_msg += '-------------------------------------\n'
            for o in pending_orders:
                ling = '{:17s}    {:^7s}    {:s}\n'.format(
                    o['order_id'], o['size'], o['price']
                )
            log_msg += '\n'
            
        # Log in both the terminal and a file.
        print(log_msg)
        with open(filename, 'a') as f:
            f.write(log_msg)
            
        #input()
        #time.sleep(deltatime)


if __name__ == '__main__':
    print('\n\n\nDo you want to make money? (y|N)')
    ans = input()
    if ans[0].lower() != 'y':
        pussy_msgs = [
            'You weak pu***!',
            'You underestimated my POWER!!!',
            'It\'s over Anakin, I have the high ground!',
            'I am your GRANNY.'
        ]
        print(random.choice(pussy_msgs))
        exit(1)
    
    print('Copying money in')
    time.sleep(0.2)
    print('3 ... ')
    time.sleep(0.1)
    print('2 ... ')
    time.sleep(0.1)
    print('1 ...')
    time.sleep(0.1)
    print('Begin ...\n')
    main()