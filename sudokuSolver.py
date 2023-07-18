# https://github.com/ForrestKnight/SudokuSolver just in case
from tkinter import Tk, DISABLED, NORMAL, Menu, TOP, LEFT, RIGHT, BOTH, NONE, NW, W, NE, E, X, Canvas, N, messagebox, \
    END, Toplevel, Text, filedialog
from tkinter.ttk import Style, Label, Button, Entry, Notebook, Combobox, Frame
from os import path


class SudokuSolver(Tk):
    def __init__(self):
        super().__init__()
        # Logo

        # basedir = path.dirname(__file__)

        # self.iconbitmap(path.join(basedir, "SudokuSolver_256x256.ico"))

        # Initialize main application
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title(f"SudokuSolver")
        self.geometry("325x360")
        self.resizable(False, False)

        # Frame Top #
        self.frame_top = Frame(self)
        self.frame_top.pack(side=TOP, anchor=NW, fill=BOTH)

        self.connect_button = Button(self.frame_top, text="Load", command=self.load_from_file)
        self.connect_button.pack(side=LEFT, anchor=W, fill=X)

        self.paste_button = Button(self.frame_top, text="Paste", command=self.paste_clipboard)
        self.paste_button.pack(side=LEFT, anchor=W, fill=X)

        self.solve_button = Button(self.frame_top, text="Solve", command=self.solve)
        self.solve_button.pack(side=LEFT, anchor=W, fill=X)

        self.verify_button = Button(self.frame_top, text="Verify", command=self.verify)
        self.verify_button.pack(side=LEFT, anchor=W, fill=X)

        # Create style used by default for all Frames
        self.s = Style(self)
        self.s.configure('FrameBoard.TFrame', background='lightblue')
        self.s.configure('Correct.TFrame', background='lightgreen')
        self.s.configure('Incorrect.TFrame', background='red')
        # Frame Board #
        self.frame_board = Frame(self, style="FrameBoard.TFrame")
        self.frame_board.pack(side=TOP, anchor="center", fill=BOTH, expand=True)

        # Create a 2D list to hold the Entry widgets
        self.entries = self.create_grid()

    def create_grid(self):
        entry_grid = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = Entry(self.frame_board, width=2, font=('Arial', 18))
                entry.grid(row=i, column=j, padx=2, pady=2, sticky="NEWS")
                row.append(entry)
            entry_grid.append(row)
        return entry_grid

    def on_close(self):
        self.destroy()

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.delete(0, END)
                value = ""
                if board[i][j]:
                    value = str(board[i][j])
                entry.insert(END, value)

    def solve(self):
        possible_choices_list = []
        possible_choices = [x for x in range(1, 10)]
        for i in range(81):
            possible_choices_list.append({x for x in range(1, 10)})

        correct_add = 45
        correct_mul = 362880
        for i in range(9):
            row = self.get_row(1)
            add_result = 0
            mul_result = 1
            for x in row:
                add_result += x
                mul_result *= x
            print(add_result, mul_result)
        for i in range(9):
            for j in range(9):
                print(self.entries[i][j].get())

    def verify(self):
        correct = True
        for i in range(9):
            if not self.verify_row(i) or not self.verify_column(i) or not self.verify_square(i):
                # print(f"Row {i} is not correct")
                correct = False
                break
            # if not self.verify_column(i):
            #     # print(f"Column {i} is not correct")
            #     correct = False
            #     break
            # if not self.verify_square(i):
            #     # print(f"Square {i} is not correct")
            #     correct = False
            #     break

        if correct:
            print("All Correct!")
            self.frame_board.configure(style="Correct.TFrame")
        else:
            self.frame_board.configure(style="Incorrect.TFrame")

        # print("Printing Rows:")
        # for i in range(9):
        #     self.print_row(i)
        #     print()
        #
        # print()
        #
        # print("Printing Columns:")
        # for i in range(9):
        #     self.print_column(i)
        #     print()
        #
        # print("Printing Squares:")
        # for i in range(9):
        #     self.print_square(i)
        #     print()

    def verify_row(self, index):
        row = self.get_row(index)
        return len(row) == len(set(row))

    def verify_column(self, index):
        column = self.get_column(index)
        return len(column) == len(set(column))

    def verify_square(self, index):
        square1, square2, square3 = self.get_square(index)
        square = square1 + square2 + square3
        return len(square) == len(set(square))

    def print_row(self, index: int):
        [print(x, end=' ') for x in self.get_row(index)]

    def print_column(self, index: int):
        [print(x, end=' ') for x in self.get_column(index)]

    def print_square(self, index):
        row1, row2, row3 = self.get_square(index)
        print(row1)
        print(row2)
        print(row3)

    def get_column(self, index):
        return [int((row[index].get()) if row[index].get() else 0) for row in self.entries]

    def get_row(self, index):
        return [int((x.get()) if x.get() else 0) for x in self.entries[index]]

    def get_square(self, index):
        if index in [0, 1, 2]:
            rows = [0, 1, 2]
        elif index in [3, 4, 5]:
            rows = [3, 4, 5]
        elif index in [6, 7, 8]:
            rows = [6, 7, 8]
        else:
            return

        if index in [0, 3, 6]:
            cols = [0, 1, 2]
        elif index in [1, 4, 7]:
            cols = [3, 4, 5]
        elif index in [2, 5, 8]:
            cols = [6, 7, 8]
        else:
            return

        row1 = self.get_row(rows[0])
        row2 = self.get_row(rows[1])
        row3 = self.get_row(rows[2])

        row1 = [row1[cols[0]], row1[cols[1]], row1[cols[2]]]
        row2 = [row2[cols[0]], row2[cols[1]], row2[cols[2]]]
        row3 = [row3[cols[0]], row3[cols[1]], row3[cols[2]]]

        return row1, row2, row3

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Sudoku Files", "*.sudoku")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    board = [[int(char) for char in line.strip()] for line in lines]
                    self.set_board(board)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the file:\n{str(e)}")

    def paste_clipboard(self):
        def validate_input():
            board = []
            input_lines = input_text.get('1.0', END).strip().split('\n')
            if len(input_lines) != 9:
                messagebox.showerror("Invalid Input", "Please enter 9 lines of values.")
                return
            for line in input_lines:
                if len(line) != 9 or not line.isdigit():
                    messagebox.showerror("Invalid Input", "Please enter a valid Sudoku board.")
                    return
                board.append(list(map(int, line)))
            self.set_board(board)
            popup.destroy()

        popup = Toplevel()
        popup.title("Paste Sudoku Board")

        input_label = Label(popup, text="Enter the Sudoku board (use digits 1-9):")
        input_label.pack()

        input_text = Text(popup, height=9, width=9, font=('Arial', 12))
        input_text.pack()

        validate_button = Button(popup, text="Validate", command=validate_input)
        validate_button.pack()


if __name__ == "__main__":
    Application = SudokuSolver()
    Application.mainloop()
