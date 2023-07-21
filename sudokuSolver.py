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
        self.geometry("493x518")
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

        self.entropy_button = Button(self.frame_top, text="Get Entropy", command=self.print_entropy)
        self.entropy_button.pack(side=LEFT, anchor=W, fill=X)

        self.possibility_button = Button(self.frame_top, text="Get Possibilities", command=self.print_possibilities)
        self.possibility_button.pack(side=LEFT, anchor=W, fill=X)

        # Create style used by default for all Frames
        self.s = Style(self)
        self.s.configure('FrameBoard.TFrame', background='lightblue')
        self.s.configure('Correct.TFrame', background='lightgreen')
        self.s.configure('Incorrect.TFrame', background='yellow')
        self.s.configure('IncorrectSmall.TFrame', background='red')
        self.s.configure('GridFrame.TFrame', background='grey', highlightcolor='lightblue', highlightthickness=1)
        # Frame Board #
        self.frame_board = Frame(self, style="FrameBoard.TFrame")
        self.frame_board.pack(side=TOP, anchor="center", fill=BOTH, expand=True)

        self.blocks = []
        for r in range(3):
            row = []
            for c in range(3):
                frame = Frame(self.frame_board, style='GridFrame.TFrame', borderwidth=2)
                frame.grid(row=r, column=c, sticky='nsew', padx=2, pady=2)
                row.append(frame)
            self.blocks.append(row)

        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                # Add cell to the block
                # Add a frame so that the cell can form a square
                frm_cell = Frame(self.blocks[i // 3][j // 3], borderwidth=1, style='GridFrame.TFrame')
                frm_cell.grid(row=(i % 3), column=(j % 3), sticky='nsew')
                frm_cell.rowconfigure(0, minsize=50, weight=1)
                frm_cell.columnconfigure(0, minsize=50, weight=1)
                entry = Entry(frm_cell, width=2, font=('Arial', 18), justify='center')
                entry.grid(sticky='nsew')
                row.append(entry)
            self.entries.append(row)

        self.possible_choices_list = [{x for x in range(1, 10)} for x in range(81)]
        self.update_possible_choices()

    def on_close(self):
        self.destroy()

    def update_possible_choices(self):
        for i in range(81):
            value = self.get_int_entry(i)
            if value != 0:
                self.possible_choices_list[i].intersection_update({value})

    def set_board(self, board):
        self.frame_board.configure(style="FrameBoard.TFrame")
        for row in self.blocks:
            for frame in row:
                frame.configure(style="GridFrame.TFrame")
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.configure(state='normal')
                entry.delete(0, END)
                value = ""
                if board[i][j]:
                    value = str(board[i][j])
                entry.insert(END, value)
                if value != "":
                    entry.configure(state='readonly')
        self.possible_choices_list = [{x for x in range(1, 10)} for x in range(81)]
        self.update_possible_choices()

    def get_int_entry(self, idx, idy=None):
        if idy is not None:
            return int(self.entries[idx][idy].get()) if self.entries[idx][idy].get() != "" else 0
        else:
            return int(self.entries[idx // 9][idx % 9].get()) if self.entries[idx // 9][idx % 9].get() != "" else 0

    def solve(self):
        self.update_possible_choices()
        changes = 1
        while changes != 0:
            while changes != 0:
                if self.calculate_entropy() == 0:
                    break
                while changes != 0:
                    changes = self.solve_remove_rows_and_columns_and_squares()
                    print(f"{changes=}")

                changes = self.check_individual_numbers(self.possible_choices_list)
                print(f"{changes=}")

            changes = self.check_for_single_possibility_rows()
            print(f"{changes=}")

        if not self.verify():
            print("Need more logic!")

    def calculate_entropy(self):
        def num_to_range(num, inMin, inMax, outMin, outMax):
            return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))

        original = sum([(len(x) if len(x) != 1 else 0) for x in self.possible_choices_list])
        return num_to_range(original, 0, 576, 0, 100)

    def print_entropy(self):
        self.update_possible_choices()
        print(f"Entropy: {self.calculate_entropy()}")

    def print_possibilities(self):
        self.update_possible_choices()
        print(f"Possible Choices: ")
        for i in range(9):
            my_set = [self.possible_choices_list[x] for x in self.get_row_indexes(i)]
            print(my_set)

    def update_board(self):
        count = 0
        for idx in range(len(self.possible_choices_list)):
            entry = self.entries[int(idx / 9)][idx % 9]
            if len(self.possible_choices_list[idx]) == 1:
                if entry.get() == '':
                    # TODO: Validate Row Column Square before inserting
                    x = list(self.possible_choices_list[idx])
                    entry.insert(END, x[0])
                    count += 1
        return count

    def solve_remove_rows_and_columns_and_squares(self):
        print("\n Removing Duplicates from Rows, Columns, and Squares")
        entropy_score = self.calculate_entropy()
        print(f"Before {entropy_score=}")

        self.remove_line_duplicates(self.possible_choices_list)

        self.remove_column_duplicates(self.possible_choices_list)

        self.remove_square_duplicates(self.possible_choices_list)

        entropy_score = self.calculate_entropy()
        print(f"After Removing {entropy_score=}")

        return self.update_board()

    @staticmethod
    def remove_line_duplicates(possible_choices_list):
        # For each row
        for i in range(9):
            row_index_list = []
            # For each element in the row
            for j in range(9):
                index = (i * 9) + j
                row_index_list.append(possible_choices_list[index])
            # Do the set difference
            non_complete_row = []
            complete_row = []
            for idx in range(len(row_index_list)):
                if len(row_index_list[idx]) != 1:
                    non_complete_row.append(idx)
                else:
                    complete_row.append(idx)
            for idx in range(len(complete_row)):
                for idy in range(len(non_complete_row)):
                    row_index_list[non_complete_row[idy]].difference_update(row_index_list[complete_row[idx]])

        return possible_choices_list

    @staticmethod
    def remove_column_duplicates(possible_choices_list):
        for i in range(9):
            column_index_list = []
            for j in range(9):
                index = (j * 9) + i
                column_index_list.append(possible_choices_list[index])
            # Do the set difference
            non_complete_row = []
            complete_row = []
            for idx in range(len(column_index_list)):
                if len(column_index_list[idx]) != 1:
                    non_complete_row.append(idx)
                else:
                    complete_row.append(idx)
            for idx in range(len(complete_row)):
                for idy in range(len(non_complete_row)):
                    column_index_list[non_complete_row[idy]].difference_update(column_index_list[complete_row[idx]])

        return possible_choices_list

    def remove_square_duplicates(self, possible_choices_list):
        # For each Square
        for i in range(9):
            square_index_list = [possible_choices_list[x] for x in self.get_square_indexes(i)]

            # Do the set difference
            non_complete_row = []
            complete_row = []
            for idx in range(len(square_index_list)):
                if len(square_index_list[idx]) != 1:
                    non_complete_row.append(idx)
                else:
                    complete_row.append(idx)
            for idx in range(len(complete_row)):
                for idy in range(len(non_complete_row)):
                    square_index_list[non_complete_row[idy]].difference_update(square_index_list[complete_row[idx]])

        return possible_choices_list

    def check_for_single_possibility_rows(self):
        print("\n Checking for Single Possibilities in Rows")
        for i in range(9):
            row = [self.possible_choices_list[x] for x in self.get_row_indexes(i)]
            for number in range(1, 10):
                set_list = [[idx, my_set] for idx, my_set in enumerate(row) if (number in my_set and len(my_set) > 1)]
                if len(set_list) == 1:
                    print(f"row={i} {set_list[0][0]=} {set_list[0][1]=} {number=} ")
                    set_list[0][1].intersection_update({number})
        return self.update_board()

    def check_individual_numbers(self, choices_list):
        print("\n Checking for Singular numbers in groups of 3")
        for idx in range(3):
            row1 = self.get_row(0 + (3 * idx))
            row2 = self.get_row(1 + (3 * idx))
            row3 = self.get_row(2 + (3 * idx))

            row1_choices = [choices_list[x] for x in self.get_row_indexes(0 + (3 * idx))]
            row2_choices = [choices_list[x] for x in self.get_row_indexes(1 + (3 * idx))]
            row3_choices = [choices_list[x] for x in self.get_row_indexes(2 + (3 * idx))]

            for number_to_check in range(1, 10):
                if number_to_check in row1 and number_to_check in row2 and number_to_check in row3:
                    # Solved
                    pass
                elif number_to_check in row1 and number_to_check in row2:
                    # Row 3 needs this number
                    index = [index for index, my_set in enumerate(row3_choices) if number_to_check in my_set]
                    if len(index) == 1:
                        row3_choices[index[0]].intersection_update({number_to_check})
                elif number_to_check in row1 and number_to_check in row3:
                    # Row 2 needs this number
                    index = [index for index, my_set in enumerate(row2_choices) if number_to_check in my_set]
                    if len(index) == 1:
                        row2_choices[index[0]].intersection_update({number_to_check})
                elif number_to_check in row2 and number_to_check in row3:
                    # Row 1 needs this number
                    index = [index for index, my_set in enumerate(row1_choices) if number_to_check in my_set]
                    if len(index) == 1:
                        row1_choices[index[0]].intersection_update({number_to_check})

                elif number_to_check in row1:
                    print("Need to find a spot in row 2")
                    print("Need to find a spot in row 3")
                elif number_to_check in row2:
                    print("Need to find a spot in row 1")
                    print("Need to find a spot in row 3")
                elif number_to_check in row3:
                    print("Need to find a spot in row 1")
                    print("Need to find a spot in row 2")
                else:
                    print("Need to find a spot in row 1")
                    print("Need to find a spot in row 2")
                    print("Need to find a spot in row 3")
        return self.update_board()

    def verify(self):
        correct = True
        for i in range(9):
            if not self.verify_row(i) or not self.verify_column(i):
                correct = False
                break
        wrong_square = -1
        for i in range(9):
            if not self.verify_square(i):
                wrong_square = i
                correct = False
                break

        if correct:
            print("All Correct!")
            self.frame_board.configure(style="Correct.TFrame")
            for row in self.blocks:
                for frame in row:
                    frame.configure(style="GridFrame.TFrame")
        else:
            print(f"{wrong_square=}")
            self.frame_board.configure(style="Incorrect.TFrame")
            self.blocks[wrong_square // 3][wrong_square % 3].configure(style="IncorrectSmall.TFrame")

        return correct

    def verify_row(self, index):
        row = self.get_row(index)
        print(f"Row Index: {index} : {len(row) == len(set(row))}")
        return len(row) == len(set(row))

    def verify_column(self, index):
        column = self.get_column(index)
        print(f"Column Index: {index} : {len(column) == len(set(column))}")
        return len(column) == len(set(column))

    def verify_square(self, index):
        square = self.get_square(index)
        print(f"Square Index: {index} : {len(square) == len(set(square))}")
        return len(square) == len(set(square))

    def print_row(self, index: int):
        [print(x, end=' ') for x in self.get_row(index)]

    def print_column(self, index: int):
        [print(x, end=' ') for x in self.get_column(index)]

    def print_square(self, index):
        print(self.get_square(index))

    def get_column(self, index):
        return [int((row[index].get()) if row[index].get() else 0) for row in self.entries]

    def get_row(self, index):
        return [int((x.get()) if x.get() else 0) for x in self.entries[index]]

    def get_row_indexes(self, index):
        return [index * 9 + x for x in range(9)]

    def get_square_indexes(self, index):
        region_indexes = []
        start_row = (index // 3) * 3
        start_col = (index % 3) * 3

        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                region_indexes.append(row * 9 + col)

        return region_indexes

    def get_square(self, index):
        index_list = self.get_square_indexes(index)
        return [self.get_int_entry(idx) for idx in index_list]

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
