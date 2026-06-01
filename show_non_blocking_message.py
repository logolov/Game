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
