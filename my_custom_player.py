from sample_players import DataPlayer
from isolation import Isolation, DebugState
import random
import math
class CustomPlayer(DataPlayer):
    
    def __init__(self, player_id):
        super().__init__(player_id)
        
       
        self.opening_book = self.load_opening_book()        

    def load_opening_book(self):
        # currently self.data is the opening book, but it could store more in the future
        # so keep self.data and self.opening_book seperated into two variables
        return self.data
    
    def get_opening_book_action(self, board):
        if board in self.opening_book:
           
            return self.opening_book[board]
        else:
            return None
        
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least
        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.
        See RandomPlayer and GreedyPlayer in sample_players for more examples.
        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
       
        action = None    
        on_depth = 0

        try:
#        if True:
            USE_OPENING_BOOK = True # switch this flag to get results for project report requirement - using opening book, and not using it
          

            # for the first 4 moves, use opening book if possible
            if USE_OPENING_BOOK and state.ply_count < 4:  
                if self.opening_book is None:
                    print ('Opening Book does not exist!!')
                else:
                    action = self.get_opening_book_action(state.board)
                    #print(action)
            
            # if there is no move found in opening book, or number of moves played is greater than 4
            if action == None:                    
                if state.ply_count < 2:
                    action = random.choice(state.actions())
                    
                else:
                 
                    # depth set to same as AI (depth=3) 
                    # to make sure its 'fair', as setting a depth more than AI will automatically be better, without any extra coding
                    depth = 3
                    #print(self.data)
                    best_move = None
                    #on_depth = 0
                    #for d in range(1, depth+1):
    
                        # track dpeth
                      #  on_depth = d

                        # minimax - lower winning rate compare to alpha beta search    
                    best_move = minimax(state, depth)

                        # benchmark
                    #best_move = alpha_beta_search(state, d)
                        
                        
                    action = best_move
    
            self.queue.put(action)
                                    
        except Exception as ex:
            # use best move when time runs out
            if str(type(ex)) == "<class 'isolation.StopSearch'>":
                feedback('Time runs out at depth={0}, iterative deepening best action is: {1}'.format(on_depth, action))
                feedback()
                if action is not None:
                    self.queue.put(action)
            
         
            # pass the exception back to level above, the calling code
            raise ex 
            
   
        

def iterative_deepening(state, depth):
    best_move = None
    for d in range(1, depth+1):
        # best_move = minimax(state, depth)
        best_move = alpha_beta_search(state, d)
        
        # trace the depth been executed
        # print ('iterative deepening next depth =', d)
    return best_move


def alpha_beta_search(state, depth):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.
    
    You can ignore the special case of calling this function
    from a terminal state.
    """
    
    player_id = state.player()    

    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    best_move = None
    
    def min_value(state, alpha, beta, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if state.terminal_test(): return state.utility(player_id)
        if depth <= 0: return score(state, player_id)
        
        v = float("inf")
        for a in state.actions():
            v = min(v, max_value(state.result(a), alpha, beta, depth-1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def max_value(state, alpha, beta, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if state.terminal_test(): return state.utility(player_id)
        if depth <= 0: return score(state, player_id)
        
        v = float("-inf")
        for a in state.actions():
            v = max(v, min_value(state.result(a), alpha, beta, depth-1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    for a in state.actions():
        v = min_value(state.result(a), alpha, beta, depth-1)
        alpha = max(alpha, v)
        if v >= best_score:
            best_score = v
            best_move = a
    return best_move

# AI minimax, from this project itself, in sample_players.py
def minimax(state, depth):

    player_id = state.player()
    
    def min_value(state, depth):
        if state.terminal_test(): return state.utility(player_id)
        if depth <= 0: return score(state, player_id)
        value = float("inf")
        for action in state.actions():
            value = min(value, max_value(state.result(action), depth - 1))
        return value

    def max_value(state, depth):
        if state.terminal_test(): return state.utility(player_id)
        if depth <= 0: return score(state, player_id)
        value = float("-inf")
        for action in state.actions():
            value = max(value, min_value(state.result(action), depth - 1))
        return value

    return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

def score(state, player_id):
    own_loc = state.locs[player_id]
    opp_loc = state.locs[1 - player_id]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) - len(opp_liberties)