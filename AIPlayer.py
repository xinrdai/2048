from Board import *
import math


##d = [[2,None,None,8],
##     [4,8,2,None],
##     [2,None,None,2],
##     [128,None,16,16]]
##newb = Board()
##newb.board = d

dirs = ['Up', 'Down', 'Left', 'Right']

class AIPlayer:
    def __init__(self, b):
        #init board
        self.b = b
        self.board = b.board
        self.score = b.score
        self.state = b.state
        self.moves = b.moves





    #check if the given index is on board
    def validIndex(self, x, y):
        return x in range(4) and y in range(4)

    #return a list of index of neighbor tiles of the given index
    def neighbors(self, x, y):
        neighbors = []
        if self.validIndex(x, y):
            if self.validIndex(x - 1, y):
                neighbors.append([x - 1, y])
            if self.validIndex(x + 1, y):
                neighbors.append([x + 1, y])
            if self.validIndex(x, y - 1):
                neighbors.append([x, y - 1])
            if self.validIndex(x, y + 1):
                neighbors.append([x, y + 1])
        return neighbors





    def heuristic(self, board):
        #using a weight matrix for calculating h value
        #                   {6 5 4 3}
        #                   {5 4 3 2}
        #   weight matrix = {4 3 2 1}
        #                   {3 2 1 0}
        w = [[100, 70, 40, 20],
             [70, 40, 20, 5],
             [40, 20, 5, 1],
             [20, 5, 1, 0]]

        score = 0
        penalty = 0


        for i in range(4):
            for j in range(4):
                num = board[i][j] if board[i][j] != None else 0
                score += num * w[i][j]
                ns = self.neighbors(i,j)
                for neighbor in ns:
                    n = board[neighbor[0]][neighbor[1]] if board[neighbor[0]][neighbor[1]] != None else 0
                    penalty += abs(n - num)


        return score - penalty



    def expectimax(self, b, depth, isPlayer):
        if depth == 0:
            return None, self.heuristic(b.board)

        board = b.board
        children = []
        move = None
        score = -math.inf
        
        #player's turn
        if isPlayer:
            #get children: [up, down, left, right]
            for i in range(4):
                childB = b
                childB.board, childB.score = childB.makeMove(childB.board, childB.score, dirs[i])
                children.append(childB)

            #get score
            for i in range(4):
                childB = children[i]

                #game over; 2048 not reached
                if childB.isOver:
                    for row in childB.board:
                        if 2048 in row:
                            return dirs[i], score
                        else:
                            continue

                tempMove, tempScore = self.expectimax(childB, depth-1, not isPlayer)
                if tempScore > score:
                    score = tempScore
                    move = dirs[i]

            return move, score
        
        #board's turn
        else:
            score = 0
            empty_cells = b.getEmptyCells(b.board)
            emptyN = len(empty_cells)
            
            #assign weight*score to 2/4 in empty cells
            for i in range(emptyN):
                x, y = empty_cells[i][0], empty_cells[i][1]
                
                #insert 4
                child4 = b
                child4.board[x][y] = 4
                tempMove, tempScore = self.expectimax(child4, depth-1, not isPlayer)
                score += .1 * tempScore if tempScore != -math.inf else 0

                #insert 2
                child2 = b
                child2.board[x][y] = 2
                tempMove, tempScore = self.expectimax(child2, depth-1, not isPlayer)
                score += .9 * tempScore if tempScore != -math.inf else 0

            #get weighted average
            score /= emptyN if emptyN != 0 else 1

            return move, score


    def findMove(self):
        score = -math.inf
        move = None
        depth = 10
        isPlayer = True

        for i in range(4):
            newb = self.b
            newb.board, s = newb.makeMove(newb.board, newb.score, dirs[i])
            if newb.isOver(newb.board):
                continue

            tempMove, newScore = self.expectimax(newb, depth - 1, not isPlayer)

            if newScore > score:
                score = newScore
                move = tempMove
        
        return move

##    def play(self):
##        isPlayer = True
##        
##        while(True):
##            if isPlayer:
##                move = self.findMove()
##
##            self.b.board, self.b.score = self.b.makeMove(self.b.board, self.b.score, move)
##            if self.b.state == 2:
##                #print('game over')
##                break


    def test(self):
##        d = [[2,4,16,8],
##             [4,8,2,4],
##             [2,16,4,2],
##             [128,2,16,16]]
##        self.b = Board()
##        self.b.board = d
##        self.board = b.board
##        self.score = b.score
##        self.state = b.state
        self.play()




##g=AIPlayer(newb)
##g.play()
