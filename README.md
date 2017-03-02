# Problem-solving-in-Python
Min-Max algorithm for tic-tac-toe  and logistic regresser
Implementation of Minimax algorithm and Alpha-Beta Minimax algorithm in Python.


To run type -

python3 ttt.py
---------------------------------------------------------------------
Input a value between 0-8, it will not accept other integer values, throughs error for string values.

First the human player enter one move. Let us input value is 0, then hit enter

computer will play the move using minimax and alpha beta algorithm, then it will ask for next move.

The game ends when a winner or tie situation is displayed.
----------------------------------------------------------------------

SAMPLE INPUTS - in order
0
6
4- Since place-4  already filled so, program will not accept it, enter again
3- Since place-3 already filled so, program will not accept it, enter again
2
8
----------------------------------------------------------------------

SAMPLE OUTPUT:

C:\Python34\python.exe "C:/Users/Nitin Patel/Desktop/sem3/FIS/Assignments/A2/ttt_2.py"
TIC-TAC-TOE
Human player start first:
Please enter your move(0-8): 0

X |   |  
  |   |  
  |   |  
Getting computer move for MINI-MAX

Number of search nodes for MINI-MAX:  59704

X |   |  
  | O |  
  |   |  
Getting computer move for Alpha-Beta-MINI-MAX

X |   |  
  | O |  
  |   |  
Number of search nodes for Alpha-Beta-MINI-MAX:  2337
Please enter your move(0-8): 6

X |   |  
  | O |  
X |   |  
Getting computer move for MINI-MAX

Number of search nodes for MINI-MAX:  926

X |   |  
O | O |  
X |   |  
Getting computer move for Alpha-Beta-MINI-MAX

X |   |  
O | O |  
X |   |  
Number of search nodes for Alpha-Beta-MINI-MAX:  188
Please enter your move(0-8): 4
Please enter your move(0-8): 3
Please enter your move(0-8): 2

X |   | X
O | O |  
X |   |  
Getting computer move for MINI-MAX

Number of search nodes for MINI-MAX:  33

X | O | X
O | O |  
X |   |  
Getting computer move for Alpha-Beta-MINI-MAX

X | O | X
O | O |  
X |   |  
Number of search nodes for Alpha-Beta-MINI-MAX:  14
Please enter your move(0-8): 8

X | O | X
O | O |  
X |   | X
Getting computer move for MINI-MAX

Number of search nodes for MINI-MAX:  2

X | O | X
O | O | O
X |   | X
Getting computer move for Alpha-Beta-MINI-MAX

X | O | X
O | O | O
X |   | X
Number of search nodes for Alpha-Beta-MINI-MAX:  2
Computer WINS..!!

Process finished with exit code 0

X |   |  
  | O |  
  |   |  
Number of search nodes for Alpha-Beta-MINI-MAX:  59704
Please enter your move(0-9): 1

X | X |  
  | O |  
  |   |  
Getting computer move for MINI-MAX

Number of search nodes for MINI-MAX:  934

X | X | O
  | O |  
  |   |  
Getting computer move for Alpha-Beta-MINI-MAX

X | X | O
  | O |  
  |   |  
Number of search nodes for Alpha-Beta-MINI-MAX:  934
Please enter your move(0-9): 4
Please enter your move(0-9): 5

X | X | O
  | O | X
  |   |  
Getting computer move for MINI-MAX

Number of search nodes for MINI-MAX:  43

X | X | O
  | O | X
O |   |  
Getting computer move for Alpha-Beta-MINI-MAX

X | X | O
  | O | X
O |   |  
Number of search nodes for Alpha-Beta-MINI-MAX:  43
Computer wins..!!

Process finished with exit code 0

-----------------------------------------------------------
