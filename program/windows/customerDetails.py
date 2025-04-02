import tkinter as tk
from Constant.databaseManipulationFunctions import searchForSingleUser
from Constant.appConstant import STANDARD_WINDOW_SIZE
from Constant.dbColumn import customerModelAttributeToField
from Constant.converterFunctions import convertTimeStampToId

from windows.addTreatment import AddTreatmentView

class CustomerDetailsPage:
     
      def createDetailField(self, root, fieldName, content):
         frame = tk.Frame(root)

         tk.Label(frame, text =fieldName, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
         tk.Label(frame, text =content if content != "" else "---", width=20, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=2)
         return frame

     

      def openAddTreatmentWindow(self, customerId):
         AddTreatmentView(self.root, customerId)

      def __init__(self, root, customerId):
            # !!!!!!!!!!!!!!!!! CustomerId is in timestamp format

            self.customerModel = searchForSingleUser(customerId)
            self.customerId = customerId
            # Toplevel object which will 
            # be treated as a new window
            self.root = root
            self.newWindow = tk.Toplevel(self.root)
         
            # sets the title of the
            # Toplevel widget
            self.newWindow.title("Customer Details")
         
            # sets the geometry of toplevel
            self.newWindow.geometry(STANDARD_WINDOW_SIZE)

            self.customerDetailFrame = tk.Frame(self.newWindow, bg='blue')
            self.customerDetailFrame.grid(column=0, row=0)

                     # A Label widget to show in toplevel
            for index, (key, value) in enumerate(vars(self.customerModel).items(), start=0):  # or customer.__dict__.items()
                  print(f"Step {index}: Processing attribute '{key}' with value '{value}'")
                  if key == 'customerId':
                     self.createDetailField(self.customerDetailFrame, customerModelAttributeToField[key], convertTimeStampToId(value)).grid(row=index, column=0)
                  else:
                     self.createDetailField(self.customerDetailFrame, customerModelAttributeToField[key], value).grid(row=index, column=0)





            self.treatmentDetailFrame = tk.Frame(self.newWindow, bg='gray')
            self.treatmentDetailFrame.grid(column=1, row=0)

            tk.Button(self.newWindow, text="Add treatment", command=lambda: self.openAddTreatmentWindow(self.customerId)).grid(row=13, column=0)



