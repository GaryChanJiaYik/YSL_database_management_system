import tkinter as tk
from Constant.databaseManipulationFunctions import searchForSingleUser
from Constant.appConstant import STANDARD_WINDOW_SIZE
from Constant.dbColumn import customerModelAttributeToField
from Constant.converterFunctions import convertTimeStampToId
from Constant.treatmentDatabaseFunctions import getAllTreatmentByCustomerId
from windows.addTreatment import AddTreatmentView

class CustomerDetailsPage:
     
      def createDetailField(self, root, fieldName, content):
         frame = tk.Frame(root)

         tk.Label(frame, text =fieldName, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
         tk.Label(frame, text =content if content != "" else "---", width=20, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=2)
         return frame

      def renderTreatmentSummaryBlock(self, parentContainer, treatmentModel):
         marginContainer = tk.Frame(parentContainer, pady=2)
         wrapperContainer = tk.Frame(marginContainer, padx=10, pady=5, highlightbackground='black', highlightthickness=1)
         wrapperContainer.grid_columnconfigure(0, weight=1)

         treatmentNameLabel = tk.Label(wrapperContainer, text=treatmentModel.treatmentName, font=('Arial', 12), anchor="w")
         treatmentNameLabel.grid(row=0, column=0, sticky="w")  # Add sticky="w"

         treatmentDescriptionLabel = tk.Label(wrapperContainer, text=treatmentModel.treatmentDescription, font=('Arial', 9), anchor="w")
         treatmentDescriptionLabel.grid(row=1, column=0, sticky="w")  # Add sticky="w"

         treatmentDateLabel = tk.Label(wrapperContainer, text=treatmentModel.treatmentDate, font=('Arial', 9), anchor="w")
         treatmentDateLabel.grid(row=2, column=0, sticky="w")  # Add sticky="w"
         wrapperContainer.grid(row=0, column=0, sticky="w")
         return marginContainer   

      def renderTreatmentSummaryFields(self, parentContainer, customerID):
         treatmentList = getAllTreatmentByCustomerId(customerID)  # A list of treatmentModel objects
         container = tk.Frame(parentContainer,)

         for id, treatment in enumerate(treatmentList):
            block = self.renderTreatmentSummaryBlock(container, treatment)
            block.grid(row=id, column=0, columnspan=2, sticky="w")  # Ensure left alignment

         return container

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
            self.newWindow.columnconfigure(1, weight=1)
            # sets the title of the
            # Toplevel widget
            self.newWindow.title("Customer Details")
         
            # sets the geometry of toplevel
            self.newWindow.geometry(STANDARD_WINDOW_SIZE)

            self.customerDetailFrame = tk.Frame(self.newWindow)
            self.customerDetailFrame.grid(column=0, row=0, sticky="nsew")

                    # A Label widget to show in toplevel
            index = 0
            for idx, (key, value) in enumerate(vars(self.customerModel).items(), start=0):  # or customer.__dict__.items()
                  print(f"Step {index}: Processing attribute '{key}' with value '{value}'")
                  if key == 'customerId':
                     self.createDetailField(self.customerDetailFrame, customerModelAttributeToField[key], convertTimeStampToId(value)).grid(row=idx, column=0)
                  else:
                     self.createDetailField(self.customerDetailFrame, customerModelAttributeToField[key], value).grid(row=idx, column=0)
                  index+=1
            tk.Button(self.customerDetailFrame, text="Add treatment", command=lambda: self.openAddTreatmentWindow(self.customerId)).grid(row=index+2, column=0, sticky='w')





            self.treatmentDetailFrame = tk.Frame(self.newWindow)
            self.treatmentDetailFrame.grid(column=1, row=0, sticky="nsew")
            treatmentSumamryTitle = tk.Label(self.treatmentDetailFrame, text="Treatment Summary", font=('Arial', 16),)
            treatmentSumamryTitle.grid(column=0, row=0, sticky='w')
            treatmentFields = self.renderTreatmentSummaryFields(self.treatmentDetailFrame, convertTimeStampToId(self.customerId))
            treatmentFields.grid(row=1, column=0)





