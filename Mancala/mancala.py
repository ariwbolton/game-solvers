
import copy

NULL = 0
PLAYER_1 = 1
PLAYER_2 = 2
SHARED = 3

class Bowl:
	def __init__(self, player):
		self.owner = player
		self.num = 0

	def getNext(self, player):
		pass

	def setNext(self, next):
		self.next = next

	def printBowl(self):
		s = ""

		if self.owner == 0:
			s = "NULL"
		elif self.owner == 1:
			s = "PLAYER_1"
		elif self.owner == 2:
			s = "PLAYER_2"
		elif self.owner == 3:
			s = "SHARED"

		print self.num, " : ", s

class SharedBowl(Bowl):
	def __init__(self, next):
		self.owner = SHARED
		self.next = next
		self.num = 4

	def getNext(self, player):
		if self.next.owner == SHARED or self.next.owner == player:
			return self.next
		else:
			return self.next.next

class OwnedBowl(Bowl):
	def __init__(self, owner, next):
		self.owner = owner
		self.num = 0

		if next is int:
			self.next = OwnedBowl(NULL)
		else:
			self.next = next

	def getNext(self, player):
		return self.next

class Board:
	def __init__(self):
		self.turn = PLAYER_1
		self.pm = list()	# Previous Moves
		self.previousPlayers = list()

		self.playerOneFirstBowl = SharedBowl(PLAYER_1)
		currentBowl = self.playerOneFirstBowl

		for i in range(5):
			currentBowl.next = SharedBowl(PLAYER_1)
			currentBowl = currentBowl.next

		currentBowl.next = OwnedBowl(PLAYER_1, NULL)
		currentBowl = currentBowl.next

		self.playerOneOwnedBowl = currentBowl

		for i in range(6):
			currentBowl.next = SharedBowl(PLAYER_2)

			if i == 1:
				self.playerTwoFirstBowl = currentBowl.next

			currentBowl = currentBowl.next

		currentBowl.next = OwnedBowl(PLAYER_2, NULL)
		currentBowl = currentBowl.next

		self.playerTwoOwnedBowl = currentBowl

		currentBowl.next = self.playerOneFirstBowl	# finish cycle

		#self.printBoard()

	def switchPlayers(self):
		self.turn = 3 - self.turn

	def printPlayers(self):
		print "Players:", self.previousPlayers

	def getScore(self):
		return (self.playerOneOwnedBowl.num, self.playerTwoOwnedBowl.num)

	def gameIsOver(self):
		p1, p2 = self.getScore()

		return (p1 + p2 == 48)

	def printScore(self):
		a, b = self.getScore()
		print "P1: %d | P2: %d" % (a, b)

	def printMoves(self):
		print "Moves:  ", self.pm

	def getMoves(self):
		return self.pm

	def moveIsValid(self, move):
		currentBowl = self.playerOneFirstBowl

		if self.turn == PLAYER_2:
			for i in range(7):
				currentBowl = currentBowl.next
		
		for i in range(move):
			currentBowl = currentBowl.next

		if currentBowl.num == 0:
			return False
		else:
			return True

	def movesAreValid(self):
		mValid = False

		for i in range(0, 6):
			if self.moveIsValid(i):
				mValid = True

		return mValid

	def addMove(self, move):
		self.pm.append(move)
		self.previousPlayers.append(self.turn)

	'''
	*	player: Constant. 	Player making move
	*	bowl:	Integer.	Number of bowls from the leftmost owned bowl of player.
	*						Must be between 0 and 5 (inclusive).
	'''
	def move(self, bowl):
		self.addMove(bowl)	# record move

		currentBowl = self.playerOneFirstBowl

		if self.turn == PLAYER_2:
			for i in range(7):
				currentBowl = currentBowl.next
		
		for i in range(bowl):
			currentBowl = currentBowl.next

		#self.printBoard()

		n = currentBowl.num
		currentBowl.num = 0

		while n > 0:
			currentBowl = currentBowl.getNext(self.turn)
			currentBowl.num += 1
			n -= 1

			if n == 0 and currentBowl.owner != SHARED:
				break

			if n == 0 and currentBowl.num > 1:
				#self.printBoard()
				n = currentBowl.num
				currentBowl.num = 0

		if n == 0 and currentBowl.owner != SHARED:
			pass
		else:
			self.switchPlayers()
		#self.printBoard()

	def printBoard(self):
		s = "Player %d's turn\n" % self.turn

		a = list()
		currentBowl = self.playerOneFirstBowl
		a.append(currentBowl.num)
		
		currentBowl = currentBowl.next

		while currentBowl != self.playerOneFirstBowl:
			a.append(currentBowl.num)
			currentBowl = currentBowl.next

		board =  " ---- --- --- --- --- --- --- ---- \n" \
  			+  "|    | %-2d| %-2d| %-2d| %-2d| %-2d| %-2d|    |\n" % (a[12], a[11], a[10], a[9], a[8], a[7]) \
  			+  "| %2d |--- --- --- --- --- ---| %2d |\n" % (a[13], a[6]) \
  			+  "|    | %-2d| %-2d| %-2d| %-2d| %-2d| %-2d|    |\n" % (a[0], a[1], a[2], a[3], a[4], a[5]) \
  			+  " ---- --- --- --- --- --- --- ---- \n" \

		print s + board
		self.printScore()
		self.printMoves()
		self.printPlayers()
		print "-----------------------------------\n"

class Mancala:
	def __init__(self, board=None):
		if board == None:
			self.board = [Board()]
			#self.printBoard()
		else:
			self.board = [copy.deepcopy(board)]


	def printBoard(self):
		self.getBoard().printBoard()

	def copyBoard(self):
		b = copy.deepcopy(self.getBoard())

		# Not sure if necessary...
		#b.pm = copy.deepcopy(self.getBoard().pm)
		#b.previousPlayers = copy.deepcopy(self.getBoard().previousPlayers)

		return b

	def getBoard(self):
		return self.board[len(self.board) - 1]

	def copyAndPushBoard(self):
		b = self.copyBoard()
		self.board.append(b)

	def popBoard(self):
		self.board.pop()

	def move(self, i):
		self.getBoard().move(i)
		self.getBoard().printBoard()

	def applyMoveList(self, moveList):
		for i in moveList:
			self.move(i)

	def optimalMove(self, searchDepth):
		m1, m2 = -100, -100
		move = -1
		bestBoard = Board()

		# Return best move for current player
		player = self.getBoard().turn

		# TODO: Handle case where can't make move on own side
		if not self.getBoard().movesAreValid():
			pass

		for i in range(0, 6):
			if not self.getBoard().moveIsValid(i):
				continue

			self.copyAndPushBoard()
			self.getBoard().move(i)

			if searchDepth == 1:
				board = self.getBoard()
				p1, p2 = board.getScore()
			else:
				p1, p2, board = self.optimalMove(searchDepth - 1)

			if (player == PLAYER_1 and p1 > m1) or (player == PLAYER_2 and p2 > m2):
				m1, m2 = p1, p2
				move = i
				bestBoard = board

			self.popBoard()

		#print "m = %d | move = %d \n" % (m, move)

		return (m1, m2, bestBoard)


'''
Best:
P1: 23 | P2: 0
Moves:   [1, 0, 4, 5, 3, 5, 4, 2]
Players: [1, 1, 1, 1, 1, 1, 1, 1]

P1: 25 | P2: 0
Moves:   [1, 0, 4, 5, 3, 5, 4, 0, 1, 2, 4, 1, 5]
Players: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


[4, 3, 6, 4, 1, 6, 1, 4, 1, 2, 1]
'''
m = Mancala()
m.applyMoveList([1, 0, 4, 5, 3, 5, 4, 0, 1, 2, 4, 1, 5])

if True:
	max1, max2, bestBoard = m.optimalMove(7)
	bestBoard.printBoard()






#maximum, bestMove = m.optimalMove(1)



