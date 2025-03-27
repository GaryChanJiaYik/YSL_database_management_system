import tkinter as tk

class ClickablePanel(tk.Frame):
    def __init__(self, parent, text, command=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Panel styling
        self.config(borderwidth=1, padx=10, pady=5)
        
        self.userName = text

        # Label inside the panel
        self.label = tk.Label(self, text=text, bg="lightgray", font=("Arial", 12))
        self.label.pack(padx=10, pady=5)
        
        # Bind click event
        self.bind("<Button-1>", lambda event: self.on_click(command))
        self.label.bind("<Button-1>", lambda event: self.on_click(command))

    def on_click(self, command):
        if command:
            command(self.userName)