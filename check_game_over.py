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