import customtkinter as ctk
from Constant.appConstant import STANDARD_WINDOW_SIZE,WINDOW_ADD_TREATMENT,WINDOW_EDIT_TREATMENT
from Components.customFields import createDetailField
from Constant.converterFunctions import formatDateTime
from Constant.treatmentDatabaseFunctions import getAllTreatmentByConditionID
from windows.addTreatmentRevamp import AddTreatmentViewRevamp
from Components.treatmentSummaryBlock import renderTreatmentSummaryBlockFunctionRevamp
from services.customerFilesServices import getConditionPicturePath,renderFilePicker, uploadCustomerFile
from PIL import Image, ImageTk
from Constant.errorCode import SUCCESS

class ConditionDetailsView(ctk.CTkFrame):

    def treatmentChecked(self):
        print("Checked pressed: ", self.treatedCheck.get())

    def OpenAddTreatmentWindow(self):
        self.controller.setCustomerID(self.conditionModel.customerId)
        self.controller.setConditionModel(self.conditionModel)
        self.controller.switch_frame(WINDOW_ADD_TREATMENT)

        #AddTreatmentViewRevamp(self.root, self.conditionModel.conditionId)

    def handleTreatmentBlockEditClick(self, model):
        print("Clicked on something!!")
        print("Clicked summary for:", model.treatmentID)

        self.controller.setTreatmentID(model.treatmentID)
        self.controller.setCustomerID(self.conditionModel.customerId)
        self.controller.setConditionModel(self.conditionModel)
        self.controller.setConditionID(self.conditionModel.conditionId)
        self.controller.switch_frame(WINDOW_EDIT_TREATMENT)

        

    def renderConditionPictureContainerContent(self, root):
        self.uploadConditionPictureBtn = None
        #Check if there is any picture for the condition
        # If yes, render the picture,
        # else, render button to upload a picture
        conditionPicturePath = getConditionPicturePath(self.customerId, self.conditionModel.conditionId)
        if conditionPicturePath is not None:
            self.renderConditionPicture(root, conditionPicturePath)
        else:
            self.uploadConditionPictureBtn = ctk.CTkButton(root, text="Upload Picture", command=self.uploadConditionPicture)
            self.uploadConditionPictureBtn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def renderConditionPicture(self, root, conditionPicturePath):
        #render the picture
        image = Image.open(conditionPicturePath)
        #resize
        image = image.resize((250, 250))  # Resize the image to fit the label
        # Convert for Tkinter
        photo = ImageTk.PhotoImage(image)


        # Display in CTkLabel
        label = ctk.CTkLabel(root, image=photo, text="")    #     # If no picture, render button to upload a picture
        label.grid(row=0, column=0, sticky="nsew")


    def uploadConditionPicture(self):
        filePath = renderFilePicker(pdefaultextension='',pfiletypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("All files", "*.*")  # Optional fallback
        ], ptitle="Select a picture")
        
        if filePath is not None:
            #manipulate the file path to the condition picture path            
            result = uploadCustomerFile(self.customerId,filePath, self.root,  self.conditionModel.conditionId)
            if result == SUCCESS:
                self.uploadConditionPictureBtn.destroy()
                self.renderConditionPicture(self.conditionPictureContainer, filePath)
                
            print(filePath)




    def __init__(self, parent, controller, customerId, conditionModel):
        # !!!!!!!! customerId is formattted
        super().__init__(parent)
        self.controller = controller
        self.customerId = customerId
        self.conditionModel = conditionModel
        self.grid_columnconfigure(0, weight=1)

        #Customer info
        self.customerInfoFrame = ctk.CTkFrame(
            self,
            bg_color='transparent',
            fg_color='transparent'
        )
        self.customerInfoFrame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=5)
        
        createDetailField(root=self.customerInfoFrame, fieldName="Customer ID", content=self.customerId, row=0, column=0)
        createDetailField(root=self.customerInfoFrame, fieldName="Customer Name", content="William", row=1, column=0)

        #Condition details

        # conditionContainer
        #   -conditionDetailsField
        #   -conditionPicture

        self.conditionContainer = ctk.CTkFrame(
            self,
            fg_color='transparent',
            bg_color='transparent'
            )
        self.conditionContainer.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)


        self.conditionDetailsField = ctk.CTkFrame(
            self.conditionContainer,
            fg_color='transparent',
            bg_color='transparent'
        )
        self.conditionDetailsField.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=5)
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


        #conditionPicture
        self.conditionPictureContainer = ctk.CTkFrame(
            self.conditionContainer,
        )
        self.conditionPictureContainer.grid(row=0, column=1, sticky="nsew", padx=(10, 5), pady=5)
        self.renderConditionPictureContainerContent(self.conditionPictureContainer)


        #Treatment list 
        self.treatmentListFrame = ctk.CTkFrame(
            self,
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

        if len(self.treatmentList) <= 0:
            ctk.CTkLabel(self.treatmentListFrame, text="No treatment found", font=('Arial', 12)).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
            return
        else:
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
                
            