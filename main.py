import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        self.main_grid = tk.Frame(self.master, bg="azure3", bd=3, width=400, height=400)
        self.main_grid.grid(pady=(100, 0))
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg="azure4", width=100, height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg="azure4", justify=tk.CENTER, font=("Helvetica", 40), width=4, height=2)
                cell_number.grid(row=i, column=j)
                row.append(cell_number)
            self.cells.append(row)
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Helvetica", 24))
        self.score_label.grid(pady=20)

    def start_game(self):
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()
        self.master.bind("<Key>", self.key_press)

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    self.cells[i][j].configure(text="", bg="azure4")
                else:
                    self.cells[i][j].configure(text=str(self.grid[i][j]), bg="orange")

    def key_press(self, event):
        key = event.keysym
        if key == "Up":
            self.move_up()
        elif key == "Down":
            self.move_down()
        elif key == "Left":
            self.move_left()
        elif key == "Right":
            self.move_right()
        self.update_grid()
        self.add_new_tile()
        self.update_grid()
        self.score_label.configure(text=f"Score: {self.score}")

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()

    def move_left(self):
        for i in range(4):
            self.grid[i] = self.merge(self.grid[i])

    def move_right(self):
        for i in range(4):
            self.grid[i] = self.merge(self.grid[i][::-1])[::-1]

    def merge(self, row):
        new_row = [i for i in row if i != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row[i + 1] = 0
        new_row = [i for i in new_row if i != 0]
        return new_row + [0] * (4 - len(new_row))

    def transpose(self):
        self.grid = [list(row) for row in zip(*self.grid)]

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()