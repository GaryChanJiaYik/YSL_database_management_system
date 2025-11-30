import customtkinter
import os
from tkinter.filedialog import askopenfilename
from Constant.appConstant import (
    STANDARD_WINDOW_SIZE, WINDOW_CONDITION_DETAIL, WINDOW_EDIT_CONDITION, WINDOW_EDIT_CUSTOMER, 
    WINDOW_CUSTOMER_DETAIL, WINDOW_ADD_TREATMENT, FONT
) 
from Constant.databaseManipulationFunctions import searchForSingleUser, addOldCustomerID
from Constant.dbColumn import customerModelAttributeToField, oldCustomerId, name, ic
from Constant.converterFunctions import convertTimeStampToId
from Constant.errorCode import SUCCESS
from Constant.generatorFunctions import generateUUID
from Constant.fileKeywords import CONSENT_FORM_KEYWORD
from Constant.converterFunctions import convertTimeStampToId
from Components.popupModal import renderPopUpModal
from Components.datePickerModal import DatePickerModal
from Components.timePickerModal import TimePickerModal
from Components.datetimePickerModal import DateTimePickerModal
from Components.conditionModelBlock import instantiateConditionModelBlock
from services.conditionDbFunctions import insertConditionToDb, getAllConditionsByCustomerId
from services.customerFilesServices import (
    customerHasConsentForm, viewCustomerFilePDF, uploadCustomerFile, deleteCustomerFile
)
from services.reportGenerateServices import generateCustomerConsentForm
from services.attachmentFilesServices import HasAttachment, handleAttachmentUpload, openAttachmentDirectory
from Model.conditionModel import ConditionModel
from datetime import datetime
from utils import setEntryValue

#Constants
ATTACHMENT_TYPE= "Customer"

class CustomerDetailsViewRevamp(customtkinter.CTkFrame):

    def createDetailField(self, root, fieldName, content, row, column, rowspan=1):
        # Field name label
        customtkinter.CTkLabel(
            root,
            text="Customer ID" if fieldName == "Old Customer ID" else fieldName,
            font=FONT["LABEL"],
            bg_color='transparent',
            anchor="w"
        ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)

        #If is old customer id and is empty,
        if fieldName == oldCustomerId and content == "":
            self.oldCustomerIdInputFieldContainer = None
            self.addOldCustomerIdButton = None
            self.renderAddOldCustomerIdButton(root, row, column, rowspan)
        else:
            # Content label (support rowspan)
            customtkinter.CTkLabel(
                root,
                text=content if content != "" else "---", 
                font=FONT["CONTENT"],
                bg_color='transparent',
                wraplength=200,
                anchor="w",
                justify="left",
            ).grid(row=row, column=column + 1, rowspan=rowspan, sticky="w", padx=(5, 10), pady=5)
            
            # if fieldName == name and content != "":
            if name.startswith(fieldName) and content != "":
                self.controller.setCustomerName(content)
            
            # if fieldName == IC and content != "":
            if ic.startswith(fieldName) and content != "":
                self.controller.setCustomerIC(content)

    def renderAddOldCustomerIdButton(self, root, row, column, rowspan=1):
        if self.oldCustomerIdInputFieldContainer is not None:
            self.oldCustomerIdInputFieldContainer.destroy()
            
        self.addOldCustomerIdButton = customtkinter.CTkButton(
                root,
                text="Add ID",
                command=lambda: self.renderCustomerOldIDInputField(root,row, column+1, rowspan),
            )

        self.addOldCustomerIdButton.grid(row=row, column=column+1, rowspan=rowspan, sticky="w", padx=(5, 10), pady=5)
        
    def renderCustomerOldIDInputField(self,root,row, column, rowspan=1):
        if self.addOldCustomerIdButton is not None:
            self.addOldCustomerIdButton.destroy()  # Remove the button

        self.oldCustomerIdInputFieldContainer = customtkinter.CTkFrame(master=root, bg_color="transparent")
        self.oldCustomerIdInputFieldContainer.grid(row=row, column=column, rowspan=rowspan, sticky="w", padx=(2, 2), pady=0)

        self.oldCustomerIdInputFieldContainer.grid_columnconfigure(0, weight=2)
        self.oldCustomerIdInputFieldContainer.grid_columnconfigure(1, weight=1)
        self.oldCustomerIdInputFieldContainer.grid_columnconfigure(2, weight=1)

        self.oldCustomerIdInputField = customtkinter.CTkEntry(
            master=self.oldCustomerIdInputFieldContainer,
            placeholder_text="Enter old ID",
            width=110,
        )

        self.oldCustomerIdInputField.grid(row=0, column=0, rowspan=1, sticky="w", padx=(5, 10), pady=5)
        self.submitOldCustomerIdButton = customtkinter.CTkButton(
            master=self.oldCustomerIdInputFieldContainer,
            text="Submit",
            command=lambda: self.addOldCustomerIdToDb(root,row, column),
            fg_color="green",
            hover_color="darkgreen",
            width=10,
        )

        self.submitOldCustomerIdButton.grid(row=0, column=1, rowspan=1, sticky="w")

        self.closeOldCustomerIdInputField = customtkinter.CTkButton(
            master=self.oldCustomerIdInputFieldContainer,
            text="Close",
            command=lambda: self.renderAddOldCustomerIdButton(root, row, column-1, rowspan),
            fg_color="red",
            hover_color="darkred",
            width=10,
        )
        self.closeOldCustomerIdInputField.grid(row=0, column=2, rowspan=1, sticky="w", padx=(5, 10), pady=5)

    def addOldCustomerIdToDb(self, root, row, column):
        oldCustomerId = self.oldCustomerIdInputField.get()

        if oldCustomerId:
            addOldCustomerID(self.customerTimeStamp, self.oldCustomerIdInputField.get())

            self.oldCustomerIdInputFieldContainer.destroy()  # Remove the input field container

            #display this new data
            customtkinter.CTkLabel(
                    root,
                    text=oldCustomerId, 
                    bg_color='transparent',
                    wraplength=200,
                    anchor="w",
                    justify="left",
                ).grid(row=row, column=column, rowspan=1, sticky="w", padx=(5, 10), pady=5)
        else:
            renderPopUpModal(root, "Old ID CANNOT be empty!", "Error", "Error")

    def addConditionToDb(self):
        # Get date and time from user input
        datetime_str = self.datetime_value.get().strip()
        
        # Comine to create datetime object
        try:
            combined_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M %p")
            formatted_datetime = combined_datetime.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date/time format. Using current datetime.")
            formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        conditionModel = ConditionModel(
            customerId=convertTimeStampToId(self.customerId),
            condition_id= generateUUID(),  # Assuming this is auto-generated in the database
            conditionDescription=self.conditionEntry.get("1.0", "end-1c"),
            undergoingTreatment=True,
            conditionDate= formatted_datetime
        )
        insertConditionToDb(conditionModel)

        # Re-render the UI
        self.conditionList = getAllConditionsByCustomerId(self.customerId)
        self.renderConditionList()
        
        self.closeAddConditionFrame()  # Close the frame after submission

    
    def openAddConditionWindow(self):
        if self.addConditionFrame is None:
            self.renderAddConditionFrame(self.conditionFrame)    


    def renderAddConditionFrame(self, parentContainer):
        # Create a frame for the add condition button
        self.addConditionFrame = customtkinter.CTkFrame(master=parentContainer, bg_color="transparent")
        self.addConditionFrame.grid(column=0, row=0, sticky="w", padx=(10, 5), pady=5)

        customtkinter.CTkLabel(
            self.addConditionFrame,
            text="Add Condition",).grid(row=0, column=0, sticky="nw", padx=(10, 5), pady=5)

        # Add condition entry field
        self.conditionEntry = customtkinter.CTkTextbox(
            master=self.addConditionFrame,
            width=350,
            height=100
        )
        self.conditionEntry.grid(row=0, column=1, sticky="w", padx=(10, 5), pady=5)
        
        # Combined DateTime Field
        customtkinter.CTkLabel(self.addConditionFrame, text="Date & Time:", pady=1).grid(
            row=1, column=0, sticky="w", padx=(10, 5), pady=(10, 0)
        )

        datetimeInputFrame = customtkinter.CTkFrame(self.addConditionFrame, fg_color="transparent")
        datetimeInputFrame.grid(row=1, column=1, sticky="w", padx=(0, 5), pady=(10, 0))

        # Combined datetime field in 24hr format
        self.datetime_value = customtkinter.CTkEntry(datetimeInputFrame, width=180)
        self.datetime_value.insert(0, datetime.now().strftime("%Y-%m-%d %I:%M %p"))
        self.datetime_value.configure(state="disabled")
        self.datetime_value.grid(row=0, column=0, padx=(0, 10))

        customtkinter.CTkButton(
            datetimeInputFrame,
            text="Edit",
            width=60,
            command=lambda: DateTimePickerModal.open_datetime_picker(
                parent=self,
                current_datetime_str=self.datetime_value.get().strip(),
                on_selected=lambda datetime_str: setEntryValue(self.datetime_value, datetime_str)
            )
        ).grid(row=0, column=1)

        # Add and close buttons
        buttonFrame = customtkinter.CTkFrame(self.addConditionFrame, fg_color="transparent")
        buttonFrame.grid(row=3, column=0, columnspan=2, sticky="w", padx=(10, 5), pady=(10, 0))
        buttonFrame.grid_columnconfigure(0, weight=0)
        buttonFrame.grid_columnconfigure(1, weight=0)

        customtkinter.CTkButton(
            master=buttonFrame,
            text="Add",
            command=lambda: self.addConditionToDb(),
        ).grid(row=0, column=0, padx=(0, 10))

        customtkinter.CTkButton(
            master=buttonFrame,
            text="Close",
            command=lambda: self.closeAddConditionFrame(),
            fg_color="red",
            hover_color="darkred",
        ).grid(row=0, column=1)
        
    
    def openDatePicker(self):
        DatePickerModal.open_date_picker(
            parent=self,
            current_date_str=self.date_value.get(),
            on_selected=lambda date_str: setEntryValue(self.date_value, date_str)
        )

    
    def openTimePicker(self):
        TimePickerModal.open_time_picker(
            parent=self,
            current_time_str=self.time_value.get().strip(),
            on_selected=lambda time_str: setEntryValue(self.time_value, time_str)
        )


    def openDateTimePicker(self):
        DateTimePickerModal.open_datetime_picker(
                parent=self,
                current_datetime_str=self.datetime_value.get().strip(),
                on_selected=lambda datetime_str: setEntryValue(self.datetime_value, datetime_str)
            )

    def closeAddConditionFrame(self):
        if self.addConditionFrame:
            self.addConditionFrame.destroy()  # remove the frame from the screen
            self.addConditionFrame = None     # reset state


    def renderConditionList(self):
        # Clear the existing widgets inside the container
        if hasattr(self, "ConditionListContainer") and self.ConditionListContainer.winfo_children():
            for widget in self.ConditionListContainer.winfo_children():
                widget.destroy()
        
        self.conditionList.sort(
            key=lambda c: datetime.strptime(c.conditionDate, "%Y-%m-%d %H:%M"), 
            reverse=True
        )
        
        #Conditions list 
        self.ConditionListContainer = customtkinter.CTkFrame(master=self.conditionFrame, bg_color="transparent", fg_color='transparent')
        self.ConditionListContainer.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
        self.ConditionListContainer.grid_columnconfigure(0, weight=1)

        for idx, condition in enumerate(self.conditionList):
            # Create a new condition model block for each condition
            instantiateConditionModelBlock(
                self.ConditionListContainer, condition, 0, idx, self.openConditionDetailsWindowCallback, 
                self.openEditConditionDetailsWindowCallback, self.OpenAddTreatmentWindow, self.controller.getIsHiddenAccess()
            )


    def openConditionDetailsWindowCallback(self, cm):
        self.controller.setCustomerID(self.customerId)
        self.controller.setConditionModel(cm)
        self.controller.switch_frame(WINDOW_CONDITION_DETAIL)
        print("Clicked condition details for:", cm.conditionId)
        
        
    def openEditConditionDetailsWindowCallback(self, cm):
        self.controller.setCustomerID(self.customerId)
        self.controller.setConditionModel(cm)
        self.controller.switch_frame(WINDOW_EDIT_CONDITION)
        print("Clicked Edit Condition:", cm.conditionId)
        
        
    def OpenAddTreatmentWindow(self, cm):
        self.controller.setCustomerID(cm.customerId)
        self.controller.setConditionID(cm.conditionId);
        self.controller.setConditionModel(cm)
        self.controller.switch_frame(WINDOW_ADD_TREATMENT, previousWindow=WINDOW_CUSTOMER_DETAIL)


    def renderConsentFormOptionButton(self, row, column):
        customerHasConsentFormVar = customerHasConsentForm(self.customerId, self.customerModel.customerName, ATTACHMENT_TYPE)
        print("")
        print("Customer has consent form: ", customerHasConsentFormVar)
        print("")
        
        if customerHasConsentFormVar:
            # Create a button to upload consent form
            customtkinter.CTkButton(
                master=self.customerDetailFrame,
                text="Upload",
                command=lambda: self.uploadOrReplaceConsentForm(),
            ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)
            
            # Create a button to view consent form
            customtkinter.CTkButton(
                master=self.customerDetailFrame,
                text="View",
                command=lambda: self.viewCustomerAttachmentDirectory() # self.viewConsentForm(),
            ).grid(row=row, column=column + 1, sticky="w", padx=(10, 5), pady=5)
        else:
            # Create a button to generate consent form
            customtkinter.CTkButton(
                master=self.customerDetailFrame,
                text="Generate",
                command=lambda: self.generateConsentForm(),
            ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)

            # # Delete button
            # customtkinter.CTkButton(
            #     master=self.customerDetailFrame,
            #     text="Delete",
            #     # command=lambda: self.renderCustomerDetailSection(),
            #     command=lambda: self.deleteConsentForm(),
            # ).grid(row=row, column=column +1, sticky="w", padx=(10, 5), pady=5)
            
    def generateConsentForm(self):
        # # PDF filename
        # today_str = datetime.now().strftime("%Y%m%d%H%M")
        # filename = f"{today_str}_ConsentForm.pdf"

        # # Folder path
        # customerFolder = f"data/attachment/{self.customerId}/{ATTACHMENT_TYPE}"
        # fullFolderPath = resourcePath(customerFolder)

        # # Make sure folder exists
        # os.makedirs(fullFolderPath, exist_ok=True)

        # # Full file path
        # pdf_path = os.path.join(fullFolderPath, filename)

        # Generate the PDF
        pdf_path = generateCustomerConsentForm(self.customerModel, self.customerId)

        # Save to system using existing file handler
        # uploadCustomerFile(self.customerId, pdf_path, self.root, CONSENT_FORM_KEYWORD, ATTACHMENT_TYPE)

        renderPopUpModal(self.root, "Consent form generated successfully!", "Generate", "Success")

        # Refresh UI
        self.renderCustomerDetailSection()

    
    
    def renderCustomerAttachmentOptionButton(self, row, column):
        customerHasAttachmentVar = HasAttachment(self.customerId, ATTACHMENT_TYPE)
    
        # Create a button to upload attachment
        customtkinter.CTkButton(
            master=self.customerDetailFrame,
            text="Upload",
            command=lambda: self.uploadCustomerAttachment(),
        ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)
        
        if customerHasAttachmentVar:
            # Create a button to open the customer attachment directory
            customtkinter.CTkButton(
                master=self.customerDetailFrame,
                text="View",
                command=lambda: self.viewCustomerAttachmentDirectory(),
            ).grid(row=row, column=column+1, sticky="w", padx=(10, 5), pady=5)

    
    def uploadOrReplaceConsentForm(self):
        filePath = askopenfilename(defaultextension='.pdf', filetypes=[('pdf file', '*.pdf')])
        if filePath:
            uploadCustomerFile(self.customerId, filePath, self.root, CONSENT_FORM_KEYWORD, ATTACHMENT_TYPE)
            self.renderCustomerDetailSection()
    
    
    def uploadCustomerAttachment(self):
        handleAttachmentUpload(self.customerId, self.root, ATTACHMENT_TYPE)
        self.renderCustomerDetailSection()
    
    
    def viewCustomerAttachmentDirectory(self):
        openAttachmentDirectory(self.customerId, self.root, ATTACHMENT_TYPE)
    
    
    def deleteConsentForm(self):
        success = deleteCustomerFile(self.customerId, CONSENT_FORM_KEYWORD, ATTACHMENT_TYPE)

        if success:
            renderPopUpModal(self.root, "Consent form deleted successfully.", "Delete", "Success")
        else:
            renderPopUpModal(self.root, "No consent form found or error occurred.", "Delete", "Error")

        # Refresh the UI
        self.renderCustomerDetailSection()


    def viewConsentForm(self):
        viewCustomerFilePDF(self.customerId, ATTACHMENT_TYPE)
        
        
    def editCustomerDetails(self):
        self.controller.setCustomerID(self.customerId)
        self.controller.switch_frame(WINDOW_EDIT_CUSTOMER, previousWindow=WINDOW_CUSTOMER_DETAIL)


    def renderCustomerDetailSection(self):
        # If already exists (refresh case), destroy it
        if hasattr(self, "customerDetailFrame") and self.customerDetailFrame:
            self.customerDetailFrame.destroy()

        # Re-fetch customer data
        self.customerModel = searchForSingleUser(self.customerId)
        self.controller.setCustomerModel(self.customerModel)
        
        self.customerDetailFrame = customtkinter.CTkFrame(master=self.root, bg_color="transparent")
        self.customerDetailFrame.grid_columnconfigure(0, weight=1)
        self.customerDetailFrame.grid_columnconfigure(1, minsize=330)
        self.customerDetailFrame.grid_columnconfigure(2, minsize=80)
        self.customerDetailFrame.grid_columnconfigure(3, weight=1)
        self.customerDetailFrame.grid_columnconfigure(4, weight=2)
        self.customerDetailFrame.grid(column=0, row=0, sticky="nsew", pady=(0,5))

        customerHeaderFrame = customtkinter.CTkFrame(master=self.customerDetailFrame, bg_color="transparent", fg_color="transparent")
        customerHeaderFrame.grid(row=0, column=0, columnspan=2, sticky="w", padx=(10, 5), pady=5)
        customerHeaderFrame.grid_columnconfigure(0, weight=0)
        customerHeaderFrame.grid_columnconfigure(1, weight=0)

        customtkinter.CTkLabel(
            customerHeaderFrame,
            text="Customer Details",
            font=FONT["HEADER"],
            anchor="w",
            bg_color='transparent',
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=0)

        customtkinter.CTkButton(
            customerHeaderFrame,
            text="Edit",
            width=60,
            command=self.editCustomerDetails
        ).grid(row=0, column=1, sticky="w")


        index = 0
       # Set of fields to go into column 2 (column index 3)
        columnTwoKeys = {'address', 'handphone', 'instagram', 'howDidYouFindUs', 'consent'}

        columnOneRowIndex = 1
        columnTwoRowIndex = 1

        for key, value in vars(self.customerModel).items():
            # Skip customerId
            if key == 'customerId':
                continue
            
            # Get field name and value
            field_name = customerModelAttributeToField.get(key, key)
            display_value = convertTimeStampToId(value) if key == 'customerId' else value
            # Decide which column to put this field in
            
            # for 'consent'
            if key == 'consent':
                # Label for "Customer Attachment"
                customtkinter.CTkLabel(
                    self.customerDetailFrame,
                    text="Customer Attachment",
                    font=FONT["LABEL"],
                    anchor="w",
                    bg_color='transparent',
                ).grid(row=columnTwoRowIndex, column=3, sticky="w", padx=(10, 10), pady=(0, 5))

                #render consent form option button
                if display_value == "Disagree不同意":
                    customtkinter.CTkLabel(
                        self.customerDetailFrame,
                        text=display_value,
                        font=FONT["CONTENT"],
                        anchor="w",
                        bg_color='transparent',
                    ).grid(row=columnTwoRowIndex, column=4, sticky="w", padx=(10, 10), pady=(0, 5))
                else:
                    # Will display upload consent form if DO NOT HAVE consent form
                    # Will display view consent form if HAVE consent form
                    self.renderCustomerAttachmentOptionButton(row=columnTwoRowIndex, column=4)

                columnTwoRowIndex += 1
                
                customtkinter.CTkLabel(
                    self.customerDetailFrame,
                    text="Consent Form",
                    font=FONT["LABEL"],
                    anchor="w",
                    bg_color='transparent',
                ).grid(row=columnTwoRowIndex, column=3, sticky="w", padx=(10, 10), pady=(0, 5))

                # Render consent form buttons (Upload / View / Delete)
                self.renderConsentFormOptionButton(row=columnTwoRowIndex, column=4)

                columnTwoRowIndex += 1
                continue  # Skip default rendering
            
            # for normal data label
            if key in columnTwoKeys:
                 # Address field spans 2 rows

                self.createDetailField(
                    self.customerDetailFrame, field_name, display_value,
                    row=columnTwoRowIndex, column=3
                )
                columnTwoRowIndex += 1
      
            else:
                self.createDetailField(
                    self.customerDetailFrame, field_name, display_value,
                    row=columnOneRowIndex, column=0
                )
                columnOneRowIndex += 1
        

    def __init__(self, parent, controller, customerId):
        super().__init__(parent)
        self.controller = controller
        self.root = self
        self.customerTimeStamp = customerId
        self.customerId = convertTimeStampToId(customerId) 
        # self.customerModel = searchForSingleUser(self.customerId)
        # print("THIS IS THE CUSTOMER MODEL")
        # print(self.customerModel)

        self.conditionList = getAllConditionsByCustomerId(self.customerId)
        print("customerId")
        print(self.customerId)

        print("length of customer conditions")
        print(len(self.conditionList))

        #For customer details
        self.renderCustomerDetailSection()

        #For condition
        self.conditionFrame = customtkinter.CTkFrame(master=self.root, bg_color="transparent")
        self.conditionFrame.grid_columnconfigure(0, weight=1)
        self.conditionFrame.grid(column=0, row=1, sticky="nsew")

        # Create a frame to hold label and button together in the same row
        conditionHeaderFrame = customtkinter.CTkFrame(master=self.conditionFrame, bg_color="transparent", fg_color="transparent")
        conditionHeaderFrame.grid(row=0, column=0, columnspan=2, sticky="w", padx=(10, 5), pady=5)
        conditionHeaderFrame.grid_columnconfigure(0, weight=0)
        conditionHeaderFrame.grid_columnconfigure(1, weight=0)

        customtkinter.CTkLabel(
            master=conditionHeaderFrame,
            text="Conditions",
            font=FONT["HEADER"],
            anchor="w",
            bg_color='transparent',
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=0)
        
        self.addConditionButton = customtkinter.CTkButton(
            master=conditionHeaderFrame,
            text="New Condition",
            command=self.openAddConditionWindow,
            width=120,
        )
        self.addConditionButton.grid(row=0, column=1, sticky="w")

        self.addConditionFrame = None
        
        #Conditions list
        self.renderConditionList()
