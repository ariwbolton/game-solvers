import copy, Queue, random

class Board:
	def __init__(self, array=list()):
		if array == []:
			self.generateRandomBoard()
		else:
			self.board = copy.deepcopy(array)

		self.generateAllPossibilities()

	def generateRandomBoard(self):
		# initialize board
		self.board = []

		for i in range(9):
			self.board.append([0,0,0, 0,0,0, 0,0,0])

		row = range(1,10)

		for i in range(3):
			for j in range(3):
				shift = i + (3 * j)

				# rotate row
				if shift == 0:
					newRow = row
				else:
					newRow = row[(len(row) - shift):] + row[:-shift]

				self.setRow((3 * i) + j, newRow)

		self.printBoard()

		# can shuffle columns within each set of 3
		# can shuffle rows within each set of 3

		for i in range(10000):
			self.shuffleRandomRows()
			self.shuffleRandomCols()

	def shuffleRandomRows(self):
		a = [0,1,2]
		random.shuffle(a)

		bucket = int(random.random() * 3)
		a = [i + (bucket * 3) for i in a]

		newFirst = copy.deepcopy(self.getRow((bucket * 3), self.board))
		newSecond = copy.deepcopy(self.getRow((bucket * 3) + 1, self.board))
		newThird = copy.deepcopy(self.getRow((bucket * 3) + 2, self.board))

		self.setRow(a[0], newFirst)
		self.setRow(a[1], newSecond)
		self.setRow(a[2], newThird)

	def shuffleRandomCols(self):
		a = [0,1,2]
		random.shuffle(a)

		bucket = int(random.random() * 3)
		a = [i + (bucket * 3) for i in a]

		newFirst = copy.deepcopy(self.getCol(bucket * 3, self.board))
		newSecond = copy.deepcopy(self.getCol((bucket * 3) + 1, self.board))
		newThird = copy.deepcopy(self.getCol((bucket * 3) + 2, self.board))

		self.setCol(a[0], newFirst)
		self.setCol(a[1], newSecond)
		self.setCol(a[2], newThird)

	def setRow(self, rowNum, row):
		for i in range(9):
			self.board[rowNum][i] = row[i]

	def setCol(self, colNum, col):
		for i in range(9):
			self.board[i][colNum] = col[i]

	def printBoard(self):
		for i in range(len(self.board)):
			if i == 0 or i == 3 or i == 6:
				print " ------- ------- ------- "

			row = self.board[i]

			line = " ".join([str(x) for x in row])

			line = "| " + line[:5] + " | " + line[6:11] + " | " + line[12:] + " |"
			line = line.replace("0", " ")

			print line
		print " ------- ------- ------- "

	def getRow(self, i, board):
		if i < 0 or i > 8:
			return None

		return board[i]

	def getCol(self, i, board):
		if i < 0 or i > 8:
			return None

		return [row[i] for row in board]

	def getBox(self, r, c, board):
		row = (r // 3) * 3
		col = (c // 3) * 3

		a = []

		for i in range(row, row + 3):
			for j in range(col, col + 3):
				a.append(board[i][j])

		return a

	def getCell(sef, row, col):
		return self.board[row][col]

	def possibilites(self, row, col):
		if self.board[row][col] != 0:
			return set([self.board[row][col]])

		rowNums = set(self.getRow(row, self.board))
		colNums = set(self.getCol(col, self.board))

		box = set(self.getBox(row, col, self.board))

		allNums = rowNums | colNums | box

		if 0 in allNums:
			allNums.remove(0)

		s = set([1,2,3,4,5,6,7,8,9])
		s = s - allNums
		return s

	def generateAllPossibilities(self):
		p = []

		for row in range(9):
			p.append([])

			for col in range(9):
				if self.board[row][col] == 0:
					poss = self.possibilites(row, col)

					p[row].append(poss)
				else:
					p[row].append(set([self.board[row][col]]))

		self.allPossibilities = p

	def isOnlyInRow(self, num, row):
		row = self.getRow(row, self.allPossibilities)

		for i in range(8):
			for j in range(i + 1, 9):
				if num in row[i] and num in row[j]:
					return False

		return True

	def isOnlyInCol(self, num, col):
		col = self.getCol(col, self.allPossibilities)

		for i in range(8):
			for j in range(i + 1, 9):
				if num in col[i] and num in col[j]:
					return False

		return True

	def isOnlyInBox(self, num, row, col):
		box = self.getBox(row, col, self.allPossibilities)

		for i in range(8):
			for j in range(i + 1, 9):
				if num in box[i] and num in box[j]:
					return False

		return True

	def rightNum(self, row, col):
		poss = self.allPossibilities[row][col]

		for num in poss:
			isOnlyInRow = self.isOnlyInRow(num, row)
			isOnlyInCol = self.isOnlyInCol(num, col)
			isOnlyInBox = self.isOnlyInBox(num, row, col)

			if isOnlyInBox or isOnlyInCol or isOnlyInRow:
				return num
			else:
				continue

		return 0

	def solveOneSquare(self):
		for row in range(9):
			for col in range(9):
				if self.board[row][col] != 0:
					continue

				n = self.rightNum(row, col)

				if n > 0:
					self.board[row][col] = n
					self.generateAllPossibilities()
					print "Found: (", row, ",", col,") =", n

					return True
				else:
					continue
		# no immediately available squares, must guess
		return False

	def solve(self):
		finished = False

		print "Current Board:"
		self.printBoard()

		if self.isCompleted():
			finished = True

		while not finished:
			found = self.solveOneSquare()

			finished = not found

		if self.isCompleted():
			print "Board is Completed"
			return True

		if self.uncompletable():
			print "Board Uncompletable"
			self.printBoard()
			return False

		# returns true if found
		return self.iterateThroughGuesses()

	def isFilledOut(self):
		# check if any 0's left

		hasZeros = 0 in set([item for sublist in self.board for item in sublist])

		if hasZeros:
			return False

		return True

	def isValid(self):

		for i in range(9):
			row = self.getRow(i, self.board)
			col = self.getCol(i, self.board)

			bRow = i // 3
			bCol = i - (bRow * 3)

			box = self.getBox(bRow * 3, bCol * 3, self.board)

			rowIsValid = len(row) == len(set(row))
			colIsValid = len(col) == len(set(col))
			boxIsValid = len(box) == len(set(box))

			if rowIsValid and colIsValid and boxIsValid:
				continue
			else:
				return False

		return True

	def isCompleted(self):
		return self.isValid() and self.isFilledOut()

	def uncompletable(self):
		l = [item for sublist in self.allPossibilities for item in sublist]

		for item in l:
			if len(item) == 0:
				print item
				return True

		if self.isFilledOut() and not self.isValid():
			return True

		return False

	def iterateThroughGuesses(self):
		minRow, minCol = 0, 0
		minLen = 9

		for row in range(9):
			for col in range(9):
				l = len(self.allPossibilities[row][col])

				if l < minLen and l != 1:
					minLen = len(self.allPossibilities[row][col])
					minRow, minCol = row, col

		poss = self.allPossibilities[minRow][minCol]

		for n in poss:
			print "Guessing:", n, " at ", "(", minRow, ",", minCol, ")"
			print "All guesses for this square:", poss
			newBoard = Board(copy.deepcopy(self.board))

			newBoard.board[minRow][minCol] = n
			newBoard.generateAllPossibilities()

			found = newBoard.solve()

			if found:
				if newBoard.isCompleted():
					newBoard.printBoard()

				return True

		return False

	