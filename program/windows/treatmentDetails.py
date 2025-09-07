import customtkinter as ctk
import json
from tkinter.filedialog import askopenfilenames
from PIL import Image
from Constant.errorCode import SUCCESS
from Constant.treatmentDatabaseFunctions import getTreatmentByID,getAllTreatmentRevisionByID
from Constant.appConstant import FONT
from Components.customFields import createDetailField
from Components.treatmentSummaryBlock import renderTreatmentSummaryBlockFunctionRevamp
from Components.popupModal import renderPopUpModal
from services.customerFilesServices import getTreatmentPicturePath, renderFilePicker, uploadCustomerFile
from services.attachmentFilesServices import HasAttachment, uploadAttachmentFile, openAttachmentDirectory

#Constants
ATTACHMENT_TYPE = "Treatment"

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
        if self.controller.getIsHiddenAccess():
            cost_value = self.treatmentModel.treatmentCost

            # Try to parse JSON if it's a string
            if isinstance(cost_value, str):
                try:
                    parsed_value = json.loads(cost_value)
                    cost_value = parsed_value
                except json.JSONDecodeError:
                    pass  # Keep the string as is if it can't be parsed

            # Format depending on the type
            if isinstance(cost_value, dict):
                formatted_cost = ", ".join([f"RM {amount:.2f} ({method})" for method, amount in cost_value.items()])
            elif isinstance(cost_value, (int, float)):
                formatted_cost = f"RM {cost_value:.2f}"
            else:
                formatted_cost = "N/A"

            createDetailField(self.treatmentDetailFrame, "Cost", formatted_cost, 4, 0)

        #Levels
        createDetailField(self.treatmentDetailFrame, "Pain", self.treatmentModel.painLevel,5,0)
        createDetailField(self.treatmentDetailFrame, "Tense", self.treatmentModel.tenseLevel,6,0)    
        createDetailField(self.treatmentDetailFrame, "Sore", self.treatmentModel.soreLevel,7,0)
        createDetailField(self.treatmentDetailFrame, "Numb", self.treatmentModel.numbLevel,8,0)    
        

    def renderTreatmentPictureContainerContent(self, root):
        self.uploadTreatmentPictureBtn = None
        customerId = self.controller.getCustomerID()
        treatmentPicturePath = getTreatmentPicturePath(customerId, self.treatmentModel.treatmentID, ATTACHMENT_TYPE)
        
        if treatmentPicturePath is not None:
            self.renderTreatmentPicture(root, treatmentPicturePath)
        else:
            self.uploadTreatmentPictureBtn = ctk.CTkButton(root, text="Upload Picture", command=self.uploadTreatmentPicture)
            self.uploadTreatmentPictureBtn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


    def renderTreatmentAttachmentContainerContent(self, root):
        for widget in root.winfo_children():
            widget.destroy()
        
        treatmentHasAttachmentVar = HasAttachment(self.customerId, ATTACHMENT_TYPE)
        
        upload_btn = ctk.CTkButton(
            master=root,
            text="Upload",
            command=self.uploadTreatmentAttachment
        )
        upload_btn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        if treatmentHasAttachmentVar:
            view_btn = ctk.CTkButton(
                master=root,
                text="View",
                command=self.viewTreatmentAttachmentDirectory
            )
            view_btn.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)


    def uploadTreatmentAttachment(self):
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
                result = uploadAttachmentFile(self.customerId, filePath, self.root, ATTACHMENT_TYPE)
                if result != SUCCESS:
                     all_success = False
        else:
            return
        
        if all_success:
            renderPopUpModal(self.root, "All files uploaded successfully", "Upload", "Success")
        else:
            renderPopUpModal(self.root, "Some files failed to upload", "Upload", "Warning")
        
        self.renderTreatmentAttachmentContainerContent(self.treatmentAttachmentContainer)


    def viewTreatmentAttachmentDirectory(self):
        openAttachmentDirectory(self.customerId, self.root, ATTACHMENT_TYPE)


    def renderTreatmentPicture(self, root, treatmentPicturePath):
        image = Image.open(treatmentPicturePath)
        image = image.resize((250, 250))
        photo = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))

        label = ctk.CTkLabel(root, image=photo, text="")
        label.image = photo
        label.grid(row=0, column=0, sticky="nsew")


    def uploadTreatmentPicture(self):
        filePath = renderFilePicker(
            pdefaultextension='',
            pfiletypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ],
            ptitle="Select a treatment picture"
        )

        if not filePath:
            return  # User clicked cancel, do nothing

        customerId = self.controller.getCustomerID()
        result = uploadCustomerFile(customerId, filePath, self.root, self.treatmentModel.treatmentID, ATTACHMENT_TYPE)
        
        if result == SUCCESS:
            if self.uploadTreatmentPictureBtn:
                self.uploadTreatmentPictureBtn.destroy()
            self.renderTreatmentPicture(self.treatmentPictureContainer, filePath)


    def __init__(self, parent, controller, treatmentID):
        super().__init__(parent)
        self.controller = controller
        self.root = self

        self.treatmentModel = getTreatmentByID(treatmentID)
        self.customerId = self.controller.getCustomerID()

        self.masterFrame = ctk.CTkFrame(master=self.root, bg_color="transparent", fg_color='transparent')
        self.masterFrame.grid(column=0, row=0, sticky="nsew")

        # #Treatment details
        # self.treatmentDetailFrame = ctk.CTkFrame(master=self.masterFrame, bg_color="transparent", fg_color='transparent' )
        # self.treatmentDetailFrame.grid(column=0, row=0, sticky="nsew")
        # ctk.CTkLabel(
        #     self.treatmentDetailFrame,
        #     text="Treatment Details",
        #     bg_color='transparent',  # Make the label background transparent
        #     font=FONT["HEADER"],
        #     anchor="w"  # Align text inside label to left
        # ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
        # self.renderTreatmentDetails()
        
        # # Treatment Picture
        # self.treatmentPictureContainer = ctk.CTkFrame(
        #     self.masterFrame,
        #     width=250,
        #     height=250,
        #     fg_color="transparent"
        # )
        # self.treatmentPictureContainer.grid_propagate(False)  # Prevent resizing to fit children
        # self.treatmentPictureContainer.grid(row=2, column=0, padx=10, pady=10)
        # self.renderTreatmentPictureContainerContent(self.treatmentPictureContainer)
        
        # Top Section Frame: Holds both treatment details and image/button side by side
        self.topSectionFrame = ctk.CTkFrame(master=self.masterFrame, bg_color="transparent", fg_color="transparent")
        self.topSectionFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.topSectionFrame.grid_columnconfigure(0, weight=1)
        self.topSectionFrame.grid_columnconfigure(1, weight=0)

        # Treatment Detail Frame (Left)
        self.treatmentDetailFrame = ctk.CTkFrame(master=self.topSectionFrame, bg_color="transparent", fg_color="transparent")
        self.treatmentDetailFrame.grid(column=0, row=0, sticky="nw")

        ctk.CTkLabel(
            self.treatmentDetailFrame,
            text="Treatment Details",
            bg_color='transparent',
            font=FONT["HEADER"],
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)

        self.renderTreatmentDetails()

        # Upload Attachment
        self.treatmentAttachmentContainer = ctk.CTkFrame(
            master=self.topSectionFrame,
            width=250,
            height=250,
            fg_color="transparent"
        )
        self.treatmentAttachmentContainer.grid_propagate(False)
        self.treatmentAttachmentContainer.grid(row=0, column=1, padx=20, pady=10, sticky="n")
        self.renderTreatmentAttachmentContainerContent(self.treatmentAttachmentContainer)

        #Treatment ammendment history
        self.treatmentRevisionHistoryFrame = ctk.CTkFrame(master=self.masterFrame, bg_color="transparent", fg_color='transparent' )
        self.treatmentRevisionHistoryFrame.grid(column=0, row=1, sticky="nsew")
        self.treatmentRevisionHistoryFrame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            self.treatmentRevisionHistoryFrame,
            text="Revision History",
            bg_color='transparent',  # Make the label background transparent
            font=FONT["HEADER"],
            anchor="w"  # Align text inside label to left
        ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=10)

        self.treatmentRevisionList = getAllTreatmentRevisionByID(self.treatmentModel.treatmentID)

        if len(self.treatmentRevisionList) <= 0:
            ctk.CTkLabel(self.treatmentRevisionHistoryFrame, text="No treatment found", font=FONT["CONTENT"]).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
            return
        else:
            self.scrollableTreatmentListContainer = ctk.CTkScrollableFrame(
                self.treatmentRevisionHistoryFrame,
                bg_color='transparent',
                fg_color='transparent',
                height=250  # No fixed width!
            )
            self.scrollableTreatmentListContainer.grid_columnconfigure(0, weight=1)
            self.scrollableTreatmentListContainer.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)

            for idx, treatment in enumerate(self.treatmentRevisionList):
                renderTreatmentSummaryBlockFunctionRevamp(
                    self.scrollableTreatmentListContainer, treatment, self.controller.getIsHiddenAccess(),
                    hideButtons=True, row_index=idx
                ).grid(row=idx, column=0, sticky="w")
                
            


