from algoplayer import ConnectFourGame
import random


def recordGame():
    labeledHistory = []
    c4 = ConnectFourGame()
    c4.play()
    if c4.winner is not 0:
        for c4Move in c4.history:
            labeledHistory.append((c4Move, c4.winner))
    return labeledHistory
    
def recordTwoModelsGame(modelRed, modelBlue):
    labeledHistory = []
    c4 = ConnectFourGame()
    c4.playTwoModels(modelRed, modelBlue)
    if c4.winner is not 0:
        for c4Move in c4.history:
            labeledHistory.append((c4Move, c4.winner))
    return labeledHistory
    
def recordGamesDupeLimit(count, dupeLimit):
    labels = []
    d = {}
    for i in range(count):
        for c4Hist in recordGame():
            sMove = str(c4Hist[0]) + str(c4Hist[1])
            if sMove in d and d[sMove] < dupeLimit:
                labels.append(c4Hist)
                d[sMove] += 1
            elif sMove not in d:
                labels.append(c4Hist)
                d[sMove] = 1
                
    random.shuffle(labels)
    return labels

def recordModelGamesDupeLimit(count, dupeLimit, model1, model2):
    labels = []
    d = {}
    for i in range(count/2):
        for c4Hist in recordTwoModelsGame(model1, model2):
            sMove = str(c4Hist[0]) + str(c4Hist[1])
            if sMove in d and d[sMove] < dupeLimit:
                labels.append(c4Hist)
                d[sMove] += 1
            elif sMove not in d:
                labels.append(c4Hist)
                d[sMove] = 1
    for i in range(count/2):
        for c4Hist in recordTwoModelsGame(model2, model1):
            sMove = str(c4Hist[0]) + str(c4Hist[1])
            if sMove in d and d[sMove] < dupeLimit:
                labels.append(c4Hist)
                d[sMove] += 1
            elif sMove not in d:
                labels.append(c4Hist)
                d[sMove] = 1 
                     
    random.shuffle(labels)
    return labels

def recordGames(count):
    labels = []
    for i in range(count):
        for c4Hist in recordGame():
            labels.append(c4Hist)
    random.shuffle(labels)
    return labels
    
def findWinProportion(count):
    playerWins = [0, 0, 0] # blue wins, ties, red wins
    gameTurns = 0
    c4 = ConnectFourGame()
    for i in range(count):
        c4.play()
        playerWins[c4.winner + 1] += 1
        gameTurns += len(c4.history)
        
    print playerWins
    print gameTurns
        
