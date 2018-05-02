from random import randint


#Game states:
#0 - still going
#1 - player won: got tile 2048
#2 - game over and player lost

class Board:

    def __init__(self):
        #create new board
        self.score = 0 #player's score
        self.moves = 0 #number of moves
        self.board = [[None for y in range(4)] for x in range(4)] #board of game
        self.over = False #if the game is over
        self.state = 0

        #init board: assign 2 or 4 to random positions on board
        pos1 = 0
        pos2 = 0
        n1 = randint(0,1) * 2 + 2
        n2 = randint(0,1) * 2 + 2
        
        while(pos1 == pos2):
            pos1 = [randint(0,3), randint(0,3)]
            pos2 = [randint(0,3), randint(0,3)]

        self.board[pos1[0]][pos1[1]] = n1
        self.board[pos2[0]][pos2[1]] = n2
        

    # assign 2 or 4 to random positions on board
    def newNumber(self, board):
        if self.isFull(board):
            return board
        pos = [randint(0,3), randint(0,3)]
        n = randint(0,1) * 2 + 2
        
        while(board[pos[0]][pos[1]] != None):
            pos = [randint(0,3), randint(0,3)]

        board[pos[0]][pos[1]] = n

        return board


    #return indices of empty cells
    def getEmptyCells(self, board):
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == None:
                    empty_cells.append([i,j])

        return empty_cells

    #dir: direction to move
    #0 - up
    #1 - down
    #2 - left
    #3 - right
    def makeMove(self, board, score, dir):
        if(dir=='Up'):
            board, score, ifMoved = self.moveUp(board, score)
        elif(dir=='Down'):
            board, score, ifMoved = self.moveDown(board, score)
        elif(dir=='Left'):
            board, score, ifMoved = self.moveLeft(board, score)
        else:
            board, score, ifMoved = self.moveRight(board, score)

        if ifMoved:
            board = self.newNumber(board)

        if(self.isOver(board)):
            self.state = 2 if self.state == 0 else 1
            #print(board)
            #print('game over')
            return board, score
        else:
            return board, score


    #only makes moves without doing anything else
    #no checking if game is over, no inserting 2/4 on board
    def moveManager(self, board, score, dir):
        if(dir=='Up'):
            board, score, ifMoved = self.moveUp(board, score)
        elif(dir=='Down'):
            board, score, ifMoved = self.moveDown(board, score)
        elif(dir=='Left'):
            board, score, ifMoved = self.moveLeft(board, score)
        else:
            board, score, ifMoved = self.moveRight(board, score)

        return board, score
        

    # merge a matrix by row
    def merge(self, matrix, score):
        new_matrix = []
        for i in range(4):
            new_row = []
            prev = None
            for j in range(4):
                #prev is None
                if prev == None:
                    if matrix[i][j] != None:
                        prev = matrix[i][j]
                        new_row.append(prev)
                    else:
                        continue
                #prev != None
                else:
                    if prev == matrix[i][j]:
                        #merge:
                        #remove newly appended item from new_row
                        new_row = new_row[:-1]
                        new_row.append(prev * 2)
                        score += prev * 2
                        #if state needs to change
                        if prev * 2 >= 2048:
                            self.state = 1
                        prev = None
                    elif matrix[i][j] != None:
                        prev = matrix[i][j]
                        new_row.append(prev)
            
            #append new row to new matrix
            while(len(new_row) < 4):
                new_row.append(None)

            new_matrix.append(new_row)

        ifMoved = not(new_matrix == matrix)

        return new_matrix, score, ifMoved


    def transpose(self, matrix):
        new_matrix = [[matrix[j][i] for j in range(4)] for i in range(4)]
        return new_matrix

    
    def moveUp(self, board, score):
        board, score, ifMoved = self.merge(self.transpose(board), score)
        return self.transpose(board), score, ifMoved


    def moveDown(self, board, score):
        new_board = board
        new_board = self.transpose(new_board)
        for i in range(4):
            new_board[i].reverse()
        new_board, score, ifMoved = self.merge(new_board, score)
        for j in range(4):
            new_board[j].reverse()
        return self.transpose(new_board), score, ifMoved


    def moveLeft(self, board, score):
        return self.merge(board, score)


    def moveRight(self, board, score):
        new_board = board
        for j in range(4):
            new_board[j].reverse()
        new_board, score, ifMoved = self.merge(new_board, score)
        for i in range(4):
            new_board[i].reverse()
        return new_board, score, ifMoved


    #checks if the board is full
    def isFull(self, board):
        full = True
        for i in range(4):
            full = full and (None not in board[i])
        return full


    #assume the board is full, check if there are available moves
    def isMovable(self, board):
        movable = False
        for i in range(3):
            for j in range(4):
                if j == 3:
                    movable = movable or board[i][j] == board[i+1][j]
                else:
                    movable = movable or (
                        board[i][j] == board[i+1][j] or
                        board[i][j] == board[i][j+1])
        for i in range(3):
            movable = movable or board[3][i] == board[3][i+1]

        return movable


    def isOver(self, board):
        return self.isFull(board) and not self.isMovable(board)


##    #check if the given index is on board
##    def validIndex(self, x, y):
##        return x in range(4) and y in range(4)
##
##    #return a list of index of neighbor tiles of the given index
##    def neighbors(self, x, y):
##        neighbors = []
##        if validIndex(x, y):
##            if validIndex(x - 1, y):
##                neighbors.add(x - 1, y)
##            if validIndex(x + 1, y):
##                neighbors.add(x + 1, y)
##            if validIndex(x, y - 1):
##                neighbors.add(x, y - 1)
##            if validIndex(x, y + 1):
##                neighbors.add(x, y + 1)
##        return neighbors



    def getBoard(self):
        return self.board
    






########################################################
################       TEST         ####################
########################################################
    
    #for test purposes - merge
    def test(self):
##        b= self.board
##        print('original board:\n', b, '\n')
##        print('move up:\n', self.moveUp(b), '\n')
##        print('move down:\n', self.moveDown(b), '\n')
##        print('move left:\n', self.moveLeft(b), '\n')
##        print('move right:\n', self.moveRight(b), '\n')
##        print('original board again:\n', b, '\n')
##        print('\nNow let\'s try makeMove:\n')
##        print('move up:\n', self.makeMove(b,0), '\n') #up
##        print('move down:\n', self.makeMove(b,1), '\n') #down
##        print('move left:\n', self.makeMove(b,2), '\n') #left
##        print('move right:\n', self.makeMove(b, 3), '\n') #right
##        print('original board again:\n', b, '\n')

        a = [[2,4,16,8],
             [4,8,2,4],
             [2,16,4,2],
             [128,2,16,4]]
        b = [[2,4,16,8],
             [4,8,2,4],
             [2,16,2,2],
             [128,2,16,4]]
        c = [[2,4,16,8],
             [4,8,2,4],
             [2,16,4,2],
             [128,2,4,4]]
        d = [[2,4,16,8],
             [4,8,2,4],
             [2,16,4,2],
             [128,2,16,16]]
        
        
##        print('if a is movable:', self.isMovable(a))
##        print('if a is full:', self.isFull(a))
##        print('if a is over:', self.isOver(a))
##        print('\n')
##        
##        print('if b is movable:', self.isMovable(b))
##        print('if b is full:', self.isFull(b))
##        print('if b is over:', self.isOver(b))
##        print('\n')
##        
##        print('if c is movable:', self.isMovable(c))
##        print('if c is full:', self.isFull(c))
##        print('if c is over:', self.isOver(c))
##        print('\n')
##        
##        print('if d is movable:', self.isMovable(d))
##        print('if d is full:', self.isFull(d))
##        print('if d is over:', self.isOver(d))
##

        print('a:', a, '\n')
        print('merge a:', self.makeMove(a, 0, 1))
        print('\n')
        print('b:', b, '\n')
        print('merge b:', self.makeMove(b, 0, 2)) #left
        print('\n')
        print('c:', c, '\n')
        print('merge c up:', self.makeMove(c, 0, 0)) #up
        print('merge c right:', self.makeMove(c, 0, 3)) #right
        print('merge c left:', self.makeMove(c, 0, 2)) #left
        print('\n')
        print('d:', d, '\n')
        print('merge d left:', self.makeMove(d, 0, 2)) #left

        return 'ok'
        
    
