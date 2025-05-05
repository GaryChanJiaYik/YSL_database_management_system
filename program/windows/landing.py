import tkinter as tk
from Components import entryWithPlaceHolder as entry  # Ensure this module exists and is correct
from Components.clickablePanel import ClickablePanel as cPanel
from Model.searchModel import searchModel as sm
import Constant.errorCode as errorCode
import Constant.dbColumn as dbCol
import csv
from Components.selectableRowTable import Table
from windows.customerDetails import CustomerDetailsPage
from Constant.appConstant import STANDARD_WINDOW_SIZE
from tkinter.filedialog import askopenfilename
from windows.customerDetailsRevamp import CustomerDetailsViewRevamp
import shutil
from Constant.databaseManipulationFunctions import searchForUserBasedOn_ID_IC_Name_Email

import customtkinter as ctk

class LandingWindow(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.root = self
        


        self.table = Table(self.root, [], onRowClickCallback=self.openNewWindow)
        # Create a result frame
        self.resultFrame = tk.Frame(self.root)   
        self.resultFrame.grid(column=0, columnspan=3, row=1, rowspan=5)

        self.Entryframe = tk.Frame(self.root)  # Create a frame for the entry field
        # Entry with placeholder
        self.searchCustomerField = entry.EntryWithPlaceholder(
            self.Entryframe, placeholder="Customer ID...", on_text_change=self.print_user_input
        )
        self.searchCustomerField.grid(column=0, row=0)
        tk.Frame(self.Entryframe, width=40).grid(column=1, row=0)  

        tk.Button(
            self.Entryframe, text="Update CSV", command=self.selectAndUpdateCsv
        ).grid(column=2, row=0)
        self.Entryframe.grid(column=0, row=0)


    def selectAndUpdateCsv(self):
        """Open a file dialog to select a new CSV file."""
        filePath = askopenfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
        if filePath:
            filename = filePath.split("/")[-1]
            shutil.copyfile(filePath, f'./data/{filename}')  # Copy the selected file to the target location
            print(f"Selected file: {filePath}")



    def print_user_input(self, text):
        """Callback function to handle user input."""
        if text == "":
            self.table.update_table([])  # Properly clear table
            return

        # Based on user input, search for results
        searchResult = searchForUserBasedOn_ID_IC_Name_Email(text)

        if searchResult == errorCode.NO_USER_FOUND:
            searchResult = []
            yourTextPanel = tk.Label(self.resultFrame, text=errorCode.NO_USER_FOUND, fg="red") 
            yourTextPanel.grid(column=1, row=1)
        else:
            searchResult.insert(0, [dbCol.customerId,dbCol.ic, dbCol.name, dbCol.email])  # Add headers
            self.table.update_table(searchResult)  





    def openNewWindow(self, customerId):
        self.controller.switch_frame(CustomerDetailsViewRevamp, customerId=customerId)
        #CustomerDetailsViewRevamp(self.root, customerId)
       

