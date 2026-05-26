def add_new_tile(self):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells) 
        self.board[i][j] = 2 if random.random() < 0.9 else 4