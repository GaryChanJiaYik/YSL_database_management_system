import tkinter as tk
from Constant.converterFunctions import convertTimeStampToId

class Table:
    def __init__(self, root, data, onRowClickCallback=None):
        self.root = root
        self.data = data
        self.total_rows = len(data)
        self.total_columns = len(data[0]) if data else 0
        self.selected_row = None  # Track selected row
        self.entries = []  # Store label widgets
        self.onRowClickCallback =onRowClickCallback
        self.createTable()

    def createTable(self):
        """Creates the table only if there is data"""
        if not self.data:
            return  # Prevent creating empty table

        for i in range(self.total_rows):
            row_labels = []
            offset = 0
            for j in range(self.total_columns):
                text = ""
                if j == 0:
                    text = convertTimeStampToId(self.data[i][0])
                else:
                    text = self.data[i][j]

                lbl = tk.Label(self.root, text=text, width=18, fg='black', 
                               font=('Arial', 12), borderwidth=2, padx=0, pady=5, 
                               bg="white" if i % 2 == 0 else "lightgray")
                lbl.grid(row=i + 1, column=j + offset, columnspan=2, sticky="nsew")
                lbl.bind("<Button-1>", lambda event, row=i: self.select_row(row))  # Bind click event
                row_labels.append(lbl)
                offset += 2
            self.entries.append([i, row_labels])

    def select_row(self, row):
        """Highlights the selected row."""
        if self.selected_row is not None:
            for cell in self.entries[self.selected_row][1]:
                cell.config(bg="white" if self.entries[self.selected_row][0] % 2 == 0 else "lightgray")
        for cell in self.entries[row][1]:
            cell.config(bg="lightblue")
        self.selected_row = row  

        #Get the id and pass it into the new window
        if self.onRowClickCallback != None:
            self.onRowClickCallback(self.data[row][0])
            #self.onRowClickCallback(self.entries[self.selected_row][1][0]["text"])

    def clearData(self):
        """Removes all labels and clears the list"""
        for row in self.entries:
            for label in row[1]:
                label.destroy()  # Remove each label
        self.entries.clear()
        self.root.update_idletasks()  # Force UI update

    def update_table(self, new_data):
        """Updates the table with new data after clearing it."""
        self.clearData()  # First, clear the old table
        self.data = new_data  
        self.total_rows = len(new_data)
        self.total_columns = len(new_data[0]) if new_data else 0

        if self.total_rows > 0:
            self.createTable()  # Recreate the table only if new data exists
       