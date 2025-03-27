import tkinter as tk

class Table:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.total_rows = len(data)
        self.total_columns = len(data[0])
        self.selected_row = None  # To keep track of the selected row

        # Create table
        self.entries = []
        for i in range(self.total_rows):
            row_labels = []
            for j in range(self.total_columns):
                lbl = tk.Label(root, text=data[i][j], width=10, fg='black', 
                               font=('Arial', 12), borderwidth=1, padx=5, pady=5, bg="white" if i % 2 == 0 else "gray")
                lbl.grid(row=i +1, column=j, sticky="nsew")
                lbl.bind("<Button-1>", lambda event, row=i: self.select_row(row))  # Bind click event
                row_labels.append(lbl)
            self.entries.append([i, row_labels])

    def select_row(self, row):
        """Highlights the selected row."""
        if self.selected_row is not None:
            # Reset previous row color
            for cell in self.entries[self.selected_row][1]:
                cell.config(bg="white" if self.entries[self.selected_row][0] % 2 == 0 else "gray")

        # Set new selected row color
        for cell in self.entries[row][1]:
            cell.config(bg="lightblue")

        self.selected_row = row  # Update selected row