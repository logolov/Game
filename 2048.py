import tkinter as tk
import random
import copy

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 - WIP")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#faf8ef")
        
        self.high_score = 0
        self.start_game()

    def start_game(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="2048", font=("Helvetica", 24, "bold"), bg="#bbada0", fg="#ffffff")
        title_label.pack(pady=10)

        self.score_label = tk.Label(
            self.root,
            text=f"Счет: {self.score}",
            font=("Helvetica", 14),
            bg="#bbada0",
            fg="#ffffff"
        )
        self.score_label.pack()

        self.grid_frame = tk.Frame(self.root, bg="#bbada0", width=380, height=380)
        self.grid_frame.pack(pady=10)
        self.grid_frame.pack_propagate(False)

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Label(
                    self.grid_frame,
                    text="",
                    font=("Helvetica", 20, "bold"),
                    width=4, height=2,
                    relief="raised",
                    bd=2
                )
                cell.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                row.append(cell)
            self.cells.append(row)

        for i in range(4):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

        button_frame = tk.Frame(self.root, bg="#faf8ef")
        button_frame.pack(pady=10)

        restart_button = tk.Button(
            button_frame,
            text="Рестарт",
            font=("Helvetica", 12),
            bg="#8f7a66",
            fg="#f9f6f2",
            command=self.restart_game
        )
        restart_button.pack(side="left", padx=10)

        self.update_ui()
        self.root.bind("<Key>", self.key_press)

    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    def reverse_rows(self, board):
        return [row[::-1] for row in board]

    def move_left_row(self, row):
        filtered = [x for x in row if x != 0]
        merged = []
        i = 0
        while i < len(filtered):
            if i + 1 < len(filtered) and filtered[i] == filtered[i + 1]:
                new_val = filtered[i] * 2
                merged.append(new_val)
                self.score += new_val
                i += 2
            else:
                merged.append(filtered[i])
                i += 1
        merged += [0] * (4 - len(merged))
        return merged

    def move_left(self, board):
        return [self.move_left_row(row) for row in board]

    def move_right(self, board):
        return self.reverse_rows(self.move_left(self.reverse_rows(board)))

    def move_up(self, board):
        transposed = self.transpose(board)
        moved = self.move_left(transposed)
        return self.transpose(moved)

    def move_down(self, board):
        transposed = self.transpose(board)
        moved = self.move_right(transposed)
        return self.transpose(moved)

    def move(self, direction):
        old_board = copy.deepcopy(self.board)

        if direction == 'left':
            self.board = self.move_left(self.board)
        elif direction == 'right':
            self.board = self.move_right(self.board)
        elif direction == 'up':
            self.board = self.move_up(self.board)
        elif direction == 'down':
            self.board = self.move_down(self.board)

        if self.board != old_board:
            self.add_new_tile()
            self.update_ui()
            self.check_game_over()

    def restart_game(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

    def update_ui(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                if value == 0:
                    self.cells[i][j].config(text="", bg="#cdc1b4")
                else:
                    bg = self.cell_colors.get(value, "#3c3a32")
                    fg = self.text_colors.get(value, "#f9f6f2")
                    self.cells[i][j].config(text=str(value), bg=bg, fg=fg)
        self.score_label.config(text=f"Счет: {self.score}")

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells) 
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def check_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return
                if i < 3 and self.board[i][j] == self.board[i+1][j]:
                    return
                if j < 3 and self.board[i][j] == self.board[i][j+1]:
                    return
        print(">>> GAME OVER <<<")

    cell_colors = {
        0: "#cdc1b4",
        2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
        128: "#edcf72", 256: "#edcc61", 512: "#edc850",
    }
    text_colors = {
        2: "#776e65", 4: "#776e65",
        8: "#f9f6f2", 16: "#f9f6f2", 32: "#f9f6f2",
    }

    def key_press(self, event):
        key = event.keysym.lower()
        if key in ('left', 'a'):
            self.move('left')
        elif key in ('right', 'd'):
            self.move('right')
        elif key in ('up', 'w'):
            self.move('up')
        elif key in ('down', 's'):
            self.move('down')

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()