####################################################################################################
# MinimAx algorithm and Alpha-Beta-Minimax algorithm implementation in python.
#
#Uses : Python3 ttt.py
#
#Author: Virendra Rajpurohit
#FIS - Assignment 2
#Date - 21 Sept 2015
###################################################################################################
import sys
#global count used to keep count of generated search nodes for each move
count=0

#Check for ROW, Column, Diagonals for winning matches
def check_terminals(tictactoe,config):
    if (tictactoe[config[0]]==tictactoe[config[1]]==tictactoe[config[2]] and tictactoe[config[0]]!=' '):
        return True
    return False

# To return utility function. return 1,-1,0 in case user wins, computer win or tie respectively.
def utility(tictactoe):
    terminals = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                 [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for config in terminals:
        if check_terminals(tictactoe,config):
            if tictactoe[config[0]]=='X':
                return -1
            else:return 1
    return 0

#Check if the tic-tac-toe is already full
def is_full(tictactoe):
    not_full=True
    for i in range(9):
        if(tictactoe[i]==' '):
            return False
    return not_full
#to copy the board from given
def duplicate_board(tictactoe):
    new_board=[]
    for i in tictactoe:
        new_board.append(i)
    return new_board

#To generates the successors of the given state
def gen_child(tictactoe,player):
    ch_list=[]
    for i in range(9):
        copy1=[]
        if(tictactoe[i]==' '):
            copy1=duplicate_board(tictactoe)
            copy1[i]=player
            ch_list.append(copy1)
    return ch_list

# To check all terminal conditions.(Rows, Columns, Diagonals, Full_board)
def TERMINAL_TEST(tictactoe):
    terminals = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                 [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for config in terminals:
        if check_terminals(tictactoe,config):
            return True
    if(is_full(tictactoe)):
        return True
    else:
        return False

#Minimax - MAX_val function
#Returns the maximum value for all successor in the given state
def MAX_VAL(tictactoe):
    if TERMINAL_TEST(tictactoe):
        return utility(tictactoe),tictactoe
    v=-sys.maxsize
    child=gen_child(tictactoe,'O')
    ch_board=[]
    for ch in child:
        global count
        count+=1
        p_val,ch_val=MIN_VAL(ch)
        if(v<p_val):
            v=p_val
            ch_board=ch
    return v,ch_board

#Minimax - MIN_val function
#Returns the minimum value for all successor in the given state
def MIN_VAL(tictactoe):
    if TERMINAL_TEST(tictactoe):
        return utility(tictactoe),tictactoe
    v=sys.maxsize
    child=gen_child(tictactoe,'X')
    ch_board=[]
    for ch in child:
        global count
        count+=1
        p_val,ch_val=MAX_VAL(ch)
        if(v>p_val):
            v=p_val
            ch_board=ch
    return v,ch_board

#minimax algorithm implementation
def minimax(tictactoe):
    #get the best move by calling MAX_VAL function
    best_move,new_Brd=MAX_VAL(tictactoe)
    return best_move,new_Brd

#Alpha-Beta-Minimax - alpha_beta_MAX_val function
#Returns the maximum value for all successor in the given state with prunning
def AB_MAX_VAL(tictactoe,a,b):
    if TERMINAL_TEST(tictactoe):
        return utility(tictactoe),tictactoe
    v=-sys.maxsize
    child=gen_child(tictactoe,'O')
    ch_board=[]
    for ch in child:
        global count
        count+=1
        p_val,ch_val=AB_MIN_VAL(ch,a,b)
        if(v<p_val):
            v=p_val
            ch_board=ch
        if(v>=b):
            return v,tictactoe
        if(a<v):
            a=v

    return v,ch_board

#Alpha-Beta-Minimax - Alpha-Beta-MIN_val function
#Returns the minimum value for all successor in the given state with prunning
def AB_MIN_VAL(tictactoe,a,b):
    if TERMINAL_TEST(tictactoe):
        return utility(tictactoe),tictactoe
    v=sys.maxsize
    child=gen_child(tictactoe,'X')
    ch_board=[]
    for ch in child:
        global count
        count+=1
        p_val,ch_val=AB_MAX_VAL(ch,a,b)
        if(v>p_val):
            v=p_val
            ch_board=ch
        if(v<=a):
            return v,tictactoe
        if(b>v):
            b=v
    return v,ch_board

 #Alpha-Beta-minimax with prunning algorithm implementation
def AB_minimax(tictactoe):
    #get the best move by calling AB_MAX_VAL function
    best_move,new_Brd=AB_MAX_VAL(tictactoe,-sys.maxsize,sys.maxsize)
    return best_move,new_Brd

#to print the Tic-Tac-Toe state in 3X3 matrix form.
def print_board(tictactoe):
    for i in range(3):
        print('')
        for j in range(3):
            print(tictactoe[i*3+j],end="")
            if(j<2):
                print(' | ',end="")

#main() fuction
def main():
    global count
    count=0
    print('TIC-TAC-TOE\nHuman player start first:')
    game=True
    player=1
    tictactoe =[]
    for i in range(9):
        in1=' '
        tictactoe.append(in1)
    #Loop till a terminal state has been reached.
    while (TERMINAL_TEST(tictactoe)==False):
        #clear the counter for search node count for a move.
        count=0
        human_move = input('Please enter your move(0-8): ')
        #check if the position is empty - if the move is possible
        if(int(human_move) in range(9)):
            if(tictactoe[int(human_move)]==' '):
                tictactoe[int(human_move)]='X'
                print_board(tictactoe)
                print('\nGetting computer move for MINI-MAX')
                comp_move,brd=minimax(tictactoe)
                print('\nNumber of search nodes for MINI-MAX: ', count)
                print_board(brd)
                #reset count for counting number of generated search nodes for alpha beta pruning
                count=0
                print('\nGetting computer move for Alpha-Beta-MINI-MAX')
                comp_move1,brd1=AB_minimax(tictactoe)
                print_board(brd1)
                print('\nNumber of search nodes for Alpha-Beta-MINI-MAX: ', count)
                #Update board with new value
                tictactoe=duplicate_board(brd)

    if(utility(tictactoe)==-1):
        print('Human Player WINS..!!')
    elif(utility(tictactoe)==1):
        print('Computer WINS..!!')
    else:
        print('Its a TIE..!!')
main()