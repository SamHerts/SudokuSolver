# https://github.com/ForrestKnight/SudokuSolver just in case
from tkinter import Tk, DISABLED, NORMAL, Menu, TOP, LEFT, RIGHT, BOTH, NW, W, NE, E, X, Canvas
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
        self.geometry("600x400")
        self.minsize(600, 400)

        # Frame Top #
        self.frame_top = Frame(self)
        self.frame_top.pack(side=TOP, anchor=NW, fill=BOTH)

        self.connect_button = Button(self.frame_top, text="Load from File", command=self.load_from_file)
        self.connect_button.pack(side=LEFT, anchor=W, fill=X)

        self.paste_button = Button(self.frame_top, text="Paste from Clipboard", command=self.paste_clipboard)
        self.paste_button.pack(side=LEFT, anchor=W, fill=X)

        # Style option for Abort button
        s = Style(self)
        s.configure("Bold.TButton", font=("Helvetica", 18, "bold"), foreground="red")
        self.abort = Button(self.frame_top, text="SOLVE", command=self.solve, style="Bold.TButton")
        self.abort.pack(side=RIGHT, anchor=NE, fill=BOTH)

        # Frame Board #
        self.frame_board = Frame(self)
        self.frame_board.pack(side=TOP, anchor=NW, fill=BOTH, expand=True)

        # Create a 2D list to hold the Entry widgets
        entries = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = Entry(self.frame_board, width=4, justify="center")
                entry.grid(row=i, column=j)
                row.append(entry)
            entries.append(row)

        # Create a canvas for drawing lines
        canvas = Canvas(self.frame_board, width=400, height=400)
        canvas.grid(row=0, column=0)

        # Draw the grid lines
        for i in range(10):
            if i % 3 == 0:
                line_width = 2  # Thick line for every 3rd line
            else:
                line_width = 1  # Thin line for other lines

            # Vertical lines
            canvas.create_line(40 * i, 0, 40 * i, 400, width=line_width)

            # Horizontal lines
            canvas.create_line(0, 40 * i, 400, 40 * i, width=line_width)

        # Draw the section lines
        for i in range(4):
            line_width = 2
            # Vertical lines
            canvas.create_line(120 * i, 0, 120 * i, 400, width=line_width)
            # Horizontal lines
            canvas.create_line(0, 120 * i, 400, 120 * i, width=line_width)

        # Frame Bottom #

        self.frame_clear = Frame(self)
        self.frame_clear.pack(fill=BOTH)

        self.frame_traffic = Frame(self)
        self.frame_traffic.pack(side=TOP, anchor=NW, fill=BOTH, expand=True)

        Button(self.frame_clear, text="Clear", command=self.solve).pack(
            pady=(5, 5), padx=(5, 5), side=LEFT, anchor=W
        )
        Button(self.frame_clear, text="Clear", command=self.solve).pack(
            pady=(5, 5), padx=(5, 5), side=RIGHT, anchor=E
        )

    def on_close(self):
        self.destroy()

    def solve(self):
        pass

    def load_from_file(self):
        pass

    def paste_clipboard(self):
        pass


if __name__ == "__main__":
    Application = SudokuSolver()
    Application.mainloop()
