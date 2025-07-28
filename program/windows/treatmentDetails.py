import customtkinter as ctk
from Constant.treatmentDatabaseFunctions import getTreatmentByID,getAllTreatmentRevisionByID
from Components.customFields import createDetailField
from Components.treatmentSummaryBlock import renderTreatmentSummaryBlockFunctionRevamp


class TreatmentDetailView(ctk.CTkFrame):
    
    def createDetailField(self, root, fieldName, content):
         frame = ctk.CTkFrame(root)

         ctk.CTkLabel(frame, text =fieldName, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
         ctk.CTkLabel(frame, text =content if content != "" else "---", width=20, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=2)
         return frame
    
    def renderCustomerDetails(self, parentContainer, customerModel):
        container = ctk.Frame(parentContainer, padx=5, pady=5)
        container.grid(row=0, column=0, sticky="w")
        ctk.Label(container, text="Customer Details", font=('Arial', 12), anchor="w").grid(row=0, column=0, sticky="w")
        self.createDetailField(container, "Customer Name", customerModel.customerName).grid(row=1, column=0, sticky="w")
        self.createDetailField(container, "Customer ID", customerModel.customerId).grid(row=2, column=0, sticky="w")    
        

        return container


    def renderTreatmentDetails(self):
        createDetailField(self.treatmentDetailFrame, "Created Date", self.treatmentModel.treatmentDate, row=2, column=0)    
        createDetailField(self.treatmentDetailFrame, "Description", self.treatmentModel.treatmentDescription, 3,0)
        createDetailField(self.treatmentDetailFrame, "Cost", f"RM {self.treatmentModel.treatmentCost}", 4,0)

        #Levels
        createDetailField(self.treatmentDetailFrame, "Pain", self.treatmentModel.painLevel,5,0)
        createDetailField(self.treatmentDetailFrame, "Tense", self.treatmentModel.tenseLevel,6,0)    
        createDetailField(self.treatmentDetailFrame, "Sore", self.treatmentModel.soreLevel,7,0)
        createDetailField(self.treatmentDetailFrame, "Numb", self.treatmentModel.numbLevel,8,0)    
        

    def __init__(self, parent, controller, treatmentID):
        super().__init__(parent)
        self.controller = controller
        self.root = self

        self.treatmentModel = getTreatmentByID(treatmentID)

        self.masterFrame = ctk.CTkFrame(master=self.root, bg_color="transparent", fg_color='transparent')
        self.masterFrame.grid(column=0, row=0, sticky="nsew")





        #Treatment details
        self.treatmentDetailFrame = ctk.CTkFrame(master=self.masterFrame, bg_color="transparent", fg_color='transparent' )
        self.treatmentDetailFrame.grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(
            self.treatmentDetailFrame,
            text="Treatment Details",
            bg_color='transparent',  # Make the label background transparent
            font=('Arial', 16),
            anchor="w"  # Align text inside label to left
        ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
        self.renderTreatmentDetails()


        #Treatment ammendment history
        self.treatmentRevisionHistoryFrame = ctk.CTkFrame(master=self.masterFrame, bg_color="transparent", fg_color='transparent' )
        self.treatmentRevisionHistoryFrame.grid(column=0, row=1, sticky="nsew")
        ctk.CTkLabel(
            self.treatmentRevisionHistoryFrame,
            text="Revision History",
            bg_color='transparent',  # Make the label background transparent
            font=('Arial', 16),
            anchor="w"  # Align text inside label to left
        ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)





        self.treatmentRevisionList = getAllTreatmentRevisionByID(self.treatmentModel.treatmentID)

        if len(self.treatmentRevisionList) <= 0:
            ctk.CTkLabel(self.treatmentRevisionHistoryFrame, text="No treatment found", font=('Arial', 12)).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
            return
        else:
            self.scrollableTreatmentListContainer = ctk.CTkScrollableFrame(
                self.treatmentRevisionHistoryFrame,
                bg_color='transparent',
                fg_color='transparent',
                width=500,
                height=250
            )
            self.scrollableTreatmentListContainer.grid_columnconfigure(0, weight=1)
            self.scrollableTreatmentListContainer.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
            for idx, treatment in enumerate(self.treatmentRevisionList):
                renderTreatmentSummaryBlockFunctionRevamp(self.scrollableTreatmentListContainer,treatment,hideButtons=True,row_index=idx).grid(row=idx, column=0, sticky="w")
                
            


