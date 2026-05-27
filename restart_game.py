def restart_game(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        if hasattr(self, '_notified_tiles'):
            del self._notified_tiles
        self.update_ui()