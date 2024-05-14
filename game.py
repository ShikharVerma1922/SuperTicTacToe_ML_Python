import random


class Game:
    def __init__(self):
        self.allNodesValues = {}

    def bestMoveForO(self, s, bigBoard, previousMoveCell):
        if not self.action(s, bigBoard, previousMoveCell):
            return 9999
        best_val = self.minimumValue(s, bigBoard, previousMoveCell)
        best_move = []
        print(self.allNodesValues)
        print(best_val)
        for elem in self.allNodesValues:  # for O winning a block
            result = [x[:] for x in s]
            l = elem.split(' ')
            i = int(l[0])
            j = int(l[1])
            result[i][j] = 'O'
            if self.allNodesValues[elem] == best_val and self.terminal(result, bigBoard):
                best_move.extend((i, j))
                return best_move

        for ele in self.allNodesValues:  # for X not winning
            result = [x[:] for x in s]
            l = ele.split(' ')
            i = int(l[0])
            j = int(l[1])
            result[i][j] = 'X'
            if self.allNodesValues[ele] == best_val and self.terminal(result, bigBoard):
                best_move.extend((i, j))
                return best_move

        for ele in self.allNodesValues:  # Doesn't matter
            l = ele.split(' ')
            i = int(l[0])
            j = int(l[1])
            if self.allNodesValues[ele] == best_val:
                best_move.extend((i, j))
                return best_move

    def player(self, s):
        total_X = sum(x.count('X') for x in s)
        total_O = sum(x.count('O') for x in s)
        if total_X > total_O:
            return 'O'
        else:
            return 'X'

    def action(self, s, bigBoard, previousMoveCell):
        a = []
        if bigBoard[previousMoveCell] == 999:
            for i in range(9):
                if s[previousMoveCell][i] == 9999:
                    a.append(str(previousMoveCell)+' '+str(i))
        else:
            for _ in range(9):
                if bigBoard[_] == 999:
                    for j in range(9):
                        if s[_][j] == 9999:
                            a.append(str(_)+' '+str(j))
        return a

    def result(self, s, a, maximizingPlayer):
        r = [x[:] for x in s]
        l = a.split(' ')
        i = int(l[0])
        j = int(l[1])
        if maximizingPlayer:
            r[i][j] = 'X'
        else:
            r[i][j] = 'O'
        return r

    def terminal(self, s, bigBoard):
        for i in range(9):
            if bigBoard[i] == 999:
                if ((s[i][0] == s[i][1] == s[i][2] != 9999) or (s[i][3] == s[i][4] == s[i][5] != 9999) or (s[i][6] == s[i][7] == s[i][8] != 9999) or (s[i][0] == s[i][3] == s[i][6] != 9999) or (s[i][1] == s[i][4] == s[i][7] != 9999) or (s[i][2] == s[i][5] == s[i][8] != 9999) or (s[i][0] == s[i][4] == s[i][8] != 9999) or (s[i][2] == s[i][4] == s[i][6] != 9999)):
                    return True
        return False

    def utility(self, s, bigBoard):
        if self.player(s) == 'O' and self.terminalForBigBoard(bigBoard, 'D'):
            return 1
        elif self.player(s) == 'X' and self.terminalForBigBoard(bigBoard, 'D'):
            return -1
        elif not self.terminalForBigBoard(s, 'D'):
            return 0

    def terminalForBigBoard(self, bigBoard, placeHolder):
        if ((bigBoard[0] == bigBoard[1] == bigBoard[2] != placeHolder) or (bigBoard[3] == bigBoard[4] == bigBoard[5] != placeHolder) or (bigBoard[6] == bigBoard[7] == bigBoard[8] != placeHolder) or (bigBoard[0] == bigBoard[3] == bigBoard[6] != placeHolder) or (bigBoard[1] == bigBoard[4] == bigBoard[7] != placeHolder) or (bigBoard[2] == bigBoard[5] == bigBoard[8] != placeHolder) or (bigBoard[0] == bigBoard[4] == bigBoard[8] != placeHolder) or (bigBoard[2] == bigBoard[4] == bigBoard[6] != placeHolder)):
            return True
        else:
            return False

    def minimumValue(self, s, bigBoard, previousMoveCell):
        v = 99
        for act in self.action(s, bigBoard, previousMoveCell):
            result = self.result(s, act)
            l = act.split(' ')
            currentCellMove = int(l[1])
            val = self.maximumValue(result, bigBoard, currentCellMove)
            self.allNodesValues.update({act: val})
            v = min(v, val)
        return v

    def maximumValue(self, s, bigBoard, previousMoveCell):
        maxVal = -99

        for act in self.action(s, bigBoard, previousMoveCell):
            bigBoardCopy = bigBoard[:]
            result = self.result(s, act)
            if self.terminal(result, bigBoard):
                l = act.split(' ')
                i = int(l[0])
                bigBoardCopy[i] = 'X'
                if self.terminalForBigBoard(bigBoardCopy, 9999):
                    maxVal = max(maxVal, 1)
                else:
                    maxVal = max(maxVal, 0)
        if maxVal == -99:
            return -1
        else:
            return maxVal

    def minimax_advance(self, updated_s, actual_s, updatedBigBoard, actualBigBoard, previousMoveCell_j, depth, maximizingPlayer, alpha, beta, counter):
        if depth == 0 or (self.terminalForBigBoard(updatedBigBoard, 999) and self.terminalForBigBoard(updatedBigBoard, "D")) or not self.action(updated_s, updatedBigBoard, previousMoveCell_j):
            return [self.evaluation(updated_s, actual_s, updatedBigBoard,
                                    actualBigBoard, maximizingPlayer, counter), 9999]

        best_move = random.choice(self.action(
            updated_s, updatedBigBoard, previousMoveCell_j))

        if maximizingPlayer:
            max_val = -99
            for act in self.action(updated_s, updatedBigBoard, previousMoveCell_j):
                l = act.split(' ')
                currentCellMove_i = int(l[0])
                currentCellMove_j = int(l[1])
                result_s = self.result(updated_s, act, maximizingPlayer)
                result_bigB = self.updatedBigBoardFunc(
                    result_s, updatedBigBoard, currentCellMove_i, maximizingPlayer)
                v = self.minimax_advance(
                    result_s, actual_s, result_bigB, actualBigBoard, currentCellMove_j, depth-1, False, alpha, beta, counter)[0]

                if depth >= 3 and ((v == 0) or v == -5):
                    if self.terminal(result_s, updatedBigBoard):
                        v = 5
                if v > max_val:
                    max_val = v
                    best_move = [currentCellMove_i, currentCellMove_j]
                # alpha = max(alpha, v)
                # if beta <= alpha:
                #     break
            return [max_val, best_move]

        else:
            min_val = 99
            for act in self.action(updated_s, updatedBigBoard, previousMoveCell_j):
                l = act.split(' ')
                currentCellMove_i = int(l[0])
                currentCellMove_j = int(l[1])
                result_s = self.result(updated_s, act, maximizingPlayer)
                result_bigB = self.updatedBigBoardFunc(
                    result_s, updatedBigBoard, currentCellMove_i, maximizingPlayer)
                v = self.minimax_advance(
                    result_s, actual_s, result_bigB, actualBigBoard, currentCellMove_j, depth-1, True, alpha, beta, counter)[0]
                if depth >= 3 and ((v == 0) or v == 5):
                    if self.terminal(result_s, updatedBigBoard):
                        v = -5
                if v < min_val:
                    min_val = v
                    best_move = [currentCellMove_i, currentCellMove_j]
                # beta = min(beta, v)
                # if beta <= alpha:
                #     break
            return [min_val, best_move]

    def evaluation(self, updated_s, actual_s, updatedBigBoard, actualBigBoard, maximizingPlayer, counter):
        if self.terminalForBigBoard(updatedBigBoard, 999) and self.terminalForBigBoard(updatedBigBoard, "D"):
            if maximizingPlayer:  # code for O
                return -10
            else:  # code for X
                return 10
        else:
            return 0

    def bestMoveForMinimax_advance(self, csbs, cbbs, pmc_j, depth, maximizingPlayer):
        if not self.action(csbs, cbbs, pmc_j):
            return 9999
        return self.minimax_advance(csbs, csbs,
                                    cbbs, cbbs, pmc_j, depth, maximizingPlayer, -99, 99, 1)

    def updatedBigBoardFunc(self, updated_s, bigBoard, currentMove_i, maximizingPlayer):
        temp = bigBoard[:]
        if self.terminal(updated_s, bigBoard):
            if maximizingPlayer:
                temp[currentMove_i] = "X"
            else:
                temp[currentMove_i] = "O"
        elif not self.action(updated_s, bigBoard, currentMove_i):
            temp[currentMove_i] = "D"
        return temp

        # G1 = Game()
        # dict1 = G1.bestMoveForO(currentSmallBoardState,
        #                         currentBigBoardState, previousMoveCell)
        # print(dict1)
        # for elem in dict1:
        #     print(f"{elem} :: {dict1[elem]}")


def bigBoardStateUpdater(currentMove, mark):
    if G1.terminal(currentSmallBoardState, currentBigBoardState):
        currentBigBoardState[currentMove] = mark
    elif not G1.action(currentSmallBoardState, currentBigBoardState, currentMove):
        currentBigBoardState[currentMove] = 'D'


def printOneLayer(l, small, big):
    for i in range(small, big):
        for j in range(3):
            if l[i][j] == 9999:
                print(" ", end=" ")
            else:
                print(l[i][j], end=" ")
        print(" | ", end=" ")
    print()
    for i in range(small, big):
        for j in range(3, 6):
            if l[i][j] == 9999:
                print(" ", end=" ")
            else:
                print(l[i][j], end=" ")
        print(" | ", end=" ")
    print()
    for i in range(small, big):
        for j in range(6, 9):
            if l[i][j] == 9999:
                print(" ", end=" ")
            else:
                print(l[i][j], end=" ")
        print(" | ", end=" ")


def printCurrentBoard(l):
    printOneLayer(l, 0, 3)
    print()
    print("-------------------------")
    printOneLayer(l, 3, 6)
    print()
    print("-------------------------")
    printOneLayer(l, 6, 9)
    print()


# printCurrentBoard([
    #   ['D' for i in range(9)] for j in range(9)])


################################################
G1 = Game()
initialSmallBoardState = [[9999 for i in range(9)] for j in range(9)]
initialBigBoardState = [999 for i in range(9)]
currentSmallBoardState = [x[:] for x in initialSmallBoardState]
currentBigBoardState = initialBigBoardState[:]


currentMoveForX = [0, 1, 2, 3, 4, 5, 6, 7, 8]
while not G1.terminalForBigBoard(currentBigBoardState, 999):
    G1 = Game()
    print()
    print("position[i j]:", end='')
    x, y = map(int, input().split())
    i = x-1
    j = y-1
    if (i < 0 or i > 8) and (j < 0 or j > 8):
        print("ERROR!! Position not on the board")
    elif i in currentMoveForX and currentSmallBoardState[i][j] == 9999:
        currentSmallBoardState[i][j] = 'X'
        bigBoardStateUpdater(i, 'X')
        bestMove = G1.bestMoveForMinimax_advance(
            currentSmallBoardState, currentBigBoardState, j, 4, False)[1]
        if bestMove:
            currentSmallBoardState[bestMove[0]][bestMove[1]] = 'O'
        else:
            break
        bigBoardStateUpdater(bestMove[0], 'O')
        printCurrentBoard(currentSmallBoardState)
        print()
        print("Computer Played On: ", (bestMove[0] + 1), (bestMove[1] + 1))
        print()
        a = G1.action(currentSmallBoardState,
                      currentBigBoardState, bestMove[1])
        tempList = []
        for ele in a:
            l = ele.split(' ')
            i = int(l[0])
            tempList.append(i)
        currentMoveForX = set(tempList)
        # print(currentBigBoardState)
    elif i in currentMoveForX and currentSmallBoardState[i][j] != 9999:
        print("WARNING!! Position already played")
        continue
    else:
        print("ILLEGAL MOVE!!")

if G1.utility(currentSmallBoardState, currentBigBoardState) == 1:
    print("!! X Won !!")
elif G1.utility(currentSmallBoardState, currentBigBoardState) == -1:
    print("!! O Won !!")
else:
    print("!! Draw !!")
########################################

# g1 = Game()
# initialSmallBoardState = [[9999 for i in range(9)] for j in range(9)]
# initialBigBoardState = [999 for i in range(9)]
# allChildScores = {}
# initialBigBoardState[3] = "O"
# initialBigBoardState[5] = "O"
# initialBigBoardState[8] = "O"

# initialSmallBoardState[1][1] = "X"
# initialSmallBoardState[1][7] = "X"
# initialSmallBoardState[5][1] = "O"
# initialSmallBoardState[1][2] = "O"
# initialSmallBoardState[1][8] = "O"
# initialSmallBoardState[4][8] = "O"
# initialSmallBoardState[4][6] = "O"

# print(initialBigBoardState)
# print(g1.bestMoveForO(initialSmallBoardState, initialBigBoardState, 1))
# print(g1.minimax_advance(initialSmallBoardState, initialSmallBoardState,
#                          initialBigBoardState, initialBigBoardState, 1, 4, True, -99, 99, 1))
# print(allChildScores)
