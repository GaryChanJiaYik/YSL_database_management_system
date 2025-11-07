import tkinter as tk
from Components import entryWithPlaceHolder as entry  # Ensure this module exists and is correct
from Components.clickablePanel import ClickablePanel as cPanel
from Model.searchModel import searchModel as sm
import Constant.errorCode as errorCode
import Constant.dbColumn as dbCol
from Components.selectableRowTable import Table
from Constant.appConstant import STANDARD_WINDOW_SIZE,WINDOW_CUSTOMER_DETAIL, WINDOW_ADD_CUSTOMER, WINDOW_VIEW_SALE
from tkinter.filedialog import askopenfilename
import shutil
from Constant.databaseManipulationFunctions import (
    searchForUserBasedOn_ID_IC_Name_Contact_oldCustomerId,
    getCustomerListByLatestTreatmentDate
)

import customtkinter as ctk

class LandingWindow(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.root = self
        


        self.table = Table(self.root, self.controller, [], onRowClickCallback=self.openNewWindow)
        # Create a result frame
        self.resultFrame = tk.Frame(self.root)   
        self.resultFrame.grid(column=0, columnspan=3, row=1, rowspan=5)

        # Configure the root grid to allow spacing between left and right sections
        self.root.grid_columnconfigure(1, weight=1)

        # --- Left side: Entry + Add Customer ---
        self.Entryframe = tk.Frame(self.root)
        self.Entryframe.grid(column=0, row=0, sticky="w")  # align left

        # Entry with placeholder
        self.searchCustomerField = entry.EntryWithPlaceholder(
            self.Entryframe, placeholder="Customer ID...", on_text_change=self.print_user_input
        )
        self.searchCustomerField.grid(column=0, row=0)

        # Spacer between entry field and Add Customer button
        tk.Frame(self.Entryframe, width=40).grid(column=1, row=0)

        # Add Customer button
        tk.Button(
            self.Entryframe, text="Add Customer", command=self.addNewCustomer
        ).grid(column=2, row=0, padx=(5, 0))

        # # Hide this button as it is not used at the moment
        # Add Update CSV Button
        # tk.Button(
        #     self.Entryframe, text="Update CSV", command=self.selectAndUpdateCsv
        # ).grid(column=3, row=0)
        # self.Entryframe.grid(column=0, row=0)

        if self.controller.getIsHiddenAccess():
            # --- Right side: View Sale ---
            self.viewSaleFrame = tk.Frame(self.root)
            self.viewSaleFrame.grid(column=2, row=0, sticky="e", padx=(0, 20))  # align to right edge

            tk.Button(
                self.viewSaleFrame, text="View Sale", command=self.viewSale
            ).grid(column=0, row=0)
        
        # Show default customer list
        self.showLatestCustomer()


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
            # self.table.update_table([])  # Properly clear table
            self.showLatestCustomer()
            return

        # Based on user input, search for results
        searchResult = searchForUserBasedOn_ID_IC_Name_Contact_oldCustomerId(text)

        # Clear previous resultFrame labels if needed
        for widget in self.resultFrame.winfo_children():
            widget.destroy()

        if searchResult == errorCode.NO_USER_FOUND:
            self.table.update_table([])  # Clear table
            yourTextPanel = tk.Label(self.resultFrame, text=errorCode.NO_USER_FOUND, fg="red") 
            yourTextPanel.grid(column=1, row=1)
        else:
            searchResult.insert(0, [dbCol.customerId, dbCol.ic, dbCol.name, "Contact No.联系号", "ID"])  # Add headers
            self.table.update_table(searchResult)  


    def showLatestCustomer(self):
        latest_customers = getCustomerListByLatestTreatmentDate(limit=20)
        latest_customers.insert(0, [dbCol.customerId, dbCol.ic, dbCol.name, "Contact No.联系号", "ID"])
        self.table.update_table(latest_customers)


    def openNewWindow(self, customerId):
        self.controller.setCustomerID(customerId) 
        self.controller.switch_frame(WINDOW_CUSTOMER_DETAIL)
        #CustomerDetailsViewRevamp(self.root, customerId)
        
    def addNewCustomer(self):
        self.controller.switch_frame(WINDOW_ADD_CUSTOMER)
        
    def viewSale(self):
        self.controller.switch_frame(WINDOW_VIEW_SALE)
       

