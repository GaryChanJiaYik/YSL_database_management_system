import tkinter as tk
from Components import entryWithPlaceHolder as entry  # Ensure this module exists and is correct
from Components.clickablePanel import ClickablePanel as cPanel
from Model.searchModel import searchModel as sm
import Constant.errorCode as errorCode
import Constant.dbColumn as dbCol
import csv


class LandingWindow:
    def __init__(self):        
        self.root = tk.Tk()
        self.root.title("YSL DB Management")
        self.root.geometry("600x400")

        # Create a result frame
        self.resultFrame = tk.Frame(self.root)   
        self.resultFrame.grid(column=0, columnspan=3, row=1, rowspan=5)

        # Entry with placeholder
        self.searchCustomerField = entry.EntryWithPlaceholder(
            self.root, placeholder="Customer ID...", on_text_change=self.print_user_input
        )
        self.searchCustomerField.grid(column=0, row=0)

        self.root.mainloop()

    def searchForUser(self, userId):
        with open('./data/db.csv', mode='r', encoding='utf-8') as file:
            csvFile = csv.reader(file)
            header = next(csvFile)           
            res = []
            if dbCol.ic in header and dbCol.name in header:
                ic_index, name_index = header.index(dbCol.ic), header.index(dbCol.name)
                for lines in csvFile:
                    if lines[ic_index] == userId:
                        res.append(sm(lines[ic_index], lines[name_index])) 
                return res
            else:
                return errorCode.NO_USER_FOUND

    def print_user_input(self, text):
        """Callback function to handle user input."""
        if text == "":
            for widget in self.resultFrame.winfo_children():
                widget.destroy()
            return

        #Based on the user input text, search 
        searchResult  = self.searchForUser(text)
        if searchResult == errorCode.NO_USER_FOUND:
            yourTextPanel = tk.Label(self.resultFrame, text=errorCode.NO_USER_FOUND, fg="red") 
            yourTextPanel.grid(column=1, row=1)
        else:
            for i, customer in enumerate(searchResult): 
                structuredText = f'${customer.userId} - {customer.customerName}'
                yourTextPanel = cPanel(self.resultFrame, text=structuredText, command=self.onUserResultClick) 
                yourTextPanel.grid(column=1, row=i)

    def onUserResultClick(self, customerName):
        print(f'Clicked on user: ${customerName}')

