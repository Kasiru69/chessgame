class gamestate():
    def __init__(self):
        self.board=[['black_r','black_n','black_b','black_q','black_k','black_b','black_n','black_r'],
                    ['black_p','black_p','black_p','black_p','black_p','black_p','black_p','black_p'],
                    ['--','--','--','--','--','--','--','--'],
                    ['--', '--', '--', '--', '--', '--', '--', '--'],
                    ['--', '--', '--', '--', '--', '--', '--', '--'],
                    ['--', '--', '--', '--', '--', '--', '--', '--'],
                    ['white_p', 'white_p', 'white_p', 'white_p', 'white_p', 'white_p', 'white_p', 'white_p'],
                    ['white_r','white_n','white_b', 'white_q', 'white_k', 'white_b', 'white_n', 'white_r']
                    ]
        self.whiteTomove=True
        self.moveLog=[]
        self.whiteking=(7,4)
        self.blackking=(0,4)
        self.checkmate=False
        self.stalemate=False
    def makeMove(self,move):
        self.board[move.startrow][move.startcol]='--'
        self.board[move.endrow][move.endcol]=move.piecemoved
        self.moveLog.append(move)
        self.whiteTomove= not self.whiteTomove
        if(move.piecemoved=='white_k'):
            self.whiteking=(move.endrow,move.endcol)
        elif(move.piecemoved=='black_k'):
            self.blackking=(move.endrow,move.endcol)
        if(move.ispawn):
            self.board[move.endrow][move.endcol] = move.piecemoved[0]+move.piecemoved[1]+move.piecemoved[2]+move.piecemoved[3]+move.piecemoved[4]+move.piecemoved[5]+'q'
    def undoMove(self):
        if len(self.moveLog) !=0:
            move=self.moveLog.pop()
            self.board[move.startrow][move.startcol] = move.piecemoved
            self.board[move.endrow][move.endcol] = move.piececaptured
            self.whiteTomove = not self.whiteTomove
            if (move.piecemoved == 'white_k'):
                self.whiteking = (move.startrow, move.startcol)
            elif (move.piecemoved == 'black_k'):
                self.blackking = (move.startrow, move.startcol)
    def ValidMoves(self):
        moves=self.getPossibleMoves()
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            #oppmoves=self.getPossibleMoves()
            self.whiteTomove = not self.whiteTomove
            if self.check():
                moves.remove(moves[i])
            self.whiteTomove = not self.whiteTomove
            self.undoMove()
        if len(moves)==0:
            if self.check():
                self.checkmate=True
            else:
                self.stalemate=True
        return moves
    def check(self):
        if self.whiteTomove:
            return self.underattack(self.whiteking[0],self.whiteking[1])
        else:
            return self.underattack(self.blackking[0],self.blackking[1])
    def underattack(self,r,c):
        self.whiteTomove = not self.whiteTomove
        oppmoves = self.getPossibleMoves()
        self.whiteTomove = not self.whiteTomove
        for move in oppmoves:
            if move.endrow == r and move.endcol == c:
                return True
        return False
    def getPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn=='w' and self.whiteTomove) or (turn=='b' and not self.whiteTomove):
                    piece=self.board[r][c][6]
                    if(piece=='p'):
                        self.getPawn(r,c,moves)
                    if(piece=='r'):
                        self.getRook(r,c,moves)
                    if(piece=='n'):
                        self.getKnight(r, c, moves)
                    if (piece == 'b'):
                        self.getBishop(r, c, moves)
                    if(piece=='q'):
                        self.getQueen(r,c,moves)
                    if(piece=='k'):
                        self.getKing(r,c,moves)
        return moves
    def getPawn(self,r,c,moves):
        if(self.whiteTomove):
            if(self.board[r-1][c]=='--'):
                moves.append(Move((r,c),(r-1,c),self.board))
                if(r==6 and self.board[r-2][c]=='--'):
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if(c-1>=0):
                if(self.board[r-1][c-1][0]=='b'):
                    moves.append(Move((r, c), (r - 1, c-1), self.board))
            if (c + 1 <8):
                if (self.board[r - 1][c + 1][0] == 'b'):
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if (self.board[r + 1][c] == '--'):
                moves.append(Move((r, c), (r + 1, c), self.board))
                if (r == 1 and self.board[r + 2][c] == '--'):
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if (c - 1 >= 0):
                if (self.board[r + 1][c - 1][0] == 'w'):
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if (c + 1 < 8):
                if (self.board[r + 1][c + 1][0] == 'w'):
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
    def getRook(self,r,c,moves):
        dir=((1,0),(-1,0),(0,1),(0,-1))
        enemy='w'
        if self.whiteTomove:
            enemy='b'
        for d in dir:
            for i in range(1,8):
                endrow=r+d[0]*i
                endcol=c+d[1]*i
                if endrow>=0 and endrow<8 and endcol>=0 and endcol<8:
                    endpiece=self.board[endrow][endcol]
                    if endpiece=='--':
                        moves.append(Move((r, c), (endrow,endcol), self.board))
                    elif endpiece[0]==enemy:
                        moves.append(Move((r, c), (endrow,endcol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getKnight(self,r,c,moves):
        dir = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        enemy = 'w'
        if self.whiteTomove:
            enemy = 'b'
        for d in dir:
            endrow=r+d[0]
            endcol=c+d[1]
            if endrow >= 0 and endrow < 8 and endcol >= 0 and endcol < 8:
                endpiece=self.board[endrow][endcol]
                if endpiece[0]==enemy or endpiece=='--':
                    moves.append(Move((r, c), (endrow, endcol), self.board))
    def getBishop(self,r,c,moves):
        dir=((1,1),(1,-1),(-1,1),(-1,-1))
        enemy = 'w'
        if self.whiteTomove:
            enemy = 'b'
        for d in dir:
            for i in range(1,8):
                endrow=r+d[0]*i
                endcol=c+d[1]*i
                if endrow >= 0 and endrow < 8 and endcol >= 0 and endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == '--':
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                    elif endpiece[0] == enemy:
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getQueen(self,r,c,moves):
        self.getBishop(r,c,moves)
        self.getRook(r,c,moves)
    def getKing(self,r,c,moves):
        dir=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        ally='b'
        if self.whiteTomove:
            ally='w'
        for d in dir:
            endrow=r+d[0]
            endcol=c+d[1]
            if endrow >= 0 and endrow < 8 and endcol >= 0 and endcol < 8:
                endpiece=self.board[endrow][endcol]
                if(endpiece[0]!=ally):
                    moves.append(Move((r, c), (endrow, endcol), self.board))

class Move():
    def __init__(self,start,end,board):
        self.startrow=start[0]
        self.startcol=start[1]
        self.endrow=end[0]
        self.endcol=end[1]
        self.piecemoved=board[self.startrow][self.startcol]
        self.piececaptured=board[self.endrow][self.endcol]
        self.moveId=self.startrow*1000+self.startcol*100+self.endrow*10+self.endcol
        self.ispawn=False
        if(self.endrow==0 and self.piecemoved=='white_p') or (self.endrow==7 and self.piecemoved=='black_p'):
            self.ispawn=True
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveId==other.moveId
        return False