import customtkinter as ctk
import os
import csv
import Constant.dbColumn as dbCol
from datetime import datetime
from Constant.appConstant import STANDARD_TEXT_BOX_WIDTH, STANDARD_TEXT_BOX_HEIGHT, WINDOW_LANDING

DB_PATH = './data/db.csv'

class AddCustomerView(ctk.CTkFrame):
        
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.fields = {}
        self.race_vars = {}
        
        self.build_form()
        
        
    def build_form(self):
        howDidYouFindUsOptions = ["Social Media", "Friend", "Google", "Walk-in", "Other"]
        row = 0

        def add_entry(row, label):
            ctk.CTkLabel(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            entry = ctk.CTkEntry(self, width=300)
            entry.grid(row=row, column=1, columnspan=2, sticky="w", pady=5)
            return entry

        def add_label(row, label):
            ctk.CTkLabel(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)

        # Fields
        self.fields[dbCol.oldCustomerId] = add_entry(row, dbCol.customerModelAttributeToField['oldCustomerId']); row += 1
        self.fields[dbCol.ic] = add_entry(row, dbCol.customerModelAttributeToField['ic']); row += 1
        self.fields[dbCol.name] = add_entry(row, dbCol.customerModelAttributeToField['customerName']); row += 1
        self.fields[dbCol.email] = add_entry(row, dbCol.customerModelAttributeToField['email']); row += 1

        # Gender (Radio Buttons)
        add_label(row, dbCol.customerModelAttributeToField['gender'])
        self.gender_var = ctk.StringVar(value="Male")
        ctk.CTkRadioButton(self, text="Male", variable=self.gender_var, value="Male").grid(row=row, column=1, sticky="w")
        ctk.CTkRadioButton(self, text="Female", variable=self.gender_var, value="Female").grid(row=row, column=2, sticky="w")
        row += 1

        # Race (Radio Buttons)
        add_label(row, dbCol.customerModelAttributeToField['race'])
        self.race_var = ctk.StringVar(value="Chinese")
        race_frame = ctk.CTkFrame(self)
        race_frame.grid(row=row, column=1, columnspan=3, sticky="w")
        # Create race options
        for idx, race_option in enumerate(["Chinese", "Malay", "Indian", "Other"]):
            rb = ctk.CTkRadioButton(
                race_frame, text=race_option, variable=self.race_var, value=race_option,
                command=self.toggle_race_other_field
            )
            rb.pack(side="left", padx=(0, 10))
        row += 1
        # "Other" field (shown only when 'Other' is selected)
        self.race_other_entry = ctk.CTkEntry(self, placeholder_text="If Other, specify", width=300)
        self.race_other_entry.grid(row=row, column=1, columnspan=2, sticky="w", padx=10, pady=5)
        self.race_other_entry.grid_remove()  # Start hidden
        row += 1

        # Address (Textbox)
        add_label(row, dbCol.customerModelAttributeToField['address'])
        self.address_text = ctk.CTkTextbox(self, width=STANDARD_TEXT_BOX_WIDTH, height=STANDARD_TEXT_BOX_HEIGHT)
        self.address_text.grid(row=row, column=1, columnspan=3, sticky="we", pady=5)
        row += 1

        self.fields[dbCol.handPhoneNumber] = add_entry(row, dbCol.customerModelAttributeToField['handphone']); row += 1
        self.fields[dbCol.instagram] = add_entry(row, dbCol.customerModelAttributeToField['instagram']); row += 1

        # How Did You Find Us (Dropdown)
        add_label(row, dbCol.customerModelAttributeToField['howDidYouFindUs'])
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
        submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit_form)
        submit_btn.grid(row=row, column=0, pady=20, sticky="w")
    
    
    def toggle_race_other_field(self):
        if self.race_var.get() == "Other":
            self.race_other_entry.grid()
        else:
            self.race_other_entry.grid_remove()
        
     
    def submit_form(self):
        # Generate timestamp for Customer ID
        timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        customer_id = timestamp

        # Consent handling
        consent_given = self.consent_var.get()
        consent_status = "Agree同意" if consent_given else "Disagree不同意"

        consent_text = (
            "I understand that I can ask any questions pertaining to the therapy before filling this form. "
            "I could, if the need arises, withdraw my consent to stop the therapy at any time throughout the procedure. "
            "The procedure, its risks and benefits have been explained to me, and I understand the explanation given.\n"
            "I hereby agree for the therapy to be carried out on me. I also understand that a record of the therapy given shall be kept. "
            "This record is confidential and will not be disclosed to an outside party, unless it has been authorised by me, "
            "or my representative, or as ordered by the court of law to do so.\n\n"
            "治疗同意书\n"
            "我明白在填写本表格之前，我可以提出任何疑问相关治疗的问题。如果有需要，我可以在治疗过程中随时撤回我的同意并终止治疗。"
            "治疗的程序、风险和益处已向我解释，我已理解所提供的说明。\n"
            "因此，我同意接受治疗。我也明白，治疗记录将被保存，该记录是保密的，除非得到我的授权、我的代表的授权，或根据法院的命令，否则不会透露给外部人士。"
        ) if consent_given else ""

        # Collect form values
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

        # Define header manually to match column order
        header = [
            dbCol.customerId,               # Timestamp
            "Column 1",                     # Consent Agree/Disagree
            dbCol.email,                   # Email电邮
            dbCol.ic,                      # IC身份证
            dbCol.name,                    # Name名
            dbCol.gender,                  # Gender性别
            dbCol.race,                    # Race种族
            dbCol.address,                 # Address地址
            dbCol.handPhoneNumber,         # HP No.手机号
            dbCol.instagram,               # Instagram
            dbCol.knowUsMethod,            # How did get know our centre?
            "Email Address",               # Repeated email
            "Score",                       # Blank
            "CONSENT FOR TREATMENT",       # Full consent text
            "Postcode 邮编",                # blank
            "State州属",
            "Country国家",
            "Are you foreigners你是外国人吗",
            "Passport护照",
            "Passport护照",
            dbCol.oldCustomerId
        ]

        # Match data to header order
        row = [
            customer_id,
            "",
            email_val,
            ic_val,
            name_val,
            gender_val,
            race_val,
            address_val,
            hp_val,
            instagram_val,
            how_val,
            "",
            "",
            consent_status,
            "",
            "",
            "",
            "",
            "",
            "",
            old_customer_id_val
        ]

        file_exists = os.path.exists(DB_PATH)

        try:
            with open(DB_PATH, mode='a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(header)
                writer.writerow(row)
            print(f"Customer record saved successfully: {customer_id}")
        except Exception as e:
            print(f"Error saving customer record: {e}")
            
        self.backToPreviousWindow()
    
    
    def backToPreviousWindow(self):
        # Clean up the current frame from stack
        if len(self.controller.window_stack) > 0:
            self.controller.window_stack.pop()

        self.controller.switch_frame(WINDOW_LANDING, isFromBackButton=True)