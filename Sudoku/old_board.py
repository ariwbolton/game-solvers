"""Board class"""
import copy, random


class Board:
    """Board class"""

    def __init__(self, array=None):
        if not array:
            array = []

        if array == []:
            self.generate_random_board()
        else:
            self.board = copy.deepcopy(array)

        self.generate_all_possibilities()

    def generate_random_board(self):
        """Generate a random board."""
        # initialize board
        self.board = []

        for i in range(9):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

        row = list(range(1, 10))

        for i in range(3):
            for j in range(3):
                shift = i + (3 * j)

                # rotate row
                if shift == 0:
                    new_row = row
                else:
                    new_row = row[(len(row) - shift):] + row[:-shift]

                self.set_row((3 * i) + j, new_row)

        self.print_board()

        # can shuffle columns within each set of 3
        # can shuffle rows within each set of 3

        for i in range(10000):
            self.shuffle_random_rows()
            self.shuffle_random_cols()

    def shuffle_random_rows(self):
        """Shuffle random rows"""
        a = [0, 1, 2]
        random.shuffle(a)

        bucket = int(random.random() * 3)
        a = [i + (bucket * 3) for i in a]

        new_first = copy.deepcopy(self.get_row((bucket * 3), self.board))
        new_second = copy.deepcopy(self.get_row((bucket * 3) + 1, self.board))
        new_third = copy.deepcopy(self.get_row((bucket * 3) + 2, self.board))

        self.set_row(a[0], new_first)
        self.set_row(a[1], new_second)
        self.set_row(a[2], new_third)

    def shuffle_random_cols(self):
        """Shuffle random cols"""
        a = [0, 1, 2]
        random.shuffle(a)

        bucket = int(random.random() * 3)
        a = [i + (bucket * 3) for i in a]

        new_first = copy.deepcopy(self.get_col(bucket * 3, self.board))
        new_second = copy.deepcopy(self.get_col((bucket * 3) + 1, self.board))
        new_third = copy.deepcopy(self.get_col((bucket * 3) + 2, self.board))

        self.set_col(a[0], new_first)
        self.set_col(a[1], new_second)
        self.set_col(a[2], new_third)

    def set_row(self, row_num, row):
        """Get a row."""
        for i in range(9):
            self.board[row_num][i] = row[i]

    def set_col(self, col_num, col):
        """Get a col."""
        for i in range(9):
            self.board[i][col_num] = col[i]

    def print_board(self):
        """Print the board."""
        for i in range(len(self.board)):
            if i == 0 or i == 3 or i == 6:
                print(" ------- ------- ------- ")

            row = self.board[i]

            line = " ".join([str(x) for x in row])

            line = "| " + line[:5] + " | " + line[6:11] + " | " + line[12:] + " |"
            line = line.replace("0", " ")

            print(line)
        print(" ------- ------- ------- ")

    def get_row(self, i, board):
        """Get a row."""
        if i < 0 or i > 8:
            return None

        return board[i]

    def get_col(self, i, board):
        """Get a col."""
        if i < 0 or i > 8:
            return None

        return [row[i] for row in board]

    def get_box(self, r, c, board):
        """Get a box."""
        row = (r // 3) * 3
        col = (c // 3) * 3

        a = []

        for i in range(row, row + 3):
            for j in range(col, col + 3):
                a.append(board[i][j])

        return a

    def get_cell(self, row, col):
        """Get a cell"""
        return self.board[row][col]

    def possibilites(self, row, col):
        """Get possibilities"""
        if self.board[row][col] != 0:
            return {self.board[row][col]}

        row_nums = set(self.get_row(row, self.board))
        col_nums = set(self.get_col(col, self.board))

        box = set(self.get_box(row, col, self.board))

        all_nums = row_nums | col_nums | box

        if 0 in all_nums:
            all_nums.remove(0)

        s = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        s = s - all_nums

        return s

    def generate_all_possibilities(self):
        """Generate all possibilities"""
        p = []

        for row in range(9):
            p.append([])

            for col in range(9):
                if self.board[row][col] == 0:
                    poss = self.possibilites(row, col)

                    p[row].append(poss)
                else:
                    p[row].append({self.board[row][col]})

        self.allPossibilities = p

    def is_only_in_row(self, num, row):
        """Is only in row"""
        row = self.get_row(row, self.allPossibilities)

        for i in range(8):
            for j in range(i + 1, 9):
                if num in row[i] and num in row[j]:
                    return False

        return True

    def is_only_in_col(self, num, col):
        """Is only in col"""
        col = self.get_col(col, self.allPossibilities)

        for i in range(8):
            for j in range(i + 1, 9):
                if num in col[i] and num in col[j]:
                    return False

        return True

    def is_only_in_box(self, num, row, col):
        """Is only in box"""
        box = self.get_box(row, col, self.allPossibilities)

        for i in range(8):
            for j in range(i + 1, 9):
                if num in box[i] and num in box[j]:
                    return False

        return True

    def right_num(self, row, col):
        """Right num"""
        poss = self.allPossibilities[row][col]

        for num in poss:
            is_only_in_row = self.is_only_in_row(num, row)
            is_only_in_col = self.is_only_in_col(num, col)
            is_only_in_box = self.is_only_in_box(num, row, col)

            if is_only_in_box or is_only_in_col or is_only_in_row:
                return num
            else:
                continue

        return 0

    def solve_one_square(self):
        """Solve one square"""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    continue

                n = self.right_num(row, col)

                if n > 0:
                    self.board[row][col] = n
                    self.generate_all_possibilities()
                    print("Found: (", row, ",", col, ") =", n)

                    return True
                else:
                    continue
        # no immediately available squares, must guess
        return False

    def solve(self):
        """Solve!"""
        finished = False

        print("Current Board:")
        self.print_board()

        if self.is_completed():
            finished = True

        while not finished:
            found = self.solve_one_square()

            finished = not found

        if self.isCompleted():
            print("Board is Completed")
            return True

        if self.uncompletable():
            print("Board Uncompletable")
            self.print_board()
            return False

        # returns true if found
        return self.iterateThroughGuesses()

    def is_filled_out(self):
        """Is filled out"""
        # check if any 0's left

        has_zeros = 0 in set([item for sublist in self.board for item in sublist])

        if has_zeros:
            return False

        return True

    def is_valid(self):
        """Is valid"""
        for i in range(9):
            row = self.get_row(i, self.board)
            col = self.get_col(i, self.board)

            b_row = i // 3
            b_col = i - (b_row * 3)

            box = self.get_box(b_row * 3, b_col * 3, self.board)

            row_is_valid = len(row) == len(set(row))
            col_is_valid = len(col) == len(set(col))
            box_is_valid = len(box) == len(set(box))

            if row_is_valid and col_is_valid and box_is_valid:
                continue
            else:
                return False

        return True

    def is_completed(self):
        """Is completed"""
        return self.is_valid() and self.is_filled_out()

    def uncompletable(self):
        """Uncompletable"""
        l = [item for sublist in self.allPossibilities for item in sublist]

        for item in l:
            if len(item) == 0:
                print(item)
                return True

        if self.is_filled_out() and not self.is_valid():
            return True

        return False

    def iterate_through_guesses(self):
        """Iterate through guesses"""
        min_row, min_col = 0, 0
        min_len = 9

        for row in range(9):
            for col in range(9):
                l = len(self.allPossibilities[row][col])

                if l < min_len and l != 1:
                    min_len = len(self.allPossibilities[row][col])
                    min_row, min_col = row, col

        poss = self.allPossibilities[min_row][min_col]

        for n in poss:
            print("Guessing:", n, " at ", "(", min_row, ",", min_col, ")")
            print("All guesses for this square:", poss)
            new_board = Board(copy.deepcopy(self.board))

            new_board.board[min_row][min_col] = n
            new_board.generate_all_possibilities()

            found = new_board.solve()

            if found:
                if new_board.is_completed():
                    new_board.print_board()

                return True

        return False
