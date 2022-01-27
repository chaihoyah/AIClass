import random
import copy
import time


class AI:

    def __init__(self, state, timelimit):
        self.state = state
        self.lastlongestC = state.longest
        self.lastlongestplayerC = state.playerlongest
        self.newmoveX = 0
        self.newmoveY = 0
        self.time = 0
        self.timelimit = timelimit

    def findMove(self):
        # player longest check
        # my longest check if corrupted
        # self.lastlongestC = self.state.longest
        # self.lastlongestplayerC = self.state.playerlongest
        new_state = copy.deepcopy(self.state)
        # lastlongest = new_state.longest
        # lastlongest_player = new_state.playerlongest  # 첫돌, 개수, 방향, 막혀있는상태(열려-0, 한쪽-1, 양쪽-2)
        # movetree = new_state.moves  # 서치할때 지나는 노드들 체크

        if len(self.state.longest) == 0:
            if len(self.state.playerlongest) == 0:  # AI먼저]
                return 9, 9
            elif len(self.state.playerlongest) != 0:  # 플레이어 먼저
                return new_state.playerlongest[0][0] + 1, new_state.playerlongest[0][1]

        a = -20000
        b = 20000
        move = list()
        self.time = time.time()
        history = -1000
        for t in range(6):
            now = time.time()
            if now - self.time > self.timelimit:
                break
            try:
                new_move = list()
                v, new_move = self.max_value(new_state, a, b, 0, t+1)
                if v > history:
                    move = new_move
            except:
                print("NOVAL")
        #v, move = self.max_value(new_state, a, b, 0, 5)

        if len(move) == 1:
            self.newmoveX = move[0][0]
            self.newmoveY = move[0][1]
        else:
            self.newmoveX = move[0]
            self.newmoveY = move[1]
        return self.newmoveX, self.newmoveY

    def checkMove(self, state):
        playercol = 0
        tree_lastlongest = state.longest
        tree_lastlongestplayer = state.playerlongest
        tree_moves = list()

        movement = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]

        if len(tree_lastlongestplayer) >= 2 and len(tree_lastlongest) >= 2:
            if tree_lastlongest[1] <= tree_lastlongestplayer[1]:
                if self.isValid(tree_lastlongestplayer[0][0]+movement[7-tree_lastlongestplayer[2]][0], tree_lastlongestplayer[0][1]+movement[7-tree_lastlongestplayer[2]][1]):
                    tree_moves.append([tree_lastlongestplayer[0][0]+movement[7-tree_lastlongestplayer[2]][0], tree_lastlongestplayer[0][1]+movement[7-tree_lastlongestplayer[2]][1]])
                if self.isValid(tree_lastlongestplayer[0][0]+movement[tree_lastlongestplayer[2]][0]*(tree_lastlongestplayer[1]-1), tree_lastlongestplayer[0][1]+movement[7-tree_lastlongestplayer[2]][1]*(tree_lastlongestplayer[1]-1)):
                    tree_moves.append([tree_lastlongestplayer[0][0]+movement[tree_lastlongestplayer[2]][0]*(tree_lastlongestplayer[1]-1), tree_lastlongestplayer[0][1]+movement[7-tree_lastlongestplayer[2]][1]*(tree_lastlongestplayer[1]-1)])
            else:
                if self.isValid(tree_lastlongest[0][0]+movement[7-tree_lastlongest[2]][0], tree_lastlongest[0][1]+movement[7-tree_lastlongest[2]][1]):
                    tree_moves.append([tree_lastlongest[0][0]+movement[7-tree_lastlongest[2]][0], tree_lastlongest[0][1]+movement[7-tree_lastlongest[2]][1]])
                if self.isValid(tree_lastlongest[0][0]+movement[tree_lastlongest[2]][0]*(tree_lastlongest[1]-1), tree_lastlongest[0][1]+movement[7-tree_lastlongest[2]][1]*(tree_lastlongest[1]-1)):
                    tree_moves.append([tree_lastlongest[0][0]+movement[tree_lastlongest[2]][0]*(tree_lastlongest[1]-1), tree_lastlongest[0][1]+movement[7-tree_lastlongest[2]][1]*(tree_lastlongest[1]-1)])
        elif len(tree_lastlongestplayer) >= 2:
            if self.isValid(tree_lastlongestplayer[0][0] + movement[7 - tree_lastlongestplayer[2]][0], tree_lastlongestplayer[0][1] + movement[7 - tree_lastlongestplayer[2]][1]):
                tree_moves.append([tree_lastlongestplayer[0][0] + movement[7 - tree_lastlongestplayer[2]][0], tree_lastlongestplayer[0][1] + movement[7 - tree_lastlongestplayer[2]][1]])
            if self.isValid(tree_lastlongestplayer[0][0] + movement[tree_lastlongestplayer[2]][0] * (tree_lastlongestplayer[1] - 1), tree_lastlongestplayer[0][1] + movement[7 - tree_lastlongestplayer[2]][1] * (tree_lastlongestplayer[1] - 1)):
                tree_moves.append([tree_lastlongestplayer[0][0] + movement[tree_lastlongestplayer[2]][0] * (tree_lastlongestplayer[1] - 1),tree_lastlongestplayer[0][1] + movement[7 - tree_lastlongestplayer[2]][1] * (tree_lastlongestplayer[1] - 1)])
        elif len(tree_lastlongest) >= 2:
            if self.isValid(tree_lastlongest[0][0] + movement[7 - tree_lastlongest[2]][0], tree_lastlongest[0][1] + movement[7 - tree_lastlongest[2]][1]):
                tree_moves.append([tree_lastlongest[0][0] + movement[7 - tree_lastlongest[2]][0], tree_lastlongest[0][1] + movement[7 - tree_lastlongest[2]][1]])
            if self.isValid(tree_lastlongest[0][0] + movement[tree_lastlongest[2]][0] * (tree_lastlongest[1] - 1), tree_lastlongest[0][1] + movement[7 - tree_lastlongest[2]][1] * (tree_lastlongest[1] - 1)):
                tree_moves.append([tree_lastlongest[0][0] + movement[tree_lastlongest[2]][0] * (tree_lastlongest[1] - 1), tree_lastlongest[0][1] + movement[7 - tree_lastlongest[2]][1] * (tree_lastlongest[1] - 1)])
        """
        for j in range(8):
            if len(list(set(map(tuple, tree_moves)))) > 2:
                break
            print(state.moves)
            if self.isValid(state.moves[-1][0] + movement[j][0],state.moves[-1][1] + movement[j][1]):
                tree_moves.append([state.moves[-1][0] + movement[j][0], state.moves[-1][1] + movement[j][1]])
                # tree_moves.append([self.state.moves[k][0]+movement[j][0], self.state.moves[k][1]+movement[j][1]])
        """

        for k in range(len(self.state.moves)):
            for j in range(8):
                if len(list(set(map(tuple, tree_moves)))) > 5:
                    break
                if self.isValid(self.state.moves[len(self.state.moves)-1-k][0]+movement[j][0], self.state.moves[len(self.state.moves)-1-k][1]+movement[j][1]):
                    tree_moves.append([self.state.moves[len(self.state.moves)-1-k][0]+movement[j][0], state.moves[len(self.state.moves)-1-k][1]+movement[j][1]])
            if len(list(set(map(tuple, tree_moves)))) > 5:
                break

        new_tree = []

        new_tree = list(set(map(tuple, tree_moves)))
        print("tree: "+str(new_tree))
        return new_tree

    def max_value(self, state, a, b, depth, depthlimit):
        new_state = copy.deepcopy(state)

        if depth == depthlimit:
            return self.eval_func(new_state)

        temp = -20000
        now = time.time()
        if (now - self.time) > self.timelimit:
            return self.eval_func(new_state)

        tree_moves = self.checkMove(new_state)
        check = list()
        for move in tree_moves:
            check = list()
            now = time.time()
            new_state.make_action(move[0], move[1])
            check.append(move)
            cc = self.min_value(new_state, a, b, depth + 1, depthlimit)
            if (now - self.time) > self.timelimit:
                break
            if temp >= cc:
                if len(check) > 0:
                    check.pop()
                check = copy.deepcopy(move)
            temp = max(temp, cc)
            if temp >= b:
                return temp
            a = max(a, temp)
        if a > 2000:
            return a
        if depth == 0:
            return temp, check
        else:
            return temp



    def min_value(self, state, a, b, depth, depthlimit):
        new_state = copy.deepcopy(state)
        if depth == depthlimit:
            return self.eval_func(new_state)

        temp = 20000
        now = time.time()
        if (now - self.time) > self.timelimit:
            return self.eval_func(new_state)
        tree_moves = self.checkMove(new_state)
        for move in tree_moves:
            now = time.time()
            if (now - self.time) > self.timelimit:
                break
            new_state.make_action(move[0], move[1])
            temp = min(temp, self.max_value(new_state, a, b, depth + 1, depthlimit))
            if temp <= a:
                return temp
            b = min(b, temp)

        if b < -2000:
            return b
        return temp

    def eval_func(self, state):
        score = 0
        if len(state.longest) >= 2:
            if state.longest[3] == 0:
                if state.longest[1] >= 5:
                    score += 2000
                    #return score
                elif state.longest[1] == 4:
                    score += 500
                elif state.longest[1] == 3:
                    score += 100
                elif state.longest[1] == 2:
                    score += 10
            elif state.longest[3] == 1:
                if state.longest[1] >= 5:
                    score += 2000
                    #return score
                elif state.longest[1] == 4:
                    score += 250
                elif state.longest[1] == 3:
                    score += 50
                elif state.longest[1] == 2:
                    score += 2

            if len(self.state.longest) >= 2:
                if state.longest[1] - self.state.longest[1] > 0:
                   score *= (state.longest[1] - self.state.longest[1])
        else:
            score += 2

        if len(state.playerlongest) >= 2:
            if state.playerlongest[3] == 0:
                if state.playerlongest[1] >= 5:
                    score -= 2000
                    #return score
                elif state.playerlongest[1] == 4:
                    score -= 1000
                elif state.playerlongest[1] == 3:
                    score -= 200
                elif state.playerlongest[1] == 2:
                    score -= 30
            elif state.playerlongest[3] == 1:
                if state.playerlongest[1] >= 5:
                    score -= 2000
                    #return score
                elif state.playerlongest[1] == 4:
                    score -= 260
                elif state.playerlongest[1] == 3:
                    score -= 60
                elif state.playerlongest[1] == 2:
                    score -= 2
            if len(self.state.playerlongest) >= 2:
                if state.playerlongest[1] - self.state.playerlongest[1] > 0:
                    score /= int(state.playerlongest[1] - self.state.playerlongest[1])
        else:
            score -= 2
        #print("l: "+ str(state.longest))
        #print("pl: "+ str(state.playerlongest))
        print("score: "+ str(score))
        return score

    def isValid(self, newX, newY):
        if newX<0 or newY<0 or newX>18 or newY>18:
            return False
        if self.state.board[newY, newX] == 0:
            return True
        else:
            return False


class State:
    def __init__(self, board, moves, longest, playerlongest, turn):
        self.board = board
        self.moves = moves
        self.longest = longest
        self.playerlongest = playerlongest
        self.turn = turn

    def make_action(self, new_x, new_y):
        movement = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        # case 1
        self.moves.append([new_x, new_y])
        if self.turn == 0:  # AI 백, AI턴
            self.board[new_y, new_x] = 2

            new = self.findLongest(0)
            newt = self.findLongest(1)
            self.popandcopy(self.longest, new)
            self.popandcopy(self.playerlongest, newt)
            self.turn += 1
        # case 2
        elif self.turn == 1:  # AI 백, 플레이어턴
            self.board[new_y, new_x] = 1

            new = self.findLongest(1)
            newt = self.findLongest(0)
            self.popandcopy(self.playerlongest, new)
            self.popandcopy(self.longest, newt)
            self.turn -= 1
        # case 3
        elif self.turn == 2:  # AI 흑, AI턴
            self.board[new_y, new_x] = 1
            new = self.findLongest(1)
            newt = self.findLongest(0)
            self.popandcopy(self.playerlongest, new)
            self.popandcopy(self.longest, newt)
            self.turn += 1
        # case4
        else:  # AI 흑, 플레이어턴
            self.board[new_y, new_x] = 2
            new = self.findLongest(0)
            newt = self.findLongest(1)
            self.popandcopy(self.longest, new)
            self.popandcopy(self.playerlongest, newt)
            self.turn -= 1
        #if self.turn == 0 or self.turn == 3:
        #    self.board[new_y, new_x] = 1
        #else:
        #    self.board[new_y, new_x] = 2

    def findLongest(self, isLong):
        Maxscore = 0
        Maxcnt = 0
        answer = list()
        if isLong == 0:
            if self.turn == 0 or self.turn == 1:  # AI 백 AI 턴 (<= 1)
                for i in range(1, len(self.moves), 2):
                    tempcnt = 1
                    tempscore = 1
                    isBlocked = 0
                    checkdir = [1, 2, 4, 6, 7]
                    for j in checkdir:
                        tempcnt = 1
                        tempscore = 1
                        isBlocked = 0
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], j)
                        if self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, self.moves[i][0],self.moves[i][1]):
                            tempcnt += 1
                            tempscore += 1
                            new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)
                            while self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, new_checkX, new_checkY):
                                tempcnt += 1
                                tempscore += 1
                                checkX = new_checkX
                                checkY = new_checkY
                                new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)

                            if self.check_pos(self.board, new_checkX, new_checkY) != 0:
                                isBlocked += 1
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], 7 - j)
                        if self.check_pos(self.board, checkX, checkY) == 1:
                            isBlocked += 1

                        if isBlocked == 1:
                            None
                        elif isBlocked == 2:
                            tempcnt = 0
                            tempscore = 0
                            i=1

                        if tempscore > Maxscore:
                            Maxscore = tempscore
                            Maxcnt = tempcnt
                            if Maxcnt >= 2:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                answer.append(Maxcnt)
                                answer.append(j)
                                answer.append(isBlocked)
                            else:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                # answer.append(Maxcnt)
                                # answer.append(j)
                                # answer.append(isBlocked)

                return answer

            elif self.turn == 2 or self.turn == 3:  # AI 흑
                for i in range(0, len(self.moves), 2):
                    tempcnt = 1
                    tempscore = 1
                    isBlocked = 0
                    checkdir = [1, 2, 4, 6, 7]
                    for j in checkdir:
                        tempcnt = 1
                        tempscore = 1
                        isBlocked = 0
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], j)
                        if self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, self.moves[i][0],
                                                                                        self.moves[i][1]):
                            tempcnt += 1
                            tempscore += 1
                            new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)
                            while self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, new_checkX,
                                                                                               new_checkY):
                                tempcnt += 1
                                tempscore += 1
                                checkX = new_checkX
                                checkY = new_checkY
                                new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)

                            if self.check_pos(self.board, new_checkX, new_checkY) != 0:
                                isBlocked += 1
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], 7 - j)
                        if self.check_pos(self.board, checkX, checkY) == 2:
                            isBlocked += 1

                        if isBlocked == 1:
                            None
                        elif isBlocked == 2:
                            i=0
                            tempcnt = 0
                            tempscore = 0

                        if tempscore > Maxscore:
                            Maxscore = tempscore
                            Maxcnt = tempcnt
                            if Maxcnt >= 2:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                answer.append(Maxcnt)
                                answer.append(j)
                                answer.append(isBlocked)
                            else:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                # answer.append(Maxcnt)
                                # answer.append(j)
                                # answer.append(isBlocked)

                return answer
        else:
            if self.turn == 3 or self.turn == 2:  # 플레이어 백 플레이어턴
                for i in range(1, len(self.moves), 2):
                    tempcnt = 1
                    tempscore = 1
                    isBlocked = 0
                    checkdir = [1, 2, 4, 6, 7]
                    for j in checkdir:
                        tempcnt = 1
                        tempscore = 1
                        isBlocked = 0
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], j)
                        if self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, self.moves[i][0],
                                                                                        self.moves[i][1]):
                            tempcnt += 1
                            tempscore += 1
                            new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)
                            while self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, new_checkX,
                                                                                               new_checkY):
                                tempcnt += 1
                                tempscore += 1
                                checkX = new_checkX
                                checkY = new_checkY
                                new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)

                            if self.check_pos(self.board, new_checkX, new_checkY) != 0:
                                isBlocked += 1
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], 7 - j)
                        if self.check_pos(self.board, checkX, checkY) == 1:
                            isBlocked += 1

                        if isBlocked == 1:
                            None
                        elif isBlocked == 2:
                            i=1

                        if tempscore > Maxscore:
                            Maxscore = tempscore
                            Maxcnt = tempcnt
                            if Maxcnt >= 2:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                answer.append(Maxcnt)
                                answer.append(j)
                                answer.append(isBlocked)
                            else:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                # answer.append(Maxcnt)
                                # answer.append(j)
                                # answer.append(isBlocked)

                return answer

            elif self.turn == 1 or self.turn == 0:  # 플레이어 흑
                for i in range(0, len(self.moves), 2):
                    tempcnt = 1
                    tempscore = 1
                    isBlocked = 0
                    checkdir = [1, 2, 4, 6, 7]
                    for j in checkdir:
                        tempcnt = 1
                        tempscore = 1
                        isBlocked = 0
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], j)
                        if self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, self.moves[i][0],
                                                                                        self.moves[i][1]):
                            tempcnt += 1
                            tempscore += 1
                            new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)
                            while self.check_pos(self.board, checkX, checkY) == self.check_pos(self.board, new_checkX,
                                                                                               new_checkY):
                                tempcnt += 1
                                tempscore += 1
                                checkX = new_checkX
                                checkY = new_checkY
                                new_checkX, new_checkY = self.moveto_dir(checkX, checkY, j)

                            if self.check_pos(self.board, new_checkX, new_checkY) != 0:
                                isBlocked += 1
                        checkX, checkY = self.moveto_dir(self.moves[i][0], self.moves[i][1], 7 - j)
                        if self.check_pos(self.board, checkX, checkY) == 2:
                            isBlocked += 1

                        if isBlocked == 1:
                            None
                        elif isBlocked == 2:
                            i=0

                        if tempscore > Maxscore:
                            Maxscore = tempscore
                            Maxcnt = tempcnt
                            if Maxcnt >= 2:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                answer.append(Maxcnt)
                                answer.append(j)
                                answer.append(isBlocked)
                            else:
                                for k in range(len(answer)):
                                    answer.pop()
                                answer.append(self.moves[i])
                                # answer.append(Maxcnt)
                                # answer.append(j)
                                # answer.append(isBlocked)

                return answer

    def popandcopy(self, listA, listB):
        for i in range(len(listA)):
            listA.pop()
        for j in range(len(listB)):
            listA.append(listB[j])

    def popandcopylongest(self, list):
        for i in range(len(self.longest)):
            self.longest.pop()
        for j in range(len(list)):
            self.longest.append(list[j])


    def moveto_dir(self, x, y, d):
        movement = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        if x + movement[d][0]  <=0 or  x + movement[d][0]  >= 0 or y+movement[d][1] >=19 or y+movement[d][1] <= 0:
            return -5, -5
        return x + movement[d][0], y + movement[d][1]

    def check_pos(self, board, x, y):
        if x >=19 or x<=0 or y>=19 or y<=0:
            return 5
        if board[y, x] == 1:
            return 1
        elif board[y, x] == 2:
            return 2
        else:
            return 0
