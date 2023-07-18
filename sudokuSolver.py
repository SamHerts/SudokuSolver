# https://github.com/ForrestKnight/SudokuSolver just in case
from tkinter import Tk, DISABLED, NORMAL, Menu, TOP, LEFT, RIGHT, BOTH, NONE, NW, W, NE, E, X, Canvas, N, messagebox, \
    END, \
    Toplevel, Text, filedialog
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
        self.geometry("300x400")
        self.minsize(320, 400)
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
        s = Style(self)
        s.configure('FrameBoard.TFrame', background='lightblue')
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
                entry.grid(row=i, column=j, padx=1, pady=1)
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
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                if value.isdigit():
                    print(int(value), end=' ')
                else:
                    print(0, end=' ')
            print()
        print()

    def verify(self):
        pass

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
