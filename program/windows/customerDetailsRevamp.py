import customtkinter
from Constant.appConstant import STANDARD_WINDOW_SIZE,WINDOW_CONDITION_DETAIL
from Constant.databaseManipulationFunctions import searchForSingleUser, addOldCustomerID
from Constant.dbColumn import customerModelAttributeToField, oldCustomerId, name
from Constant.converterFunctions import convertTimeStampToId
from services.conditionDbFunctions import insertConditionToDb, getAllConditionsByCustomerId
from Model.conditionModel import ConditionModel
from Constant.generatorFunctions import generateUUID
from Constant.converterFunctions import convertTimeStampToId, getFormattedDateTime
import datetime
from Components.conditionModelBlock import instantiateConditionModelBlock
from windows.conditionDetailsView import ConditionDetailsView
from services.customerFilesServices import customerHasConsentForm, viewCustomerFilePDF, uploadCustomerFile
from tkinter.filedialog import askopenfilename
from Components.popupModal import renderPopUpModal
from Constant.fileKeywords import CONSENT_FORM_KEYWORD
import shutil

class CustomerDetailsViewRevamp(customtkinter.CTkFrame):

    def createDetailField(self, root, fieldName, content, row, column, rowspan=1):
        # Field name label
        customtkinter.CTkLabel(
            root,
            text=fieldName,
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
                bg_color='transparent',
                wraplength=200,
                anchor="w",
                justify="left",
            ).grid(row=row, column=column + 1, rowspan=rowspan, sticky="w", padx=(5, 10), pady=5)
            
            # if fieldName == name and content != "":
            if name.startswith(fieldName) and content != "":
                self.controller.setCustomerName(content)

    def renderAddOldCustomerIdButton(self, root, row, column, rowspan=1):
        if self.oldCustomerIdInputFieldContainer is not None:
            self.oldCustomerIdInputFieldContainer.destroy()
            
        self.addOldCustomerIdButton = customtkinter.CTkButton(
                root,
                text="Add old ID",
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
        conditionModel = ConditionModel(
            customerId=convertTimeStampToId(self.customerId),
            condition_id= generateUUID(),  # Assuming this is auto-generated in the database
            conditionDescription=self.conditionEntry.get("1.0", "end-1c"),
            undergoingTreatment=True,
            conditionDate= getFormattedDateTime()  # Placeholder date, replace with actual date if needed
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


        # Add condition button
        customtkinter.CTkButton(
            master=self.addConditionFrame,
            text="Submit",
            command=lambda: self.addConditionToDb(),
        ).grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)


        customtkinter.CTkButton(
            master=self.addConditionFrame,
            text="Close",
            command=lambda: self.closeAddConditionFrame(),
            fg_color="red",
            hover_color="darkred",
        ).grid(row=1, column=1, sticky="w", padx=(10, 5), pady=5)
        self.addConditionFrame.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)

    def closeAddConditionFrame(self):
        if self.addConditionFrame:
            self.addConditionFrame.destroy()  # remove the frame from the screen
            self.addConditionFrame = None     # reset state

    def renderConditionList(self):
        # Clear the existing widgets inside the container
        if hasattr(self, "ConditionListContainer") and self.ConditionListContainer.winfo_children():
            for widget in self.ConditionListContainer.winfo_children():
                widget.destroy()
        
        #Conditions list 
        self.ConditionListContainer = customtkinter.CTkFrame(master=self.conditionFrame, bg_color="transparent", fg_color='transparent')
        self.ConditionListContainer.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
        self.ConditionListContainer.grid_columnconfigure(0, weight=1)


        for idx, condition in enumerate(self.conditionList):
            # Create a new condition model block for each condition
            instantiateConditionModelBlock(
                self.ConditionListContainer, condition, 0, idx, self.openConditionDetailsWindowCallback
            )

    def openConditionDetailsWindowCallback(self, cm):
        self.controller.setCustomerID(self.customerId)

        self.controller.setConditionModel(cm)


        self.controller.switch_frame(WINDOW_CONDITION_DETAIL)
        #ConditionDetailsView(self.root, self.customerId, cm )
        print("Clicked condition details for:", cm.conditionId)

    def renderConsentFormOptionButton(self, row, column):
        
        customerHasConsentFormVar = customerHasConsentForm(self.customerId)
        print("")
        print("Customer has consent form: ", customerHasConsentFormVar)
        print("")
        if not customerHasConsentFormVar:
            # Create a button to upload consent form
            customtkinter.CTkButton(
                master=self.customerDetailFrame,
                text="Upload Consent Form",
                command=lambda: self.uploadOrReplaceConsentForm(),
            ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)
        else:
            # Create a button to view consent form
            customtkinter.CTkButton(
                master=self.customerDetailFrame,
                text="View Consent Form",
                command=lambda: self.viewConsentForm(),
            ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)

            # Updaet button
            customtkinter.CTkButton(
                master=self.customerDetailFrame,
                text="Update Consent Form",
                command=lambda: self.uploadOrReplaceConsentForm(),
            ).grid(row=row, column=column +1, sticky="w", padx=(10, 5), pady=5)

    
    def uploadOrReplaceConsentForm(self):
        filePath = askopenfilename(defaultextension='.pdf', filetypes=[('pdf file', '*.pdf')])
        if filePath:
            uploadCustomerFile(self.customerId, filePath, self.root, CONSENT_FORM_KEYWORD)

    def viewConsentForm(self):
        viewCustomerFilePDF(self.customerId)



    def __init__(self, parent, controller, customerId):
        super().__init__(parent)
        self.controller = controller
        self.root = self

        self.customerTimeStamp = customerId
        self.customerId = convertTimeStampToId(customerId) 
        self.customerModel = searchForSingleUser(self.customerId)
        print("THIS IS THE CUSTOMER MODEL")
        print(self.customerModel)

        self.conditionList = getAllConditionsByCustomerId(self.customerId)
        print("customerId")
        print(self.customerId)

        print("length of customer conditions")
        print(len(self.conditionList))


        self.customerDetailFrame = customtkinter.CTkFrame(master=self.root, bg_color="transparent")
        self.customerDetailFrame.grid_columnconfigure(0, weight=1)
        self.customerDetailFrame.grid_columnconfigure(1, minsize=330)
        self.customerDetailFrame.grid_columnconfigure(2, minsize=80)
        self.customerDetailFrame.grid_columnconfigure(3, weight=1)
        self.customerDetailFrame.grid_columnconfigure(4, weight=2)
        self.customerDetailFrame.grid(column=0, row=0, sticky="nsew")

        customtkinter.CTkLabel(
            self.customerDetailFrame,
            text="Customer Details",
            bg_color='transparent',  # Make the label background transparent
            font=('Arial', 16),
            anchor="w"  # Align text inside label to left
        ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)





        index = 0
       # Set of fields to go into column 2 (column index 3)
        columnTwoKeys = {'address', 'handphone', 'instagram', 'howDidYouFindUs'}

        columnOneRowIndex = 1
        columnTwoRowIndex = 1

        for key, value in vars(self.customerModel).items():
            # Get field name and value
            field_name = customerModelAttributeToField.get(key, key)
            display_value = convertTimeStampToId(value) if key == 'customerId' else value
            # Decide which column to put this field in
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

        #render consent form option button
        

        # Will display upload consent form if DO NOT HAVE consent form
        # Will display view consent form if HAVE consent form
        self.renderConsentFormOptionButton(row=columnTwoRowIndex, column=3)


        #For condition
        self.conditionFrame = customtkinter.CTkFrame(master=self.root, bg_color="transparent")
        self.conditionFrame.grid_columnconfigure(0, weight=1)
        self.conditionFrame.grid(column=0, row=1, sticky="nsew")

        customtkinter.CTkLabel(
            self.conditionFrame,
            text="Conditions",
            bg_color='transparent', # Make the label background transparent
            font=('Arial', 16),
            anchor="w"  # Align text inside label to left
        ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)

        # Add conditions
        self.addConditionButton = customtkinter.CTkButton(
            master=self.conditionFrame,
            text="Add New Condition",
            command=lambda: self.openAddConditionWindow(),

        )
        self.addConditionButton.grid(row=0, column=1, sticky="w", padx=(10, 5), pady=5)


        self.addConditionFrame = None
        
        #Conditions list
        self.renderConditionList()






