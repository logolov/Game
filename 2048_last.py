import tkinter as tk
import random
import copy
import json
import os

RECORD_FILE = "2048_highscore.json"

def load_high_score():
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except (json.JSONDecodeError, KeyError):
            return 0
    return 0

def save_high_score(score):
    with open(RECORD_FILE, "w") as f:
        json.dump({"high_score": score}, f)

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#faf8ef")
        
        self.high_score = load_high_score()
        self.show_start_screen()

    def show_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.root,
            text="2048",
            font=("Helvetica", 32, "bold"),
            bg="#faf8ef",
            fg="#776e65"
        )
        title.pack(pady=30)

        rules = (
            "Соединяйте плитки с одинаковыми числами.\n"
            "При каждом ходе появляется новая плитка.\n"
            "Цель - собрать плитку как можно большего номинала!\n\n"
            "Управление: стрелки ←↑→↓"
        )
        rules_label = tk.Label(
            self.root,
            text=rules,
            font=("Helvetica", 11),
            bg="#faf8ef",
            fg="#776e65",
            justify="center",
            wraplength=350
        )
        rules_label.pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#faf8ef")
        button_frame.pack(pady=30)

        start_btn = tk.Button(
            button_frame,
            text="Начать игру",
            font=("Helvetica", 14, "bold"),
            bg="#8f7a66",
            fg="#f9f6f2",
            activebackground="#9f8a76",
            activeforeground="#fff",
            width=15,
            command=self.start_game
        )
        start_btn.pack(pady=10)

        exit_btn = tk.Button(
            button_frame,
            text="Выйти",
            font=("Helvetica", 12),
            bg="#d44d38",
            fg="#f9f6f2",
            activebackground="#e55e4a",
            activeforeground="#fff",
            width=15,
            command=self.root.quit
        )
        exit_btn.pack(pady=10)

    def start_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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
            text=f"Счет: {self.score}   Лучший счет: {self.high_score}",
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
            text="Новая игра",
            font=("Helvetica", 12, "bold"),
            bg="#8f7a66",
            fg="#f9f6f2",
            activebackground="#9f8a76",
            activeforeground="#fff",
            width=12,
            command=self.restart_game
        )
        restart_button.pack(side="left", padx=10)

        menu_button = tk.Button(
            button_frame,
            text="Главное меню",
            font=("Helvetica", 12, "bold"),
            bg="#aa988c",
            fg="#f9f6f2",
            activebackground="#bca99d",
            activeforeground="#fff",
            width=12,
            command=self.show_start_screen
        )
        menu_button.pack(side="left", padx=10)

        exit_button = tk.Button(
            button_frame,
            text="Выйти",
            font=("Helvetica", 12, "bold"),
            bg="#d44d38",
            fg="#f9f6f2",
            activebackground="#e55e4a",
            activeforeground="#fff",
            width=12,
            command=self.root.quit
        )
        exit_button.pack(side="left", padx=10)

        instr = tk.Label(self.root, text="Используйте стрелки ←↑→↓", font=("Helvetica", 10), bg="#faf8ef")
        instr.pack()

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
                if self.score > self.high_score:
                    self.high_score = self.score
                    save_high_score(self.high_score)
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
        if hasattr(self, '_notified_tiles'):
            del self._notified_tiles
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
        self.score_label.config(text=f"Счет: {self.score}   Лучший счет: {self.high_score}")

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

        self.show_message("Игра окончена", "Больше ходов нет.")
        self.update_high_score()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)
            self.update_ui()

    def show_non_blocking_message(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x100")
        popup.resizable(False, False)
        popup.configure(bg="#faf8ef")
        popup.overrideredirect(True)

        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 150
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - 50
        popup.geometry(f"+{x}+{y}")

        label = tk.Label(popup, text=message, font=("Helvetica", 12, "bold"), bg="#faf8ef", fg="#776e65", justify="center")
        label.pack(expand=True)

        popup.after(2000, popup.destroy)

    def show_message(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x120")
        popup.resizable(False, False)
        popup.configure(bg="#faf8ef")
        tk.Label(popup, text=message, font=("Helvetica", 14), bg="#faf8ef").pack(pady=20)
        tk.Button(popup, text="OK", command=popup.destroy, font=("Helvetica", 12)).pack()

    cell_colors = {
        0: "#cdc1b4",
        2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
        128: "#edcf72", 256: "#edcc61", 512: "#edc850",
        1024: "#edc53f", 2048: "#edc22e",
        4096: "#edc22e", 8192: "#edc22e", 16384:"#f60000" 
    }
    text_colors = {
        2: "#776e65", 4: "#776e65",
        8: "#f9f6f2", 16: "#f9f6f2", 32: "#f9f6f2",
        64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
        512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2",
        4096: "#f9f6f2", 8192: "#f9f6f2", 16384:"#fecaca"
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