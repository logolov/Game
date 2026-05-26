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