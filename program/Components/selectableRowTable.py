import tkinter as tk
from Constant.converterFunctions import convertTimeStampToId
from Constant.appConstant import (
    STANDARD_WINDOW_WIDTH, WINDOW_EDIT_CUSTOMER, WINDOW_LANDING, BLUE,
    FONT, IMG_PATH
)
from PIL import Image, ImageTk

class Table:
    def __init__(self, root, controller, data, onRowClickCallback=None):
        self.root = root
        self.controller = controller
        self.data = data
        self.total_rows = len(data)
        self.total_columns = len(data[0]) if data else 0
        self.selected_row = None  # Track selected row
        self.entries = []  # Store label widgets
        self.onRowClickCallback =onRowClickCallback
        
        # Load icon
        try:
            image_path = IMG_PATH["EDIT"]
            edit_image_raw = Image.open(image_path).convert("RGBA").resize((15, 15))
            self.edit_icon = ImageTk.PhotoImage(edit_image_raw)
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            self.edit_icon = None # Handle the case where the image is not found
    
        self.createTable()


    def createTable(self):
        """Creates the table only if there is data"""
        if not self.data:
            return  # Prevent creating empty table
        
        for i in range(self.total_rows):
            row_labels = []
            is_header = i == 0  # First row is header
             
            offset = 0
            for j in range(self.total_columns):
                if j == 0:
                    continue  # Skip customerId, don't render it
    
                text = ""
                if j == 0:
                    text = convertTimeStampToId(self.data[i][0])
                else:
                    text = self.data[i][j]

                if is_header:
                    lbl = tk.Label(self.root, text=text, width=25, fg='black', 
                                font=FONT["LABEL"], borderwidth=2, padx=0, pady=5, 
                                bg="white" if i % 2 == 0 else "lightgray")
                else:
                    lbl = tk.Label(self.root, text=text, width=25, fg='black', 
                                font=FONT["CONTENT"], borderwidth=2, padx=0, pady=5, 
                                bg="white" if i % 2 == 0 else "lightgray")
                lbl.grid(row=i + 1, column=j - 1, sticky="nsew")
                if not is_header:
                    lbl.bind("<Button-1>", lambda event, row=i: self.select_row(row))  # Bind click event
                row_labels.append(lbl)
                offset += 2

            if not is_header:
                # Add delete button in the last column
                edit_btn = tk.Button(
                    self.root,
                    image=self.edit_icon,
                    command=lambda row=i: self.modify_row(row),
                    relief="flat",
                    bg=BLUE, #if i % 2 == 0 else "lightgray",
                    activebackground="lightgray"
                )
                edit_btn.grid(row=i + 1, column=self.total_columns * 2, sticky="nsew", padx=(5, 0), pady=(5, 0))
                row_labels.append(edit_btn)
            
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
            
    def modify_row(self, row):
        if row == 0:
            return  # Skip header row

        customerID = self.data[row][0]
        self.controller.setCustomerID(customerID)
        self.controller.switch_frame(WINDOW_EDIT_CUSTOMER, previousWindow=WINDOW_LANDING)
       