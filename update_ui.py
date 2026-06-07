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