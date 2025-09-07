import customtkinter as ctk
from tkinter.filedialog import askopenfilenames
from Constant.appConstant import (
    STANDARD_WINDOW_SIZE, WINDOW_ADD_TREATMENT, WINDOW_EDIT_TREATMENT, WINDOW_TREATMENT_DETAIL,
    FONT
    )
from Constant.converterFunctions import formatDateTime
from Constant.treatmentDatabaseFunctions import getAllTreatmentByConditionID
from Constant.errorCode import SUCCESS
from Components.customFields import createDetailField
from Components.popupModal import renderPopUpModal
from Components.treatmentSummaryBlock import renderTreatmentSummaryBlockFunctionRevamp
from Components.floatingInfoPanel import attach_floating_info
from services.conditionDbFunctions import updateTreatmentStatus, getTreatmentStatus
from services.customerFilesServices import getConditionPicturePath,renderFilePicker, uploadCustomerFile
from services.attachmentFilesServices import HasAttachment, uploadAttachmentFile, openAttachmentDirectory
from PIL import Image
from Constant.errorCode import SUCCESS

#Constants
ATTACHMENT_TYPE = "Condition"

class ConditionDetailsView(ctk.CTkFrame):

    def treatmentChecked(self):
        is_treated = self.treatedCheck.get()
        new_status = "Treated" if is_treated else "Undergoing"
        
        self.statusLabel.configure(text=new_status)
        updateTreatmentStatus(self.customerId, self.conditionModel.conditionId, is_treated)
        
    def LoadTreatmentStatus(self):
        is_treated = getTreatmentStatus(self.customerId, self.conditionModel.conditionId)

        self.treatedCheck.set(is_treated)
        self.statusLabel.configure(text="Treated" if is_treated else "Undergoing")

    def OpenAddTreatmentWindow(self):
        self.controller.setCustomerID(self.conditionModel.customerId)
        self.controller.setConditionID(self.conditionModel.conditionId);
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
        conditionPicturePath = getConditionPicturePath(self.customerId, self.conditionModel.conditionId, ATTACHMENT_TYPE)
        if conditionPicturePath is not None:
            self.renderConditionPicture(root, conditionPicturePath)
        else:
            self.uploadConditionPictureBtn = ctk.CTkButton(root, text="Upload Picture", command=self.uploadConditionPicture)
            self.uploadConditionPictureBtn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


    def renderConditionAttachmentContainerContent(self, root):
        for widget in root.winfo_children():
            widget.destroy()

        conditionHasAttachmentVar = HasAttachment(self.customerId, ATTACHMENT_TYPE, self.conditionModel.conditionId)

        upload_btn = ctk.CTkButton(
            master=root,
            text="Upload",
            command=self.uploadConditionAttachment
        )
        upload_btn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        if conditionHasAttachmentVar:
            view_btn = ctk.CTkButton(
                master=root,
                text="View",
                command=self.viewConditionAttachmentDirectory
            )
            view_btn.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        
    def renderConditionPicture(self, root, conditionPicturePath):
        #render the picture
        image = Image.open(conditionPicturePath)
        #resize
        image = image.resize((250, 250))  # Resize the image to fit the label
        # Convert for Tkinter
        # photo = ImageTk.PhotoImage(image)
        photo = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))

        # Display in CTkLabel
        label = ctk.CTkLabel(root, image=photo, text="")    #     # If no picture, render button to upload a picture
        label.image = photo
        label.grid(row=0, column=0, sticky="nsew")


    def uploadConditionPicture(self):
        filePath = renderFilePicker(
            pdefaultextension='',
            pfiletypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ],
            ptitle="Select a picture"
        )

        if not filePath:
            return  # User clicked cancel, do nothing

        # Upload the file to the correct condition picture path
        result = uploadCustomerFile(self.customerId, filePath, self.parent, self.conditionModel.conditionId, ATTACHMENT_TYPE)

        if result == SUCCESS:
            if hasattr(self, 'uploadConditionPictureBtn') and self.uploadConditionPictureBtn:
                self.uploadConditionPictureBtn.destroy()
            self.renderConditionPicture(self.conditionPictureContainer, filePath)


    def uploadConditionAttachment(self):
        file_paths = askopenfilenames(
            title="Select files to upload",
            filetypes=[
                ("All Files", "*.*"),
                ("ZIP Files", "*.zip"),
                ("PDF Files", "*.pdf"),
                ("Images", "*.jpg *.jpeg *.png"),
            ]
        )

        all_success = True
        if file_paths:
            for filePath in file_paths:
                result = uploadAttachmentFile(self.customerId, filePath, self.parent, ATTACHMENT_TYPE, self.conditionModel.conditionId)
                if result != SUCCESS:
                    all_success = False
        else:
            return
        
        if all_success:
            renderPopUpModal(self.parent, "All files uploaded successfully", "Upload", "Success")
        else:
            renderPopUpModal(self.parent, "Some files failed to upload", "Upload", "Warning")
        
        self.renderConditionAttachmentContainerContent(self.conditionAttachmentContainer)
    

    def viewConditionAttachmentDirectory(self):
        openAttachmentDirectory(self.customerId, self.parent, ATTACHMENT_TYPE, self.conditionModel.conditionId)


    def navigateToTreatmentDetailView(self, model):
        self.controller.setTreatmentID(model.treatmentID)
        self.controller.setCustomerID(self.conditionModel.customerId)
        self.controller.setConditionModel(self.conditionModel)
        self.controller.setConditionID(self.conditionModel.conditionId)
        self.controller.switch_frame(WINDOW_TREATMENT_DETAIL)


    def __init__(self, parent, controller, customerId, conditionModel):
        # !!!!!!!! customerId is formattted
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
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
        
        self.customerModel = self.controller.getCustomerModel()
        self.customerNameLabel = createDetailField(root=self.customerInfoFrame, fieldName="Customer Name", content=self.customerModel.customerName, row=0, column=0)
        createDetailField(root=self.customerInfoFrame, fieldName="IC", content=self.controller.getCustomerIC(), row=1, column=0)
        attach_floating_info(
            widget=self.customerNameLabel,  # ← bind to frame, not label
            parent=self,
            info_lines=[
                f"CustomerID:   {self.customerModel.oldCustomerId}",
                f"Gender:       {self.customerModel.gender}",
                f"Contact:      {self.customerModel.handphone}"
            ]
        )

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
        
        
        self.conditionHighlightFrame = ctk.CTkFrame(
            self.conditionDetailSubFrame,
            corner_radius=10,
            border_width=2,
            border_color=["#2563eb", "#3b82f6"],  # light / dark mode
            fg_color=["#f0f0f0", "#2a2a2a"]
        )
        self.conditionHighlightFrame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(5, 10), padx=(0, 0))
        self.conditionHighlightFrame.grid_columnconfigure(0, weight=2)
        self.conditionHighlightFrame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.conditionHighlightFrame,
            text="Condition Info",
            font=('Arial', 16),
            #font=('Arial', 16, 'bold'),
            text_color=["#000000", "#FFFFFF"]  # optional
        ).grid(row=0, column=0, sticky="w", pady=5, padx=10)

        self.treatedCheck = ctk.BooleanVar()
        ctk.CTkCheckBox(
            self.conditionHighlightFrame,
            text="Mark as treated",
            command=self.treatmentChecked,
            checkbox_height=16,
            checkbox_width=16,
            border_width=2,
            variable=self.treatedCheck
            #font=("Arial", 13, "bold")
        ).grid(row=0, column=1, sticky="e", padx=10, pady=5)
        

        createDetailField(root=self.conditionDetailsField, fieldName="Description", content=conditionModel.conditionDescription, row=1, column=0)
        createDetailField(root=self.conditionDetailsField, fieldName="Added Date", content=conditionModel.conditionDate, row=2, column=0)
        self.statusLabel = createDetailField(root=self.conditionDetailsField, fieldName="Status", content="Undergoing Treatement" if conditionModel.undergoingTreatment else "Treated", row=3, column=0)
        self.LoadTreatmentStatus()

        # Upload Attachment
        self.conditionAttachmentContainer = ctk.CTkFrame(
            self.conditionContainer,
        )
        self.conditionAttachmentContainer.grid(row=0, column=1, sticky="nsew", padx=(10, 5), pady=5)
        self.renderConditionAttachmentContainerContent(self.conditionAttachmentContainer)
        
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


        ctk.CTkLabel(self.treatmentListSubFrame, text="Existing Treatments", font=FONT["HEADER"]).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(self.treatmentListSubFrame, text="New Treatment", command=self.OpenAddTreatmentWindow).grid(row=0, column=1, sticky="e")

        #treatment
        self.treatmentList = getAllTreatmentByConditionID(self.conditionModel.conditionId)

        if len(self.treatmentList) <= 0:
            ctk.CTkLabel(self.treatmentListFrame, text="No treatment found", font=FONT["CONTENT"]).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
            return
        else:
            # # treatment list with scroll
            # self.scrollableTreatmentListContainer = ctk.CTkScrollableFrame(
            #     self.treatmentListFrame,
            #     bg_color='transparent',
            #     fg_color='transparent',
            #     width=500,
            #     height=250
            # )
            # self.scrollableTreatmentListContainer.grid_columnconfigure(0, weight=1)
            # self.scrollableTreatmentListContainer.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
            # for idx, treatment in enumerate(self.treatmentList):
            #     renderTreatmentSummaryBlockFunctionRevamp(
            #         self.scrollableTreatmentListContainer,treatment,hideButtons=False,
            #         on_click_view= self.navigateToTreatmentDetailView, 
            #         on_click=self.handleTreatmentBlockEditClick
            #     ).grid(row=idx, column=0, sticky="w")
            
            # treatment list without scroll
            self.treatmentListContainer = ctk.CTkFrame(
                self.treatmentListFrame,
                bg_color='transparent',
                fg_color='transparent'
            )
            self.treatmentListContainer.grid_columnconfigure(0, weight=1)
            self.treatmentListContainer.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
            for idx, treatment in enumerate(self.treatmentList):
                renderTreatmentSummaryBlockFunctionRevamp(
                    self.treatmentListContainer,
                    treatment,
                    self.controller.getIsHiddenAccess(),
                    hideButtons=False,
                    on_click_view=self.navigateToTreatmentDetailView,
                    on_click=self.handleTreatmentBlockEditClick,
                    row_index=idx,
                ).grid(row=idx, column=0, sticky="w")
                
            