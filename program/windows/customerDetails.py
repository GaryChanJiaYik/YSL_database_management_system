import tkinter as tk
from Constant.databaseManipulationFunctions import searchForSingleUser


class CustomerDetailsPage:
     def __init__(self, root, customerId):
        # !!!!!!!!!!!!!!!!! CustomerId is in timestamp format

        self.customerModel = searchForSingleUser(customerId)

        print(self.customerModel)
        # Toplevel object which will 
        # be treated as a new window
        self.root = root
        self.newWindow = tk.Toplevel(self.root)
    
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("New Window")
    
        # sets the geometry of toplevel
        self.newWindow.geometry("200x200")
    
        # A Label widget to show in toplevel
        tk.Label(self.newWindow, 
            text ="This is a new window").pack()