import enum
import math
import time

from order import Order


class PrintPallete:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_sonjeol():
    msg = PrintPallete.FAIL
    msg += ' _  _    _____  _____  _   _     ___  _____  _____  _        _  _ \n'
    msg += '| || |  /  ___||  _  || \ | |   |_  ||  ___||  _  || |      | || |\n'
    msg += '| || |  \ `--. | | | ||  \| |     | || |__  | | | || |      | || |\n'
    msg += '| || |   `--. \| | | || . ` |     | ||  __| | | | || |      | || |\n'
    msg += '|_||_|  /\__/ /\ \_/ /| |\  | /\__/ /| |___ \ \_/ /| |____  |_||_|\n'
    msg += '(_)(_)  \____/  \___/ \_| \_/ \____/ \____/  \___/ \_____/  (_)(_)\n\n'
    msg += PrintPallete.ENDC
    return msg


def print_eekjeol():
    msg = PrintPallete.OKGREEN
    msg += '______ ______  _____ ______  _____  _____   _  _  _ \n'
    msg += '| ___ \| ___ \|  _  ||  ___||_   _||_   _| | || || |\n'
    msg += '| |_/ /| |_/ /| | | || |_     | |    | |   | || || |\n'
    msg += '|  __/ |    / | | | ||  _|    | |    | |   | || || |\n'
    msg += '| |    | |\ \ \ \_/ /| |     _| |_   | |   |_||_||_|\n'
    msg += '\_|    \_| \_| \___/ \_|     \___/   \_/   (_)(_)(_)\n\n'
    msg += PrintPallete.ENDC
    return msg


def print_super_eekjeol():
    msg = ''
    msg += PrintPallete.FAIL + '______ ' + PrintPallete.WARNING + '______ ' + PrintPallete.OKGREEN + ' _____ ' + PrintPallete.OKCYAN + '______ ' + PrintPallete.OKBLUE + ' _____  _____  ' + PrintPallete.ENDC + ' _  _  _ \n'
    msg += PrintPallete.FAIL + '| ___ \\' + PrintPallete.WARNING + '| ___ \\' + PrintPallete.OKGREEN + '|  _  |' + PrintPallete.OKCYAN + '|  ___|' + PrintPallete.OKBLUE + '|_   _||_   _| ' + PrintPallete.ENDC + '| || || |\n'
    msg += PrintPallete.FAIL + '| |_/ /' + PrintPallete.WARNING + '| |_/ /' + PrintPallete.OKGREEN + '| | | |' + PrintPallete.OKCYAN + '| |_   ' + PrintPallete.OKBLUE + '  | |    | |   ' + PrintPallete.ENDC + '| || || |\n'
    msg += PrintPallete.FAIL + '|  __/ ' + PrintPallete.WARNING + '|    / ' + PrintPallete.OKGREEN + '| | | |' + PrintPallete.OKCYAN + '|  _|  ' + PrintPallete.OKBLUE + '  | |    | |   ' + PrintPallete.ENDC + '| || || |\n'
    msg += PrintPallete.FAIL + '| |    ' + PrintPallete.WARNING + '| |\ \ ' + PrintPallete.OKGREEN + '\ \_/ /' + PrintPallete.OKCYAN + '| |    ' + PrintPallete.OKBLUE + ' _| |_   | |   ' + PrintPallete.ENDC + '|_||_||_|\n'
    msg += PrintPallete.FAIL + '\_|    ' + PrintPallete.WARNING + '\_| \_|' + PrintPallete.OKGREEN + ' \___/ ' + PrintPallete.OKCYAN + '\_|    ' + PrintPallete.OKBLUE + ' \___/   \_/   ' + PrintPallete.ENDC + '(_)(_)(_)\n\n'
    msg += '' + PrintPallete.ENDC
    return msg


class GrannysCookie():
    def __init__(self, richness):
        self.size = richness
        self.call_num = 0
        
    def __call__(
        self,
        market_info,
    ):
        current_price = float(market_info['last'])
        order_list = []
        if self.call_num < 5:
            order_list.append(
                Order(self.size, current_price, isopen=True, islong=True)
            )
        else:
            order_list.append(
                Order(self.size, current_price - 1000.0, isopen=False, islong=True)
            )
        self.call_num = (self.call_num + 1) % 10
        return order_list
    
    
class State(enum.Enum):
    Init = 1
    OpenCheck = 2
    Pending = 3
    LongRichWait = 4
    LongRich = 5
    LongPoor = 6
    ShortRichWait = 7
    ShortRich = 8
    ShortPoor = 9
    CloseCheck = 10
    GreatDepression = 11

    
class GrannysBrownie():
    def __init__(self, richness, timeout=5.0, verbose=False):
        self.size = richness
        self.timeout = timeout
        self.verbose = verbose
        self.timer = time.time()
        self.state = State.Init
        self.current_max = -math.inf
        self.current_min = math.inf
        
        self.previous_price = -math.inf
        self.num_eekjeol = 0
        self.num_super_eekjeol = 0
        self.num_sonjeol = 0
    
    def parse_positions(self, positions: dict):
        my_long = 0
        my_short = 0
        for pos in positions['holding']:
            if pos['side'] == 'long':
                my_long += int(pos['position'])
            elif pos['side'] == 'short':
                my_short += int(pos['position'])
            else:
                raise ValueError
        return (my_long, my_short)
        
    def append_open(
        self,
        order_list: list,
        price: float,
        size: int,
        islong: bool,
    ):
        if size <= 0:
            return order_list
#         margin = 20.0 # TODO Delete this magic number!!!!
#         margin *= (1 if islong else -1)
        order_list.append(Order(size, price, True, islong, True))
        return order_list
    
    def append_close(
        self,
        order_list: list,
        price: float,
        size: int,
        islong: bool,
    ):
        if size <= 0:
            return order_list
        margin = 100.0 # TODO Delete this magic number!!!!
        margin *= (-1 if islong else 1)
        order_list.append(Order(size, price + margin, False, islong))
        return order_list
    
    def append_revoke(self, order_list: list):
        order_list.append(Order(self.size, 0.0, True, True, isrevoke=True))
        return order_list
    
    def get_my_price(self, positions):
        '''Get average price values of my positions.
        
        Returns tuple(float, float):
            [0]: Long position average price; None if I have none.
            [1]: Short position average price; None if I have none.
        '''
        my_long, my_short = self.parse_positions(positions)
        long_price = [
            float(pos['avg_cost'])
            for pos in positions['holding']
            if pos['side'] == 'long'
        ][0]
        short_price = [
            float(pos['avg_cost'])
            for pos in positions['holding']
            if pos['side'] == 'short'
        ][0]
        return (
            long_price if my_long else None,
            short_price if my_short else None,
        )

    def __call__(
        self,
        market_info,
        pending_orders,
        current_positions,
    ):
        current_price = float(market_info['last'])
        my_long, my_short = self.parse_positions(current_positions)
        long_price, short_price = self.get_my_price(current_positions)
        self.current_max = max(current_price, self.current_max)
        self.current_min = min(current_price, self.current_min)
        
        max_is_now = self.current_max == current_price
        min_is_now = self.current_min == current_price
        
        log_msg = ''
        order_list = []
        next_state = self.state
        if self.state == State.Init:
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Init' + PrintPallete.ENDC
                    + '\n '
                )
            # Open both long and short positions together.
            self.long_tickets = self.size
            self.short_tickets = self.size
            self.append_open(
                order_list,
                current_price,
                self.long_tickets,
                islong=True,
            )
            self.append_open(
                order_list,
                current_price,
                self.short_tickets,
                islong=False,
            )
            self.timer = time.time()
            self.current_max = current_price
            self.current_min = current_price
            # State update.
            next_state = State.OpenCheck
            
        elif self.state == State.OpenCheck:
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Open Check' + PrintPallete.ENDC
                    + '\n '
                )
                log_msg += (
                    'Margin Mode: '
                    + str(current_positions['margin_mode'])
                    + '\n'
                )
            # Check timer for timeout.
            # If timer's over, close all my current positions and reset.
            if time.time() - self.timer > self.timeout:
                log_msg += 'Timer\'s over! I\'m out!\n'
                self.append_close(order_list, current_price, my_long, True)
                self.append_close(order_list, current_price, my_short, False)
                next_state = State.GreatDepression
            # State update: Check any pending orders.
            elif (
                len(pending_orders) > 0 and
                (my_long != self.long_tickets or my_short != self.short_tickets)
            ):
                next_state = self.state
            else:
                next_state = State.Pending

        elif self.state == State.Pending:
            # Thresholds for quitting LONG position.
            long_thres = (1 - (0.0012 / 1.0003 / 3)) * long_price
            # Thresholds for quitting SHORT position.
            short_thres = (1 + (0.0012 / 0.9997 / 3)) * short_price
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Pending' + PrintPallete.ENDC
                    + ';  '
                )
                log_msg += (
                    'ShortQuit='
                    + PrintPallete.OKGREEN + '{:.2f}' + PrintPallete.ENDC
                    + '  LongQuit='
                    + PrintPallete.FAIL + '{:.2f}' + PrintPallete.ENDC
                    + '\n'
                ).format(
                    short_thres, long_thres
                )
            # State update.
            #if my_long == 0:
            if current_price < long_thres:
            #if current_price > short_thres: #granny's random box
                self.append_close(order_list, current_price, my_long, True)
                self.onehand_price = current_price
                self.timer = time.time()
                next_state = State.ShortRichWait
            #elif my_short == 0:
            elif current_price > short_thres:
            #elif current_price < long_thres: #granny's random box
                self.append_close(order_list, current_price, my_short, False)
                self.onehand_price = current_price
                self.timer = time.time()
                next_state = State.LongRichWait
            else:
                next_state = State.Pending
        
        elif self.state == State.LongRichWait:
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Long Rich Wait' + PrintPallete.ENDC
                    + '\n'
                )
            # State update: Check any pending orders.
            if my_short == 0:
                next_state = State.LongRich
            else:
                if len(pending_orders) == 0:
                    self.append_close(order_list, current_price, my_short, False)
                    self.timer = time.time()
                # Check timer for timeout.
                elif time.time() - self.timer > self.timeout:
                    log_msg += 'Timer\'s over! REORDER!\n'
                    self.append_revoke(order_list)
                next_state = self.state
                
        elif self.state == State.ShortRichWait:
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Short Rich Wait' + PrintPallete.ENDC
                    + '\n'
                )
            # State update: Check any pending orders.
            if my_long == 0:
                next_state = State.ShortRich
            else:
                if len(pending_orders) == 0:
                    self.append_close(order_list, current_price, my_long, True)
                    self.timer = time.time()
                # Check timer for timeout.
                elif time.time() - self.timer > self.timeout:
                    log_msg += 'Timer\'s over! REORDER!\n'
                    self.append_revoke(order_list)
                next_state = self.state
            
        elif self.state == State.LongRich:
#             alpha_line = -(1.0009 / 0.9997 - 1) * long_price + self.onehand_price
#             beta_line = alpha_line + (1.0021 / 0.9997 - 1.0009 / 0.9997 - 1) * long_price + self.onehand_price
            alpha_line = (1.0009 / 0.9997 - 1) * long_price + self.onehand_price
            beta_line = (1.0021 / 0.9997 - 2) * long_price + 2 * self.onehand_price
            if self.current_max < beta_line:
                johnburr_thres = 0.0012 / 0.9997 * (1 - 0.001 * my_long) * long_price
            else:
                johnburr_thres = (0.0012 / 0.9997 - 1) * long_price + self.onehand_price
            johnburr_thres *= 0.5
                
            if self.verbose:
                max_col = PrintPallete.OKGREEN if max_is_now else PrintPallete.ENDC
                min_col = PrintPallete.FAIL if min_is_now else PrintPallete.ENDC
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Long Rich'\
                    + PrintPallete.ENDC + '\n'
                )
                log_msg += (
                    'AL='
                    + PrintPallete.OKCYAN + '{:.2f}' + PrintPallete.ENDC
                    + '  BL='
                    + PrintPallete.OKBLUE + '{:.2f}' + PrintPallete.ENDC
                    + '  MAX|MIN='
                    + max_col + '{:.2f}' + PrintPallete.ENDC
                    + '|'
                    + min_col + '{:.2f}' + PrintPallete.ENDC
                    + '  JohnBurr='
                    + PrintPallete.WARNING + '{:.2f}' + PrintPallete.ENDC
                    + '\n'
                ).format(
                    alpha_line,
                    beta_line,
                    self.current_max,
                    self.current_min,
                    self.current_max - johnburr_thres,
                )
            # State update.
            if current_price < self.current_max - johnburr_thres:
                if self.current_max < alpha_line:
                    log_msg += print_sonjeol()
                    self.num_sonjeol += 1
                elif self.current_max > beta_line:
                    log_msg += print_super_eekjeol()
                    self.num_super_eekjeol += 1
                else:
                    log_msg += print_eekjeol()
                    self.num_eekjeol += 1
                self.append_close(order_list, current_price, my_long, True)
                self.timer = time.time()
                next_state = State.CloseCheck
            else:
                # John Burr: Stay rich, stay full.
                next_state = State.LongRich
            
        elif self.state == State.ShortRich:
#             alpha_line = -(0.9991 / 1.0003 - 1) * short_price + self.onehand_price
#             beta_line = alpha_line + (0.9979 / 1.0003 - 0.9991 / 1.0003 - 1) * short_price + self.onehand_price 
            alpha_line = (0.9991 / 1.0003 - 1) * short_price + self.onehand_price
            beta_line = (0.9979 / 1.0003 - 2) * short_price + 2 * self.onehand_price
            if self.current_min > beta_line:
                johnburr_thres = 0.0012 / 1.0003 * (1 - 0.001 * my_long) * short_price
            else:
                johnburr_thres = (0.0012 / 1.0003 + 1) * short_price - self.onehand_price
            johnburr_thres *= 0.5

            if self.verbose:
                max_col = PrintPallete.OKGREEN if max_is_now else PrintPallete.ENDC
                min_col = PrintPallete.FAIL if min_is_now else PrintPallete.ENDC
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Short Rich'\
                    + PrintPallete.ENDC + '\n'
                )
                log_msg += (
                    'AL='
                    + PrintPallete.OKCYAN + '{:.2f}' + PrintPallete.ENDC
                    + '  BL='
                    + PrintPallete.OKBLUE + '{:.2f}' + PrintPallete.ENDC
                    + '  MAX|MIN='
                    + max_col + '{:.2f}' + PrintPallete.ENDC
                    + '|'
                    + min_col + '{:.2f}' + PrintPallete.ENDC
                    + '  JohnBurr='
                    + PrintPallete.WARNING + '{:.2f}' + PrintPallete.ENDC
                    + '\n'
                ).format(
                    alpha_line,
                    beta_line,
                    self.current_max,
                    self.current_min,
                    self.current_min + johnburr_thres,
                )
            # State update.
            if current_price > self.current_min + johnburr_thres:
                if self.current_max > alpha_line:
                    log_msg += print_sonjeol()
                    self.num_sonjeol += 1
                elif self.current_max < beta_line:
                    log_msg += print_super_eekjeol()
                    self.num_super_eekjeol += 1
                else:
                    log_msg += print_eekjeol()
                    self.num_eekjeol += 1
                self.append_close(order_list, current_price, my_short, False)
                self.timer = time.time()
                next_state = State.CloseCheck
            else:
                # John Burr: Stay rich, stay full.
                next_state = State.ShortRich
        
        elif self.state == State.CloseCheck:
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Close Check' + PrintPallete.ENDC
                    + '\n'
                )
            # Check timer for timeout.
#             if time.time() - self.timer > self.timeout:
#                 print('Timer\'s over! I\'m out!')
#                 next_state = State.GreatDepression
            # State update: Check any pending orders.
            if my_long == 0 and my_short == 0:
                next_state = State.Init
            else:
                if len(pending_orders) == 0:
                    self.append_close(order_list, current_price, my_long, True)
                    self.append_close(order_list, current_price, my_short, False)
                next_state = self.state
                
        elif self.state == State.GreatDepression:
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Fucked Up' + PrintPallete.ENDC
                    + '\n'
                )
            # State update.
            # If any pending orders exist --> Cancel immediately!
            if len(pending_orders) > 0:
                self.append_revoke(order_list)
                next_state = self.state
            else:
                next_state = State.Init
        
        else:
            if self.verbose:
                log_msg += (
                    'Current state: '
                    + PrintPallete.UNDERLINE + 'Where Am I?' + PrintPallete.ENDC
                    + '\n'
                )
            # State update.
            next_state = State.RunForNothing
        
        self.state = next_state
        self.previous_price = current_price
        return order_list, log_msg