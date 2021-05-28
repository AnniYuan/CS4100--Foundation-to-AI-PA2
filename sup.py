class GameState:
    '''
    A GameState contains a 3 x 3 grid which represents the board, if the position == True then it is an empty cell
    There are two players x and o, turn represents whose turn it is
    Numberx represents the number of steps x has taken (number of x represents in the grid)
    Numbery represents the number of steps y has taken (number of y represents in the grid)
    isTermimate represente the game termination, the gane is terminated if the grid is fully occupied or has a winner
    '''

    def __init__(self):
        grid = []
        for row in range(3):
            grid = grid + [[]]
            for col in range(3):
                grid[row] = grid[row] + [' ']
        self.grid = grid
        self.numberx = 0
        self.numbero = 0
        self.isTerminate = False
        if self.numbero == self.numberx:
            self.turn = 'x'
        else: self.turn = 'o'


    #deep_copy, return a new gamstate with the input grid
    def copy_grid(self, grid):
        self.grid = [x[:] for x in grid]
        self.numberx = 0
        self.numbero = 0
        for row in grid:
            for cell in row:
                if cell == 'x':
                    self.numberx += 1
                elif cell == 'o':
                    self.numbero += 1
        if self.numberx + self.numbero == 9 or self.utility() == 1 or self.utility() == -1:
            self.isTerminate = True
        else:
            self.isTerminate = False
        if self.numbero == self.numberx:
            self.turn = 'x'
        else:
            self.turn = 'o'
        return self

    def __str__(self):
        string = 'grid:'
        for row in self.grid:
            string = string+ '\n' + str(row)
        string += '\n #x: ' + str(self.numberx) + ' #o: ' + str(self.numbero)
        string += '\n whose turn: ' + self.turn
        string += '\n Termination: ' + str(self.isTerminate)
        return string

    # If current turn is o change to x, vise versa
    def switchplayer(self):
        if self.turn == 'o':
            self.turn = 'x'
        elif self.turn == 'x':
            self.turn = 'o'

    # mark the current turn(x or o) to the board at postion pos
    def moveAgent(self, pos):
        x,y = pos
        turn = self.turn
        if self.grid[x][y] == ' ' and turn == 'x':
            self.grid[x][y] = 'x'
            self.numberx += 1
            self.switchplayer()
            self.utility()
        elif self.grid[x][y] == ' ' and turn == 'o':
            self.grid[x][y] = 'o'
            self.numbero += 1
            self.switchplayer()
            self.utility()
        else:
            raise Exception('Action for '+ str(turn)+ ' is invalid: Position ' + str(pos) + ' is already occupied.')

    def utility(self):
        row0, row1, row2 = self.grid
        #cross win
        if row0[0] == row1[1] == row2[2] == 'x' or row0[2] == row1[1] == row2[0] == 'x':
            self.isTerminate = True
            return 1
        if row0[0] == row1[1] == row2[2] == 'y' or row0[2] == row1[1] == row2[0] == 'o':
            self.isTerminate = True
            return -1
        #horizontal win
        for row in self.grid:
            if row[0] == row[1] == row[2] and row[0] == 'x':
                self.isTerminate = True
                return 1
            if row[0] == row[1] == row[2] and row[0] == 'o':
                self.isTerminate = True
                return -1
        #vertical win
        for i in range(0,3):
            if row0[i] == row1[i] == row2[i] == 'x':
                self.isTerminate = True
                return 1
            if row0[i] == row1[i] == row2[i] == 'o':
                self.isTerminate = True
                return -1
        if self.numbero + self.numberx == 9:
            self.isTerminate = True
            return 0
        return None

    def minmax(self):
        if self.turn == 'x':
            return self.max_value()
        if self.turn == 'o':
            return self.min_value()

    def max_value(self):
        sucessors = self.generate_succesor()
        if self.isTerminate:
            return self.utility()
        maxV = max([s.minmax() for s in sucessors])
        # print('This is selecting maxV for below grid, mav is ' + str(maxV))
        # print(self.__str__())
        # for s in sucessors:
        #     if s.minmax() == maxV:
        #         print(s.__str__())
        #         break
        return maxV

    def min_value(self):
        sucessors = self.generate_succesor()
        if self.isTerminate:
            return self.utility()
        minV = min([s.minmax() for s in sucessors])
        return minV


    # if the game has not terminated, return a list of positions for the current player. Otherwise return empty list
    def avaliable_cells(self):
        if self.isTerminate:
            return[]
        cells = []
        grid = self.grid
        for row in range(0,3):
            for col in range(0,3):
                if grid[row][col] == ' ':
                    pos = (row,col)
                    cells.append(pos)
        return cells


    #return a list of successor gamestates
    def generate_succesor(self):
        s = []
        avaliable_moves = self.avaliable_cells()
        for pos in avaliable_moves:
            grid = self.grid.copy()
            g_copy = GameState().copy_grid(grid)
            g_copy.moveAgent(pos)
            s.append(g_copy)
        return s

grids0 = [[' ', ' ', ' '],
          [' ', ' ', ' '],
          [' ', ' ', ' ']]

grids1 = [[' ', ' ', ' '],
          [' ', ' ', ' '],
          [' ', ' ', 'x']]

grids2 = [['o', ' ', ' '],
          [' ', ' ', ' '],
          [' ', ' ', 'x']]

grids3 = [['o', ' ', ' '],
          ['x', ' ', ' '],
          [' ', ' ', 'x']]

grids4 = [['o', 'o', ' '],
          ['x', ' ', ' '],
          [' ', ' ', 'x']]

grids5 = [['o', 'o', 'x'],
          ['x', ' ', ' '],
          [' ', ' ', 'x']]

grids6 = [['o', 'o', 'x'],
          ['x', ' ', 'o'],
          [' ', ' ', 'x']] #-> 1

grids4_2 = [['o', ' ', ' '],
            ['x', 'o', ' '],
            [' ', ' ', 'x']]

gridstest = [['o', 'o', 'x'],
            [' ', 'x', ' '],
            ['o', 'x', ' ']]
gs0 = GameState().copy_grid(grids0)
gs1 = GameState().copy_grid(grids1)
gs2 = GameState().copy_grid(grids2)
gs3 = GameState().copy_grid(grids3)
gs4 = GameState().copy_grid(grids4)
gs5 = GameState().copy_grid(grids5)
gs6 = GameState().copy_grid(grids6)
gs4_2 = GameState().copy_grid(grids4_2)
test = GameState().copy_grid(gridstest)
#print(test.minmax())

'''
Q3 verification
'''
#print(gs6.minmax())
#print(gs0.minmax())

'''
Q4 output for below:

S0:  0 (max, x's turn)
S1:  0 (min, o's turn)
S2:  1 (max, x's turn)
S3:  0 (min, o's turn)
S4:  1 (max, x's turn)
S5:  1 (min, o's turn)
S6:  1 (max, x's turn)

S1 -> S2 is a suboptimal move played by o, below is a optimal move:
[[' ', ' ', ' '],
 [' ', 'o', ' '],
 [' ', ' ', 'x']]
 
S2-> S3 is a suboptimal move played by x, below is a optimal move:
[['o', ' ', 'x'],
 [' ', ' ', ' '],
 [' ', ' ', 'x']]
 
 [['o', ' ', ' '],
  [' ', ' ', ' '],
  ['x', ' ', 'x']]
S3-> S4 is a suboptimal move played by o, below is a optimal move:
[['o', ' ', 'o'],
 ['x', ' ', ' '],
 [' ', ' ', 'x']]
            
[['o', ' ', ' '],
 ['x', ' ', 'o'],
 [' ', ' ', 'x']] 
            
[['o', ' ', ' '],
 ['x', 'o', ' '],
 [' ', ' ', 'x']]

'''

# print('S0: ',gs0.minmax())
# print('S1: ',gs1.minmax())
# print('S2: ',gs2.minmax())
# print('S3: ',gs3.minmax())
# print('S4: ',gs4.minmax())
# print('S5: ',gs5.minmax())
# print('S6: ',gs6.minmax())
print('S3_2: ',gs4_2.minmax()) #-> 1
