import numpy
import random


WIN_LENGTH = 4
NUM_ROWS = 6
NUM_COLS = 7
RED = 1
BLUE = -1

    
class ConnectFourGame:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.board = numpy.zeros([NUM_ROWS, NUM_COLS], dtype=int)
        self.colheights = [0] * NUM_COLS
        self.history = []
        self.winner = 0
        self.verbose = 0
        
    def algoMove(self, player):
        
        preferredCol = []
        openCol = []
        endCol = []
        for i in range(NUM_COLS):
            if self.colheights[i] < NUM_ROWS:
                if self.isNearSameColor(player, i):
                    preferredCol.append(i)
                elif i != 0 and i != NUM_COLS-1:
                    openCol.append(i)
                else:
                    endCol.append(i)
        nextMove = -1
        # Mimic a simple probability distribution to favor preferred cols
        # while allowing for more diversity of moves.
        prefMult = 10
        openMult = 2
        endMult = 1
        choiceRange = [len(preferredCol)*prefMult, len(openCol)*openMult, len(endCol)*endMult]
        if sum(choiceRange) == 0:
            return False
        
        randMove = random.randint(1, sum(choiceRange))
        
        if randMove <= choiceRange[0]:
            nextMove = random.choice(preferredCol)
        elif randMove <= sum(choiceRange[:2]):
            nextMove = random.choice(openCol)
        else:
            nextMove = random.choice(endCol)
        # if len(preferredCol) > 0:
        #     nextMove = random.choice(preferredCol)
        # elif len(openCol) > 0:
        #     nextMove = random.choice(openCol)
        # elif len(endCol) > 0:
        #     nextMove = random.choice(endCol)
        # else:
        #     return False
            
        self.board[self.colheights[nextMove], nextMove] = player
        self.colheights[nextMove] += 1
        return True
        
    # Simple model move that always takes the highest probability prediction.
    def modelMove(self, player, model):
        moves = []
        playerDex = 0 if player == 1 else 1
        for i in range(NUM_COLS):
            if self.colheights[i] < NUM_ROWS:
                mBoard = numpy.copy(self.board.reshape(1, 6, 7))
                mBoard[0, self.colheights[i], i] = player
                pred = model.predict(numpy.array([mBoard]), 1, 0)
                moves.append((i,pred[0, playerDex]))
                
        if len(moves) == 0:
            return False
        moves.sort(key=lambda x: x[1], reverse=True)

        nextMove = moves[0][0]

        self.board[self.colheights[nextMove], nextMove] = player
        self.colheights[nextMove] += 1
        return True
        
    # Randomly chooses a model move from a probability distribution of available moves.
    # Allows for diversity of model moves while still favoring whatever the network predicts.
    # Prevents model v. model games from being completely deterministic.
    # Experimental. A trained model using this as is performs very poorly.
    def modelPMove(self, player, model):
        moves = []
        playerDex = 0 if player == 1 else 1
        for i in range(NUM_COLS):
            if self.colheights[i] < NUM_ROWS:
                mBoard = numpy.copy(self.board.reshape(1, 6, 7))
                mBoard[0, self.colheights[i], i] = player
                pred = model.predict(numpy.array([mBoard]), 1, 0)
                moves.append((i,pred[0, playerDex]))
                
        if len(moves) == 0:
            return False
        moves.sort(key=lambda x: x[1], reverse=True)

        if(self.verbose):
            print moves
        pRange = sum([p for _, p in moves])
        pMove = random.uniform(0, pRange)
        
        nextMove = -1
        runningTotal = 0
        for i, p in moves:
            runningTotal += p
            if pMove < runningTotal:
                nextMove = i
                break

        # Fallback to last move in case of weird float comparison.
        if nextMove == -1:
            nextMove = moves[-1][0]

        self.board[self.colheights[nextMove], nextMove] = player
        self.colheights[nextMove] += 1
        return True
        
    def playerHasWon(self, player):
        # Check row wins.
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS - WIN_LENGTH + 1):
                seriesLength = 0
                for k in range(WIN_LENGTH):
                    if self.board[i, j+k] == player:
                        seriesLength += 1
                    else:
                        break
                if seriesLength == WIN_LENGTH:
                    return True

        # Check column wins.
        for i in range(NUM_COLS):
            for j in range(NUM_ROWS - WIN_LENGTH + 1):
                seriesLength = 0
                for k in range(WIN_LENGTH):
                    if self.board[j+k, i] == player:
                        seriesLength += 1
                    else:
                        break
                if seriesLength == WIN_LENGTH:
                    return True

        # Check bottom left to top right diagonal wins.
        for i in range(NUM_ROWS - WIN_LENGTH + 1):
            for j in range(NUM_COLS - WIN_LENGTH + 1):
                seriesLength = 0
                for k in range(WIN_LENGTH):
                    if self.board[i+k, j+k] == player:
                        seriesLength += 1
                    else:
                        break
                if seriesLength == WIN_LENGTH:
                    return True

        # Check top left to bottom right diagonal wins.
        for i in range(WIN_LENGTH - 1, NUM_ROWS):
            for j in range(NUM_ROWS - WIN_LENGTH + 1):
                seriesLength = 0
                for k in range(WIN_LENGTH):
                    if self.board[i-k, j+k] == player:
                        seriesLength += 1
                    else:
                        break
                if seriesLength == WIN_LENGTH:
                    return True
        
        return False
            
        
    def isNearSameColor(self, player, col):
        row = self.colheights[col]
        if row > 0:
            if self.board[row-1, col] == player:
                return True
            elif col < NUM_COLS-1 and self.board[row-1, col+1] == player:
                return True
            elif col > 0 and self.board[row-1, col-1] == player:
                return True
                
        if col < NUM_COLS-1 and self.board[row, col+1] == player:
            return True
        elif col < NUM_COLS-1 and self.board[row, col-1] == player:
            return True
        
        return False
        
    def printBoard(self):
        boardString = ''
        for i, row in enumerate(self.board):
            rowString = str(i) + '|'
            for val in row:
                if val == RED:
                    rowString += 'X'
                elif val == BLUE:
                    rowString += 'O'
                else:
                    rowString += '.'
            boardString = rowString + '|\n' + boardString
        print(boardString)
                    
    def play(self):
        self.reset()
        currentPlayer = 0 # Red will always play first.
        
        while(True):
            currentPlayer = BLUE if currentPlayer == RED else RED
            if self.algoMove(currentPlayer):
                self.history.append(numpy.copy(self.board))
                #print("Current player: " + str(currentPlayer))
                #self.printBoard()
                if self.playerHasWon(currentPlayer):
                    #print("Player " + str(currentPlayer) + " wins!")
                    self.winner = currentPlayer
                    break
            else:
                #print("Tie!")
                break
           
    def playTwoModels(self, modelRed, modelBlue):
        self.reset()
        currentPlayer = 0 # Red will always play first.
        
        while(True):
            currentPlayer = BLUE if currentPlayer == RED else RED
            moved = False
            if currentPlayer == RED:
                moved = self.modelMove(currentPlayer, modelRed)
            else:
                moved = self.modelMove(currentPlayer, modelBlue)
                
            if moved:
                self.history.append(numpy.copy(self.board))
                #self.printBoard()
                if self.playerHasWon(currentPlayer):
                    #print("Player " + str(currentPlayer) + " wins!")
                    self.winner = currentPlayer
                    break
            else:
                #print("Tie!")
                break
        return (self.winner, self.history)
        

    def playModel(self, model, modelPlayer, verbose):
        self.reset()
        self.verbose = verbose
        # 100 games with model as red, 100 with model as blue.
        currentPlayer = 0
        while(True):
            if verbose:
                self.printBoard()
            currentPlayer = BLUE if currentPlayer == RED else RED
            if currentPlayer == modelPlayer:
                #print 'model turn'
                if self.modelMove(currentPlayer, model):
                    self.history.append(numpy.copy(self.board))
                    if self.playerHasWon(currentPlayer):
                        self.winner = currentPlayer
                        break
                else:
                    break
            else:   
                #print 'algo turn'
                if self.algoMove(currentPlayer):
                    self.history.append(numpy.copy(self.board))
                    if self.playerHasWon(currentPlayer):
                        self.winner = currentPlayer
                        break
                else:
                    #print("Tie!")
                    break
                    
        #print self.history
        return (self.winner, self.history)
                        
                        
    def evalModel(self, model):
        self.reset()
        # 1000 games with model as red, 1000 with model as blue.
        numGames = 1000
        modelRedGames = [self.playModel(model, RED, False) for _ in range(numGames)]
        modelBlueGames = [self.playModel(model, BLUE, False) for _ in range(numGames)]
        
        mrResults = [x[0] for x in modelRedGames]
        mbResults = [x[0] for x in modelBlueGames]
        
        print 'Red W/L/T: ' + str(mrResults.count(RED)) + '/' + str(mrResults.count(BLUE)) + '/' + str(mrResults.count(0))
        print 'Blue W/L/T: ' + str(mbResults.count(BLUE)) + '/' + str(mbResults.count(RED)) + '/' + str(mbResults.count(0))


    # Experimental. Only produces interesting results if model games aren't deterministic.
    def evalTwoModels(self, model1, model2):
        self.reset()
        # 1000 games with model1 as red, 1000 with model1 as blue.
        numGames = 100
        model1RedGames = [self.playTwoModels(model1, model2) for _ in range(numGames)]
        model1BlueGames = [self.playTwoModels(model2, model1) for _ in range(numGames)]
        
        m1rResults = [x[0] for x in model1RedGames]
        m1bResults = [x[0] for x in model1BlueGames]
        
        print 'Model 1 Red W/L/T: ' + str(m1rResults.count(RED)) + '/' + str(m1rResults.count(BLUE)) + '/' + str(m1rResults.count(0))
        print 'Model 2 Red W/L/T: ' + str(m1bResults.count(BLUE)) + '/' + str(m1bResults.count(RED)) + '/' + str(m1bResults.count(0))  
            
            
                    