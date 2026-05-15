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