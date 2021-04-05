#import time
import random

import bitget.exceptions
import bitget.swap_api as swap
import bitget.option_api as option


class Session():
    def __init__(self, real_money: bool = False, leverage: int = 1):
        self.api_key = 'bg_f20fb5acafac7a09492d57aa89708b85'
        self.secret_key = '5fe77cd579c84dd7623687af1fdb02108df2715768732110ed8a7649dad7a7a8'
        self.passphrase = 'gksckdgmlckd'
        
        # Open sessions.
        self.swap_api = swap.SwapAPI(
            self.api_key,
            self.secret_key,
            self.passphrase,
            use_server_time=True,
            first=False,
        )
        self.option_api = option.OptionAPI(
            self.api_key,
            self.secret_key,
            self.passphrase,
            use_server_time=True,
            first=False,
        )
        
        # s for simulation
        self.market = 'cmt_btcsusdt' if real_money else 'sbtcusd'
        self.leverage = leverage
        self.set_leverage(leverage)
        
    def get_client_oid(self):
        return random.randint(1000000000,9999999999999)

    def get_current_price(self):
        '''Get current market price.
        
        Return (dict):
            Sample value:
            {'symbol': 'cmt_btcsusdt',
             'last': '54755.5',
             'best_ask': '54777.0',
             'best_bid': '54775.5',
             'high_24h': '55509',
             'low_24h': '52893.5',
             'volume_24h': '16962639',
             'timestamp': '1616817424258',
             'priceChangePercent': '2.73',
             'base_volume': '16962.639'}
        '''
        return self.swap_api.get_specific_ticker(self.market)
    
    def get_current_orders(self):
        '''
        Returns:
        [
            {
                'symbol': 'sbtcusd',
                'size': '1',
                'client_oid': '4414655719220',
                'createTime': '1616827290879',
                'filled_qty': '0',
                'fee': '0.00000000',
                'order_id': '759594201443729413',
                'price': '55107.00',
                'price_avg': '0.00',
                'status': '0',
                'type': '1',
                'order_type': '0',
                'totalProfits': '0',
            }
        ]
        '''
        orders = self.option_api.get_order_current(self.market)
        return orders
    

    
    def get_current_positions(self, getall: bool = False):
        '''
        Returns:
        {
            'margin_mode': 'fixed',
            'holding': [
                {
                    'liquidation_price': '54797.40',
                    'position': '15',
                    'avail_position': '15',
                    'avg_cost': '55092.53',
                    'symbol': 'sbtcusd',
                    'leverage': '125',
                    'keepMarginRate': '0.0020',
                    'realized_pnl': '0.00000000',
                    'unrealized_pnl': '0.00000012',
                    'side': 'long',
                    'holdSide': '1',
                    'timestamp': '1616751151027',
                    'margin': '0.000002178157'
                },
                {
                    'liquidation_price': '0.00',
                    'position': '0',
                    'avail_position': '0',
                    'avg_cost': '0.00',
                    'symbol': 'sbtcusd',
                    'leverage': '125',
                    'keepMarginRate': '0.0020',
                    'realized_pnl': '0.00000000',
                    'unrealized_pnl': '0.00000000',
                    'side': 'short',
                    'holdSide': '2',
                    'timestamp': '1616751151027',
                    'margin': '0.000000000000'
                }
            ]
        }
        '''
        if getall:
            return self.swap_api.get_all_position()
        return self.swap_api.get_single_position(self.market)
    
    def set_leverage(self, leverage: int): #, side: int = 1, hold_side: int = 1):
        self.swap_api.set_leverage(self.market, leverage, 1, 1)
        self.swap_api.set_leverage(self.market, leverage, 2, 2)
    
    def open(
        self,
        size : int,
        price : float,
        long : bool, # 1: open long; 2: open short; 3: close long; 4: close short
        order_type : int = 0, # 0: Good Till Cancel; 1: Post Only; 2: Immediately or Cancel; 3: Fill or Kill
    ):
        try:
            res = self.option_api.take_order(
                symbol=self.market,
                client_oid=self.get_client_oid(),
                size=str(size),
                type=('1' if long else '2'),
                order_type=str(order_type),
                match_price='0',
                price=str(price),
            )
        except bitget.exceptions.BitgetAPIException as e:
            print('ape::open', e)
    
    def open_current(
        self,
        size : int,
        long : bool, # 1: open long; 2: open short; 3: close long; 4: close short
        order_type : int = 0, # 0: Good Till Cancel; 1: Post Only; 2: Immediately or Cancel; 3: Fill or Kill
    ):
        try:
            res = self.option_api.take_order(
                symbol=self.market,
                client_oid=self.get_client_oid(),
                size=str(size),
                type=('1' if long else '2'),
                order_type=str(order_type),
                match_price='1',
            )
        except bitget.exceptions.BitgetAPIException as e:
            print('ape::open_current', e)

    def close(
        self,
        size : int,
        price : float,
        long : bool, # 1: open long; 2: open short; 3: close long; 4: close short
        order_type : int = 0, # 0: Good Till Cancel; 1: Post Only; 2: Immediately or Cancel; 3: Fill or Kill
    ):
        try:
            res = self.option_api.take_order(
                symbol=self.market,
                client_oid=self.get_client_oid(),
                size=str(size),
                type=('3' if long else '4'),
                order_type=str(order_type),
                match_price='0',
                price=str(price),
            )
        except bitget.exceptions.BitgetAPIException as e:
            print('ape::close', e)
    
    def close_current(
        self,
        size : int,
        long : bool, # 1: open long; 2: open short; 3: close long; 4: close short
        order_type : int = 1, # 0: Good Till Cancel; 1: Post Only; 2: Immediately or Cancel; 3: Fill or Kill
    ):
        try:
            res = self.option_api.take_order(
                symbol=self.market,
                client_oid=self.get_client_oid(),
                size=str(size),
                type=('3' if long else '4'),
                order_type=str(order_type),
                match_price='1',
            )
        except bitget.exceptions.BitgetAPIException as e:
            print('ape::close_current', e)
            
    def order_batch(
        self,
        order_list,
    ):
        '''Post multiple orders simultaneously.
        '''
        if len(order_list) == 0:
            return
        
        try:
            def get_type(isopen, islong):
                if isopen and islong:
                    return 1
                elif isopen and not islong:
                    return 2
                elif not isopen and islong:
                    return 3
                else:
                    return 4
                
            # type - 1: open long; 2: open short; 3: close long; 4: close short
            # match_price - 0: Specified Price; 1: Current Price.
            # order_type - 0: Good Till Cancel; 1: Post Only; 2: Immediately or Cancel; 3: Fill or Kill
            order_data = [
                {
                    'price': o.price,
                    'size': o.size,
                    'type': get_type(o.isopen, o.islong),
                    'match_price': ('1' if o.iscurrent else '0'),
                    # TODO more sophisticated tuning?
                    'order_type': ('0' if o.isopen else '1'),
                    'client_oid': self.get_client_oid(),
                }
                for o in order_list
                if not o.isrevoke
            ]
            res = self.option_api.take_orders(
                symbol=self.market,
                order_data=str(order_data).replace("'", '"'),
            )
        except bitget.exceptions.BitgetAPIException as e:
            print('ape::order_batch', e)
        
    def revoke(
        self,
        order_list,
    ):
        try:
            self.option_api.revoke_orders(
                self.market,
                [o['order_id'] for o in order_list],
            )
        except bitget.exceptions.BitgetAPIException as e:
            print('ape::revoke', e)