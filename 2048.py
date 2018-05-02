from tkinter import *
from Board import *
from AIPlayer import *

#Game states:
#0 - still going
#1 - game over and player won
#2 - game over and player lost
STATES = [0, 1, 2]
HOW_TO_PLAY = """HOW TO PLAY: Use your arrow keys to move the tiles. When
two tiles with the same number touch, they merge into one!"""
ICON = '2048            '
BG_COLOR = 'linen'
icon_color = 'brown4'
cell_colors = {None: 'old lace', #cells without nums
               2: 'wheat1', 4: 'wheat2',
               8: 'coral1', 16: 'coral2', 32: 'coral3', 64: 'OrangeRed2',
               128: 'goldenrod1', 256: 'goldenrod2', 512: 'goldenrod3',
               1024: 'DarkGoldenrod1', 2048: 'DarkGoldenrod2'}
big_num_color = 'red2'
border_color = 'NavajoWhite4'
number_color = 'salmon4'
new_game_color = 'saddle brown'


class Game:
    def __init__(self, master):
        #init game
        self.b = Board()
        self.board = self.b.board
        self.score = self.b.score
        self.bestScore = self.b.score
        self.state = STATES[0]


        #init AI Player
        #self.ai = AIPlayer(self.board)

##        tempb = [[2,1024,64,8],
##                 [2048,8,2,4],
##                 [2,256,4,512],
##                 [128,4000,16,32]]


        #init GUI
        #tk layout
        self.root = master
        self.root.title('2048')
        self.root.geometry('660x800') #width=630, height=700

        
        #top frame - 600x100, x:30, y:30
        self.topFrame = Frame(self.root, width=600, height=150, bg=BG_COLOR)
        #icon
        self.iconLabel = Label(self.topFrame,
                               text=ICON, font=(None, 60, 'bold'),
                               fg=icon_color, bg=BG_COLOR)
        self.iconLabel.place(x=20,y=10)
        #score
        self.scoreLabel = Label(self.topFrame,
                                text='Score:\n'+str(self.score), font=(None, 18),
                                fg='white', bg=border_color)
        self.scoreLabel.place(x=330,y=30, width=80, height=50)
        #best score
        self.bestScoreLabel = Label(self.topFrame,
                                    text='Best:\n'+str(self.bestScore), font=(None, 18),
                                    fg='white', bg=border_color)
        self.bestScoreLabel.place(x=450,y=30, width=80, height=50)
        #new game
        self.newGameButton = Button(self.topFrame,
                                    text='New Game', font=(None, 20),
                                    command=self.newGame)
        self.newGameButton.place(x=400, y=100) #width=120, height=50)
        #AI player
        self.aiButton = Button(self.topFrame,
                               text="AI Player", font=(None, 20),
                               command=self.aiPlayer)
        self.aiButton.place(x=250, y=100)


        #board frame - 600x420
        self.boardFrame = Frame(self.root, width=600, height=500, bg=BG_COLOR)
        #border label
        self.borderLabel = Label(self.boardFrame, bg=border_color)
        self.borderLabel.place(x=70,y=20,width=450, height=450)
        #cell label - draw board
        self.drawBoard()

        #bottomFrame - 600x150
        self.bottomFrame = Frame(self.root, width=600, height=150)
        #howLabel
        self.howToLabel = Label(self.bottomFrame, justify=LEFT,
                                text=HOW_TO_PLAY, font=("Adobe Calson Pro", 16),
                                fg=number_color, bg=BG_COLOR)
        self.howToLabel.place(x=0,y=0,width=600,height=100)

        #key events
        self.root.bind('<Key>', self.keyPressed)


        self.topFrame.pack()
        self.boardFrame.pack()
        self.bottomFrame.pack()
        
        self.drawBoard()

        

    #AI Player
    def aiPlayer(self):
        ai = AIPlayer(self.b)
        isPlayer = True
        
        while(True):
            if isPlayer:
                move = ai.findMove()

            self.b.board, self.b.score = self.b.makeMove(self.b.board, self.b.score, move)
            self.board = self.b.board
            self.score = self.b.score
            self.drawBoard()
            if self.b.state == 2:
                self.b.state = 0
                #print('game over')
                continue

            if self.b.state == 1:
                break

            for row in self.b.board:
                if 2048 in row:
                    self.drawBoard()
                    break
            

    

    #key pressed, board changes
    def keyPressed(self,event):
        self.board, self.score = self.b.makeMove(self.board, self.score, event.keysym)
        self.drawBoard()
        #game over and player lost
        if self.b.state == 2:
            self.overLabel = Label(self.topFrame,
                                   text='Game over. You lost!', font=(None, 20),
                                   fg='red', bg=BG_COLOR)
            self.overLabel.place(x=20, y=100)
        elif self.b.state == 1:
            self.overLabel = Label(self.topFrame,
                                   text='Congrats!\nYou reached 2048.', font=(None, 20),
                                   fg='blue', bg=BG_COLOR)
            self.overLabel.place(x=20,y=100)
        



    def gameState(self):
        if self.b.state == 2:
            self.overLabel = Label(self.topFrame,
                                   text='Game over. You lost!', font=(None, 20),
                                   fg='red', bg=BG_COLOR)
            self.overLabel.place(x=20, y=100)
        elif self.b.state == 1:
            self.overLabel = Label(self.topFrame,
                                   text='Congrats!\nYou reached 2048.', font=(None, 20),
                                   fg='blue', bg=BG_COLOR)
            self.overLabel.place(x=20,y=100)

    #new game button pressed
    def newGame(self):
        self.bestScore = self.score if self.score > self.bestScore else self.bestScore
        self.b = Board()
        self.score = self.b.score
        self.board = self.b.board
        self.state = STATES[0]
        self.overLabel = None
        self.drawBoard()
        self.gameState()


    #draw board on screen
    def drawBoard(self):
        #board
        bx = 70
        by = 20
        cells = []
        for i in range(4):
            for j in range(4):
                num = self.board[i][j]
                color = cell_colors[num] if num in cell_colors else 'red2'
                cellLabel = Label(self.boardFrame,
                                  text = num,
                                  font = (None, 28, 'bold'),
                                  fg = 'white', bg = color)
                cells.append(cellLabel)
                cellLabel.place(x=bx+10*(j+1)+j*100, y=by+10*(i+1)+i*100, width=100, height=100)

        self.scoreLabel = Label(self.topFrame,
                                text='Score:\n'+str(self.score), font=(None, 18),
                                fg='white', bg=border_color)
        self.scoreLabel.place(x=330,y=30, width=80, height=50)
        self.bestScoreLabel = Label(self.topFrame,
                                    text='Best:\n'+str(self.bestScore), font=(None, 18),
                                    fg='white', bg=border_color)
        self.bestScoreLabel.place(x=450,y=30, width=80, height=50)

        #game state
        if self.b.state == 2:
            self.overLabel = Label(self.topFrame,
                                   text='Game over. You lost!', font=(None, 20),
                                   fg='red', bg=BG_COLOR)
            self.overLabel.place(x=20, y=100)
        elif self.b.state == 1:
            self.overLabel = Label(self.topFrame,
                                   text='Congrats!\nYou reached 2048.', font=(None, 20),
                                   fg='blue', bg=BG_COLOR)
            self.overLabel.place(x=20,y=100)
        else:
            self.overLabel = None







########################################################
################       TEST         ####################
########################################################
        
    def test(self, n):
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

        boards = [a, b, c, d]
        self.drawBoard(boards[n])
        
        


root = Tk()
game = Game(root)
root.mainloop()
