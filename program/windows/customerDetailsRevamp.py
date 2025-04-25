import customtkinter
from Constant.appConstant import STANDARD_WINDOW_SIZE
from Constant.databaseManipulationFunctions import searchForSingleUser
from Constant.dbColumn import customerModelAttributeToField
from Constant.converterFunctions import convertTimeStampToId
from services.conditionDbFunctions import insertConditionToDb, getAllConditionsByCustomerId
from Model.conditionModel import ConditionModel
from Constant.generatorFunctions import generateUUID
from Constant.converterFunctions import convertTimeStampToId, getFormattedDateTime
import datetime
from Components.conditionModelBlock import instantiateConditionModelBlock
from windows.conditionDetailsView import ConditionDetailsView


class CustomerDetailsViewRevamp:

    def createDetailField(self, root, fieldName, content, row, column, rowspan=1):
        # Field name label
        customtkinter.CTkLabel(
            root,
            text=fieldName,
            bg_color='transparent',
            anchor="w"
        ).grid(row=row, column=column, sticky="w", padx=(10, 5), pady=5)
        # Content label (support rowspan)
        customtkinter.CTkLabel(
            root,
            text=content if content != "" else "---", 
            bg_color='transparent',
            wraplength=200,
            anchor="w",
            justify="left",
        ).grid(row=row, column=column + 1, rowspan=rowspan, sticky="w", padx=(5, 10), pady=5)

    def addConditionToDb(self):
        print(self.conditionEntry.get("1.0", "end-1c"))  # Get the text from the Text widget
        conditionModel = ConditionModel(
            customerId=convertTimeStampToId(self.customerId),
            condition_id= generateUUID(),  # Assuming this is auto-generated in the database
            conditionDescription=self.conditionEntry.get("1.0", "end-1c"),
            undergoingTreatment=True,
            conditionDate= getFormattedDateTime()  # Placeholder date, replace with actual date if needed
        )
        insertConditionToDb(conditionModel)
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


    def openConditionDetailsWindowCallback(self, cm):
        ConditionDetailsView(self.root, self.customerId, cm )
        print("Clicked condition details for:", cm.conditionId)

    def __init__(self, root, customerId):
        self.root = root
        self.newWindow = customtkinter.CTkToplevel(self.root)
        self.newWindow.columnconfigure(0, weight=1)
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Customer Details")
        
        # sets the geometry of toplevel
        self.newWindow.geometry(STANDARD_WINDOW_SIZE)

        self.customerId = convertTimeStampToId(customerId) 
        self.customerModel = searchForSingleUser(customerId)

        self.conditionList = getAllConditionsByCustomerId(self.customerId)
        print("customerId")
        print(self.customerId)

        print("length of customer conditions")
        print(len(self.conditionList))


        self.customerDetailFrame = customtkinter.CTkFrame(master=self.newWindow, bg_color="transparent")
        self.customerDetailFrame.grid_columnconfigure(0, weight=1)
        self.customerDetailFrame.grid_columnconfigure(1, weight=2)
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


        #For condition
        self.conditionFrame = customtkinter.CTkFrame(master=self.newWindow, bg_color="transparent")
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
        self.ConditionListContainer = customtkinter.CTkFrame(master=self.conditionFrame, bg_color="transparent")
        self.ConditionListContainer.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
        self.ConditionListContainer.grid_columnconfigure(0, weight=1)


        for idx, condition in enumerate(self.conditionList):
            # Create a new condition model block for each condition
            instantiateConditionModelBlock(
                self.ConditionListContainer, condition, 0, idx, self.openConditionDetailsWindowCallback
            )






