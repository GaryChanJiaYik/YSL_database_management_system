import customtkinter as ctk
from Constant.appConstant import STANDARD_WINDOW_SIZE
from Components.customFields import createDetailField
from Constant.converterFunctions import formatDateTime
from Constant.treatmentDatabaseFunctions import getAllTreatmentByConditionID
from windows.addTreatmentRevamp import AddTreatmentViewRevamp
from Components.treatmentSummaryBlock import renderTreatmentSummaryBlockFunctionRevamp

class ConditionDetailsView:

    def treatmentChecked(self):
        print("Checked pressed: ", self.treatedCheck.get())

    def OpenAddTreatmentWindow(self):
        AddTreatmentViewRevamp(self.root, self.conditionModel.conditionId)

    def handleTreatmentBlockEditClick(self, model):
        print("Clicked on something!!")


    def __init__(self, root, customerId, conditionModel):
        # !!!!!!!! customerId is formattted
        self.root = root
        self.newWindow = ctk.CTkToplevel(self.root)
        self.newWindow.columnconfigure(0, weight=1)
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Condition Details")
        self.newWindow.grid_columnconfigure(0, weight=1)
        
        # sets the geometry of toplevel
        self.newWindow.geometry(STANDARD_WINDOW_SIZE)

        self.customerId = customerId
        self.conditionModel = conditionModel
        
        #Customer info
        self.customerInfoFrame = ctk.CTkFrame(
            self.newWindow,
            fg_color='transparent',
            bg_color='transparent'
        )
        self.customerInfoFrame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=5)
        
        createDetailField(root=self.customerInfoFrame, fieldName="Customer ID", content=self.customerId, row=0, column=0)
        createDetailField(root=self.customerInfoFrame, fieldName="Customer Name", content="William", row=1, column=0)

        #Condition details
        self.conditionDetailsField = ctk.CTkFrame(
            self.newWindow,
            fg_color='transparent',
            bg_color='transparent'
        )
        self.conditionDetailsField.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        self.conditionDetailSubFrame = ctk.CTkFrame(
            self.conditionDetailsField,
            fg_color='transparent',
            bg_color='transparent'
        )
        self.conditionDetailSubFrame.grid_columnconfigure(0, weight=2)
        self.conditionDetailSubFrame.grid_columnconfigure(1, weight=1)
        self.conditionDetailSubFrame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=5)

        ctk.CTkLabel(
             self.conditionDetailSubFrame,
             text="Condition Info",
            font=('Arial', 16)
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.treatedCheck = ctk.BooleanVar()
        ctk.CTkCheckBox(
            self.conditionDetailSubFrame,
            text="Mark as treated",
            command=self.treatmentChecked(),
            checkbox_height=16,
            checkbox_width=16,
            border_width=2,
            variable=self.treatedCheck
        ).grid(row=0, column=1, sticky="e", padx=(10, 5), pady=5)
        

        createDetailField(root=self.conditionDetailsField, fieldName="Description", content=conditionModel.conditionDescription, row=1, column=0)
        createDetailField(root=self.conditionDetailsField, fieldName="Added Date", content=conditionModel.conditionDate, row=2, column=0)
        createDetailField(root=self.conditionDetailsField, fieldName="Status", content="Undergoing Treatement" if conditionModel.undergoingTreatment else "Treated", row=3, column=0)


        #Treatment list 
        self.treatmentListFrame = ctk.CTkFrame(
            self.newWindow,
            bg_color='transparent',
            fg_color='transparent'
        )
        self.treatmentListFrame.grid_columnconfigure(0, weight=1)

        self.treatmentListFrame.grid(row=2, column=0, sticky="nsew", padx=(10, 5), pady=5)

        self.treatmentListSubFrame = ctk.CTkFrame(
            self.treatmentListFrame,
            bg_color='transparent',
            fg_color='transparent'
        )
        self.treatmentListSubFrame.grid_columnconfigure(0, weight=1)
        self.treatmentListSubFrame.grid_columnconfigure(1, weight=0)
        self.treatmentListSubFrame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=5)


        ctk.CTkLabel(self.treatmentListSubFrame, text="Treatments",font=('Arial', 16)).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(self.treatmentListSubFrame, text="Add Treatment", command=self.OpenAddTreatmentWindow).grid(row=0, column=1, sticky="e")

        #treatment
        self.treatmentList = getAllTreatmentByConditionID(self.conditionModel.conditionId)
        print("len of treatrments: ", len(self.treatmentList))


        self.scrollableTreatmentListContainer = ctk.CTkScrollableFrame(
            self.treatmentListFrame,
            bg_color='transparent',
            fg_color='transparent',
            width=500,
            height=250
        )
        self.scrollableTreatmentListContainer.grid_columnconfigure(0, weight=1)
        self.scrollableTreatmentListContainer.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        for idx, treatment in enumerate(self.treatmentList):
            renderTreatmentSummaryBlockFunctionRevamp(self.scrollableTreatmentListContainer,treatment,self.handleTreatmentBlockEditClick).grid(row=idx, column=0, sticky="w")
            
        