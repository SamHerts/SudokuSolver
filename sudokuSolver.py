# https://github.com/ForrestKnight/SudokuSolver just in case
from tkinter import Tk, DISABLED, NORMAL, Menu, TOP, LEFT, RIGHT, BOTH, NW, W, NE, E, X
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
