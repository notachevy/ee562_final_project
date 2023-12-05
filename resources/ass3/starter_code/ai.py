''' 
ai.py

Nathan Ford
EE 562
October 21, 2023

This program creates an AI class to be fed a Mancala board state and return an optimal move.
    the opponent is assumed to play optimally. 
'''

import time

CONST_DEPTH = 9 # depth limit of search

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        pass

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a # own holes
            self.b = b # opponent holes
            self.a_fin = a_fin # num stones in own kallah
            self.b_fin = b_fin # num stones in opponent kallah

        # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 

    def move(self, a, b, a_fin, b_fin, t):
        # # In your experiments, you can try different depth, for example:
        # f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # # Make sure to clean the file before each of your experiment
        # for d in range(1, CONST_DEPTH + 1, 2): #You should try more
        #     f.write('depth = '+str(d)+'\n')
        #     t_start = time.time()
        #     move = self.minimax(a, b, a_fin, b_fin, CONST_DEPTH - d, t_start, t)
        #     f.write(str(time.time()-t_start)+'\n')
        # f.close()
        # return move
        # # #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        # # #and remove timing code. 
        # # #Comment all the code above and start your code here


        start_time = time.time() # start timer

        # print(self.heuristic2(a, b, a_fin, b_fin, 0))
        # print("Available moves: ", self.getSuccessors(a))
        move = self.minimax(a, b, a_fin, b_fin, 0, start_time, t)

        # code to write runtimes to a .txt file
        # f = open('time.txt', 'a') #append to time.txt so that you can see running time for all
        # f.write('depth = '+str(CONST_DEPTH)+'\n')
        # f.write(str(time.time()-start_time)+'\n')
        # f.close()

        # print("Move: ", move)
        return move


    # This function tests if a given state is terminal - either the game ended (in a win, loss, or tie) or the depth or time limit was reached.
    #    True is returned if the state is terminal and False otherwise.
    #     @param a - an array of the number of stones in each of the player's holes
    #     @param a_fin - the number of stones in the player's kalah
    #     @param b_fin - the number of stones in the opponent's kalah
    #     @param depth - the current search depth
    #     @param start_time - time the move search began
    #     @param time_limit - the time limit of the search
    def testIfTerminalState(self, a, a_fin, b_fin, depth, start_time, time_limit):
        successors = self.getSuccessors(a) # possible moves

        # reached search depth or search time-limit or a player won or tied or no more possible moves
        return (depth == CONST_DEPTH) or ((time.time() - start_time) > time_limit) or \
            a_fin > 36 or b_fin > 36 or (a_fin == 36 and b_fin == 36) or len(successors) == 0 


    # This function returns the heuristic value of a given state by looking at the difference between the number of stones in the 
    #    player kalah vs the number of stones in the opponent kalah
    #     @param a - an array of the number of stones in each of the player's holes
    #     @param b - an array of the number of stones in each of the opponent's holes
    #     @param a_fin - the number of stones in the player's kalah
    #     @param b_fin - the number of stones in the opponent's kalah
    #     @param going_again - whether or not the current state is the result of a chained move
    def heuristic(self, a, b, a_fin, b_fin, going_again):
        return a_fin - b_fin # player kalah - opponent kalah
    


    # This function returns the elements of a state and whether or not the move warrants another move
    #     @param a - an array of the number of stones in each of the player's holes
    #     @param b - an array of the number of stones in each of the opponent's holes
    #     @param a_fin - the number of stones in the player's kalah
    #     @param b_fin - the number of stones in the opponent's kalah
    #     @param move - a number from [0, 5] that represents the player hole to start the move in
    def updateNewState(self, a, b, a_fin, b_fin, move):
        if(a[move] == 0): # move hole is empty
            return None, False # return no new state and no move again

        ao = a[:] # initial player holes
        # array containing all player holes, player kalah, and opponent holes in that order
        #     with current move at index 0
        full_board = a[move:] + [a_fin] + b + a[:move]
        num_stones = a[move] # num stones in move hole
        full_board[0] = 0 # sets move hole to empty
        position = 1 # distance counterclockwise from move hole

        while num_stones > 0: # while there are still stones to move
            full_board[position] += 1 # place a stone in hole as counterclockwise traversal
            position = (position + 1) % 13 # move to next position and wrap around if necessary
            num_stones -= 1 # decrease number of remaining stones

        # update stones in each position
        a_final = full_board[6 - move]
        b_final = b_fin
        b_holes = full_board[7 - move:13 - move]
        a_holes = full_board[13 - move:] + full_board[:6-move]

        move_again = bool() # move again
        ceat = False # final stone placed in empty player hole

        position = (position - 1) % 13
        if position == 6 - move: # move ended in the player kalah
            move_again = True # player should move again

        # determine if final stone placed in empty player hole
        if position <= 5 - move and ao[move] < 14:
            id = position + move
            if (ao[id] == 0 or position % 13 == 0) and b_holes[5 - id] > 0:
                ceat = True
        elif position >= 13 - move and ao[move] < 14:
            id = position + move - 13
            if (ao[id] == 0 or position % 13 == 0) and b_holes[5 - id] > 0:
                ceat = True

        # if ends in own empty hole
        if ceat:
            a_final += b_holes[5-id]+1 # add stones in corresponding opponent hole and the final stones to player kalah
            b_holes[5-id] = 0 # empty corresponding opponent hole
            a_holes[id] = 0 # empty own hole

        # if no stones in player holes
        if sum(a_holes)==0:
            b_final += sum(b_holes)

        # if no stones in opponent holes
        if sum(b_holes)==0:
            a_final += sum(a_holes)

        return a_holes, b_holes, a_final, b_final, move_again



    # This function returns a list of all moves that result in a legal successor state
    #     @param a - an array of the number of stones in each of the player's holes
    def getSuccessors(self, a):
        successors = [] # legal moves

        for i in range(len(a)): # each own hole
            if a[i] != 0: # hole is not empty
                successors.append(i) # add move to legal moves

        return successors # array of successors with their move and if they get to go again



    # This function returns a move in the form [0, 5] that results in the best board state for the AI. The 
    #    search uses an alpha-beta minimax search algorithm.
    #     @param a - an array of the number of stones in each of the player's holes
    #     @param b - an array of the number of stones in each of the opponent's holes
    #     @param a_fin - the number of stones in the player's kalah
    #     @param b_fin - the number of stones in the opponent's kalah
    #     @param depth - the current search depth
    #     @param start_time - time the move search began
    #     @param time_limit - the time limit of the search
    def minimax(self, a, b, a_fin, b_fin, depth, start_time, time_limit):
        if self.testIfTerminalState(a, a_fin, b_fin, depth, start_time, time_limit): # terminal state
            return -1 # invalid state
        
        v, move = self.maxValue(a, b, a_fin, b_fin, depth, start_time, time_limit, float('-inf'), float('inf'), -1, 0) # heuristic value and move to achieve it
        return move


    # This function returns the maximum heuristic value possible and the move that leads to the best state.
    #     @param a - an array of the number of stones in each of the player's holes
    #     @param b - an array of the number of stones in each of the opponent's holes
    #     @param a_fin - the number of stones in the player's kalah
    #     @param b_fin - the number of stones in the opponent's kalah
    #     @param depth - the current search depth
    #     @param start_time - time the move search began
    #     @param time_limit - the time limit of the search
    #     @param alpha - the alpha value used in alpha cutoff
    #     @param beta - the beta value used in beta cutoff
    #     @param move - a number from [0, 5] that represents the player hole to start the move in
    #     @param going_again - whether or not the current state is the result of a chained move
    def maxValue(self, a, b, a_fin, b_fin, depth, start_time, time_limit, alpha, beta, move, going_again):
        if(self.testIfTerminalState(a, a_fin, b_fin, depth, start_time, time_limit)): # terminal state
            return self.heuristic2(a, b, a_fin, b_fin, going_again), move # current heuristic value and move to reach it
        
        v = float('-inf') # heuristic value of search

        successors = self.getSuccessors(a) # legal next moves
        best_move = successors[0] # initialize best move (must be at least one move or the game is over)

        # TODO: pick and update best move, am i doing it right?
        for possible_move in successors: # for each own hole
            a_new, b_new, a_fin_new, b_fin_new, move_again = self.updateNewState(a, b, a_fin, b_fin, possible_move)
            if move_again == False: # not going again
                v_temp, move_temp = self.minValue(b_new, a_new, b_fin_new, a_fin_new, depth + 1, start_time, time_limit, alpha, beta, possible_move, 0)

                if(v_temp > v): # new best value
                    best_move = possible_move
                v = max(v, v_temp)
                
                if v >= beta: # beta cutoff
                    return v, best_move

                alpha = max(alpha, v)
            
            else: # going again
                v_temp, move_temp = self.maxValue(a_new, b_new, a_fin_new, b_fin_new, depth + 1, start_time, time_limit, alpha, beta, possible_move, 1)

                if(v_temp < v):
                    best_move = possible_move
                v = min(v, v_temp)
                
                if v <= alpha: # alpha cutoff
                    return v, best_move
                
                beta = min(beta, v)

        return v, best_move
    


    # This function returns the minimum heuristic value possible and the move that leads to the worst state.
    #     @param a - an array of the number of stones in each of the player's holes
    #     @param b - an array of the number of stones in each of the opponent's holes
    #     @param a_fin - the number of stones in the player's kalah
    #     @param b_fin - the number of stones in the opponent's kalah
    #     @param depth - the current search depth
    #     @param start_time - time the move search began
    #     @param time_limit - the time limit of the search
    #     @param alpha - the alpha value used in alpha cutoff
    #     @param beta - the beta value used in beta cutoff
    #     @param move - a number from [0, 5] that represents the player hole to start the move in
    #     @param going_again - whether or not the current state is the result of a chained move
    def minValue(self, a, b, a_fin, b_fin, depth, start_time, time_limit, alpha, beta, move, going_again):
        if(self.testIfTerminalState(a, a_fin, b_fin, depth, start_time, time_limit)): # terminal state
            return self.heuristic2(a, b, a_fin, b_fin, going_again), move # current heuristic value and move to reach it
        
        v = float('inf') # heuristic value

        successors = self.getSuccessors(a) # legal next moves
        best_move = successors[0] # initialize best move (must be at least one move or the game is over)
        
        for possible_move in successors: # for each valid successor
            a_new, b_new, a_fin_new, b_fin_new, move_again = self.updateNewState(a, b, a_fin, b_fin, possible_move)
            if move_again == False: # not going again
                v_temp, move_temp = self.maxValue(b_new, a_new, b_fin_new, a_fin_new, depth + 1, start_time, time_limit, alpha, beta, possible_move, 0)

                if(v_temp < v): # new worst heuristic
                    best_move = possible_move
                v = min(v, v_temp)
                
                if v <= alpha: # alpha cutoff
                    return v, best_move
                
                beta = min(beta, v)

            else: # going again 
                v_temp, move_temp = self.minValue(a_new, b_new, a_fin_new, b_fin_new, depth + 1, start_time, time_limit, alpha, beta, possible_move, 1)

                if(v > v_temp):
                    best_move = possible_move
                v = max(v, v_temp)
                
                if v >= beta: # beta cutoff
                    return v, best_move
                
                alpha = max(alpha, v)
            
        return v, best_move

    # This function returns the heuristic value of a given state by looking at the difference between the number of stones in the 
    #    player kalah vs the number of stones in the opponent kalah, the ability to chain moves, and the ability to capture holes.
    #     @param a - an array of the number of stones in each of the player's holes
    #     @param b - an array of the number of stones in each of the opponent's holes
    #     @param a_fin - the number of stones in the player's kalah
    #     @param b_fin - the number of stones in the opponent's kalah
    #     @param going_again - whether or not the current state is the result of a chained move
    def heuristic2(self, a, b, a_fin, b_fin, going_again):
        
        # a_sweep = 0
        # b_sweep = 0

        a_can_go_again = 0 # whether player can go again
        b_can_go_again = 0 # whether opponent can go again

        a_open = [] # player holes open to capture
        b_open = [] # opponent holes open to capture

        a_available = 0 # available player stones available to capture
        b_available = 0 # available opponent stones available to capture

        for i in range(len(a)): # for each hole
            if a[i] == 0: # if player hole is empty
                a_open.append(i) # add player hole capturable list
            if b[i] == 0: # opponent hole is empty
                b_open.append(i) # add opponent hole capturable list

        for open_opponent in b_open: # each opponent capturable hole
            for i in range(len(a)): # for each hole
                if a[i] - i - 1 == len(b) + open_opponent: # player hole accross from target opponent hole
                    a_available += b[open_opponent] - 1 # number of stones gained in capture

        for open_player in a_open: # each player capturable hole
            for i in range(len(b)): # for each hole
                if b[i] - i - 1 == len(a) + open_player: # opponent hole accross from target player hole
                    b_available += a[open_player] - 1 # number of stones gained in capture

        for i in range(len(a)): # for each hole
            if a[i] - i == len(a): # final stone lands in kalah
                a_can_go_again += 1 # increment move that can go again counter

        for i in range(len(b)): # for each hole
            if b[i] - i == len(b): # final stone lands in kalah
                b_can_go_again += 1 # increment move that can go again counter

        # if(len(a_open) == len(a)): 
        #     for i in range(len(a_open)): # for each hole
        #         b_sweep += b[i] # add b stones that can be swept
        
        # if(len(b_open) == len(b)): 
        #     for i in range(len(b_open)):# for each hole
        #         a_sweep += a[i] # add a stones that can be swept

        # sweep = 0.1 * (a_sweep - b_sweep)
        score = 0.5 * (a_fin - b_fin) # difference in player and opponent kalahs
        available = 0.05 * (a_available - 1.5 * b_available) # difference in stones available for capture 
        go_again = 0.1 * (a_can_go_again - b_can_go_again) # difference in whether a player or opponent can go again

        # print("Score: ", score, "Auxillary: ", available + go_again)
        return score + available + go_again #+ sweep