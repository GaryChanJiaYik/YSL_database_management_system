import customtkinter as ctk
import Constant.dbColumn as dbCol
from datetime import datetime
from Constant.appConstant import STANDARD_TEXT_BOX_WIDTH, STANDARD_TEXT_BOX_HEIGHT, WINDOW_LANDING, WINDOW_CUSTOMER_DETAIL
from Constant.databaseManipulationFunctions import searchForSingleUser, addCustomer, saveCustomerChanges, deleteCustomerById
from Constant.converterFunctions import convertTimeStampToId

class AddCustomerView(ctk.CTkFrame):
        
    def __init__(self, parent, controller, isEditMode=False, customerId=None):
        super().__init__(parent)
        self.controller = controller
        self.isEditMode = isEditMode
        self.customerId = customerId
        
        self.fields = {}
        self.race_vars = {}
        
        self.buildForm()
        
        # Populate fields if editing
        if self.isEditMode and self.customerId is not None:
            self.customerModel = searchForSingleUser(convertTimeStampToId(customerId))
            self.populateFields()
        
        
    def buildForm(self):
        howDidYouFindUsOptions = ["Social Media", "Friend", "Google", "Walk-in", "Other"]
        row = 0

        def addEntry(row, label):
            ctk.CTkLabel(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            entry = ctk.CTkEntry(self, width=300)
            entry.grid(row=row, column=1, columnspan=2, sticky="w", pady=5)
            return entry

        def addLabel(row, label):
            ctk.CTkLabel(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)

        # Fields
        self.fields[dbCol.oldCustomerId] = addEntry(row, dbCol.customerModelAttributeToField['oldCustomerId']); row += 1
        self.fields[dbCol.ic] = addEntry(row, dbCol.customerModelAttributeToField['ic']); row += 1
        self.fields[dbCol.name] = addEntry(row, dbCol.customerModelAttributeToField['customerName']); row += 1
        self.fields[dbCol.email] = addEntry(row, dbCol.customerModelAttributeToField['email']); row += 1

        # Gender (Radio Buttons)
        addLabel(row, dbCol.customerModelAttributeToField['gender'])
        self.gender_var = ctk.StringVar(value="Male")
        ctk.CTkRadioButton(self, text="Male", variable=self.gender_var, value="Male").grid(row=row, column=1, sticky="w")
        ctk.CTkRadioButton(self, text="Female", variable=self.gender_var, value="Female").grid(row=row, column=2, sticky="w")
        row += 1

        # Race (Radio Buttons)
        addLabel(row, dbCol.customerModelAttributeToField['race'])
        self.race_var = ctk.StringVar(value="Chinese")
        race_frame = ctk.CTkFrame(self)
        race_frame.grid(row=row, column=1, columnspan=3, sticky="w")
        # Create race options
        for idx, race_option in enumerate(["Chinese", "Malay", "Indian", "Other"]):
            rb = ctk.CTkRadioButton(
                race_frame, text=race_option, variable=self.race_var, value=race_option,
                command=self.toggleRaceOtherField
            )
            rb.pack(side="left", padx=(0, 10))
        row += 1
        # "Other" field (shown only when 'Other' is selected)
        self.race_other_entry = ctk.CTkEntry(self, placeholder_text="If Other, specify", width=300)
        self.race_other_entry.grid(row=row, column=1, columnspan=2, sticky="w", padx=10, pady=5)
        self.race_other_entry.grid_remove()  # Start hidden
        row += 1

        # Address (Textbox)
        addLabel(row, dbCol.customerModelAttributeToField['address'])
        self.address_text = ctk.CTkTextbox(self, width=STANDARD_TEXT_BOX_WIDTH, height=STANDARD_TEXT_BOX_HEIGHT)
        self.address_text.grid(row=row, column=1, columnspan=3, sticky="we", pady=5)
        row += 1

        self.fields[dbCol.handPhoneNumber] = addEntry(row, dbCol.customerModelAttributeToField['handphone']); row += 1
        self.fields[dbCol.instagram] = addEntry(row, dbCol.customerModelAttributeToField['instagram']); row += 1

        # How Did You Find Us (Dropdown)
        addLabel(row, dbCol.customerModelAttributeToField['howDidYouFindUs'])
        self.how_var = ctk.StringVar()
        self.how_dropdown = ctk.CTkComboBox(self, values=howDidYouFindUsOptions, variable=self.how_var)
        self.how_dropdown.grid(row=row, column=1, columnspan=2, sticky='w', pady=5)
        self.how_dropdown.configure(state="readonly")
        row += 1

        # Consent Section Title
        consent_title = ctk.CTkLabel(self, text="CONSENT FOR TREATMENT", font=ctk.CTkFont(weight="bold"))
        consent_title.grid(row=row, column=0, columnspan=3, sticky="w", pady=(20, 5), padx=10)
        row += 1

        # Consent Text (wrapped label)
        consent_text = (
            "I understand that I can ask any questions pertaining to the therapy before filling this form. "
            "I could, if the need arises, withdraw my consent to stop the therapy at any time throughout the procedure. "
            "The procedure, its risks and benefits have been explained to me, and I understand the explanation given."
        )
        consent_label = ctk.CTkLabel(self, text=consent_text, wraplength=600, justify="left")
        consent_label.grid(row=row, column=0, columnspan=3, sticky="w", padx=10)
        row += 1

        # Consent Checkbox
        self.consent_var = ctk.BooleanVar()
        consent_checkbox = ctk.CTkCheckBox(self, text="I agree to the above consent", variable=self.consent_var)
        consent_checkbox.grid(row=row, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 20))
        row += 1

        # Buttons
        if self.isEditMode:
            ctk.CTkButton(
                self, 
                text="Save", 
                command=self.saveCustomer
            ).grid(row=row, column=0, pady=20, sticky="w")
            ctk.CTkButton(
                self, 
                text="Delete", 
                command=self.deleteCustomer, 
                fg_color="red", 
                text_color="white"
            ).grid(row=row, column=1, pady=20, sticky="w", padx=10)
        else:
            ctk.CTkButton(self, text="Add", command=self.submitForm).grid(row=row, column=0, pady=20, sticky="w")
    
    
    def toggleRaceOtherField(self):
        if self.race_var.get() == "Other":
            self.race_other_entry.grid()
        else:
            self.race_other_entry.grid_remove()
    
    
    def populateFields(self):
        if not hasattr(self, 'customerModel'):
            return

        self.fields[dbCol.oldCustomerId].insert(0, self.customerModel.oldCustomerId or "")
        self.fields[dbCol.ic].insert(0, self.customerModel.ic or "")
        self.fields[dbCol.name].insert(0, self.customerModel.customerName or "")
        self.fields[dbCol.email].insert(0, self.customerModel.email or "")
        self.fields[dbCol.handPhoneNumber].insert(0, self.customerModel.handphone or "")
        self.fields[dbCol.instagram].insert(0, self.customerModel.instagram or "")
        self.address_text.insert("0.0", self.customerModel.address or "")
        
        # Gender
        if self.customerModel.gender.startswith("Male"):
            self.gender_var.set("Male")
        elif self.customerModel.gender.startswith("Female"):
            self.gender_var.set("Female")
        
        # Race
        race_raw = self.customerModel.race or "Chinese"
        standard_races = ["Chinese", "Malay", "Indian"]

        if any(race_raw.startswith(r) for r in standard_races):
            for std_race in standard_races:
                if race_raw.startswith(std_race):
                    self.race_var.set(std_race)
                    break
            self.race_other_entry.grid_remove()  # Hide the "Other" entry
        else:
            # It's a custom race
            self.race_var.set("Other")
            self.race_other_entry.grid()  # Show the entry
            self.race_other_entry.delete(0, "end")
            self.race_other_entry.insert(0, race_raw)
        self.how_var.set(self.customerModel.howDidYouFindUs or "Other")

        if self.customerModel.race == "Other":
            self.race_other_entry.grid()
            self.race_other_entry.insert(0, self.customerModel.raceOther or "")
    
        # Consent
        consent_raw = self.customerModel.consent
        if consent_raw.startswith("Agree"):  # or check "同意" if you prefer
            self.consent_var.set(True)
        else:
            self.consent_var.set(False)
        
    
    def getFormData(self, customer_id=None):
        # Use current timestamp as ID if new
        if not customer_id:
            now = datetime.now()
            customer_id = f"{now.month}/{now.day}/{now.year} {now:%H:%M:%S}"

        consent_given = self.consent_var.get()
        consent_status = "Agree同意" if consent_given else "Disagree不同意"

        email_val = self.fields[dbCol.email].get()
        ic_val = self.fields[dbCol.ic].get()
        name_val = self.fields[dbCol.name].get()
        gender_val = "Male男" if self.gender_var.get() == "Male" else "Female女"
        race_val = self.race_other_entry.get() if self.race_var.get() == "Other" else self.race_var.get()
        address_val = self.address_text.get("1.0", "end").strip()
        hp_val = self.fields[dbCol.handPhoneNumber].get()
        instagram_val = self.fields[dbCol.instagram].get()
        how_val = self.how_var.get()
        old_customer_id_val = self.fields[dbCol.oldCustomerId].get()

        header = [
            dbCol.customerId, "Column 1", dbCol.email, dbCol.ic, dbCol.name, dbCol.gender, dbCol.race, dbCol.address,
            dbCol.handPhoneNumber, dbCol.instagram, dbCol.knowUsMethod, "Email Address", "Score", 
            "CONSENT FOR TREATMENT", "Postcode 邮编", "State州属", "Country国家", "Are you foreigners你是外国人吗", 
            "Passport护照", "Passport护照", dbCol.oldCustomerId
        ]

        row = [
            customer_id, "", email_val, ic_val, name_val, gender_val, race_val, address_val, hp_val, instagram_val,
            how_val, "", "", consent_status, "", "", "", "", "", "", old_customer_id_val
        ]

        return header, row, customer_id
    
    def submitForm(self):
        header, row, customer_id = self.getFormData()
        
        addCustomer(lambda: (header, row, customer_id))
        self.controller.setCustomerID(customer_id)
        
        if len(self.controller.window_stack) > 0:
            self.controller.window_stack.pop()

        self.controller.switch_frame(WINDOW_CUSTOMER_DETAIL, isFromBackButton=False)
    
    def saveCustomer(self):
        saveCustomerChanges(self.getFormData, self.customerModel.customerId)
        self.backToPreviousWindow()
    
    def deleteCustomer(self):
        # from tkinter import messagebox
        # confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?")
        # if not confirm:
        #     return
        deleteCustomerById(self.customerModel.customerId)
        self.backToPreviousWindow()
        
    
    def backToPreviousWindow(self):
        # Clean up the current frame from stack
        if len(self.controller.window_stack) > 0:
            self.controller.window_stack.pop()

        self.controller.switch_frame(WINDOW_LANDING, isFromBackButton=True)