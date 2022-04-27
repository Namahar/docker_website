from sudoku import Sudoku

def check(board, row, col, value):
   ''' check that new value is valid on board '''

   # check row is valid
   for i in range(9):
      if board[row][i] == value and col != i:
         return False

   # check that column is valid
   for i in range(9):
      if board[i][col] == value and row != i:
         return False

   # check square is valid
   square_r = row // 3
   square_c = col // 3

   for r in range(square_r*3, square_r*3 + 3):
      for c in range(square_c*3, square_c*3 + 3):
         if board[r][c] == value and r != row and c != col:
            return False

   return True

def find_cell(board):
   ''' finds an empty cell on the board '''

   for r in range(9):
      for c in range(9):
         if board[r][c] == None:
            return (r, c)

   return None

def solver(board, states):

   # get empty square
   empty = find_cell(board)

   if not empty:
      return True
   else:
      row, col = empty
      
   # check all possible solutions
   for i in range(1, 10):
      
      if check(board, row, col, i):
         board[row][col] = i

         temp = [r[:] for r in board]
         states.append(temp)
         
         if solver(board, states):
            return True

         board[row][col] = None
         
         # temp = [r[:] for r in board]
         # states.append(temp)

   return False

def get_board():
   return Sudoku(3).difficulty(0.6).board

def solver_wrapper(board):

   states = []
   solver(board, states)

   return states
