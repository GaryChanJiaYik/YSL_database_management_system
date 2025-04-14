import tkinter as tk

class treatmentDetail:
    
    def createDetailField(self, root, fieldName, content):
         frame = tk.Frame(root)

         tk.Label(frame, text =fieldName, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
         tk.Label(frame, text =content if content != "" else "---", width=20, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=2)
         return frame
    
    def renderCustomerDetails(self, parentContainer, customerModel):
        container = tk.Frame(parentContainer, padx=5, pady=5)
        container.grid(row=0, column=0, sticky="w")
        tk.Label(container, text="Customer Details", font=('Arial', 12), anchor="w").grid(row=0, column=0, sticky="w")
        self.createDetailField(container, "Customer Name", customerModel.customerName).grid(row=1, column=0, sticky="w")
        self.createDetailField(container, "Customer ID", customerModel.customerId).grid(row=2, column=0, sticky="w")    
        

        return container




    def __init__(self,root, customerModel, treatmentID):
        self.treatmentID = treatmentID
        self.root = root



        self.newWindow = tk.Toplevel(self.root)
        self.newWindow.columnconfigure(1, weight=1)
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Treatment Details")

        #Customer details summary
        self.customerDetailsFrame = tk.Frame()
        self.renderCustomerDetails(self.customerDetailsFrame, customerModel)




        #Treatment details

        #Treatment ammendment history