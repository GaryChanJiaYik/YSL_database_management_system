import customtkinter
import json
from Constant.appConstant import (
    STANDARD_WINDOW_SIZE, STANDARD_TEXT_BOX_WIDTH, TREATMENT_DESCRIPTION_CHARACTER_LIMIT,
    WINDOW_CONDITION_DETAIL, WINDOW_CUSTOMER_DETAIL, FONT
)
import datetime
import Constant.dbColumn as dbCol
from Constant.converterFunctions import formatDateTime, getFormattedDateTime
import Constant.treatmentDatabaseFunctions as TreatmentFunc
from Model.treatmentModel import TreatmentModel
from datetime import datetime
from Components.popupModal import renderPopUpModal
from Constant.inputValidations import checkLengthOfInput
from Components.datePickerModal import DatePickerModal
from Components.timePickerModal import TimePickerModal
from Components.timeSpinBoxPickerModal import TimeSpinBoxPickerModal 
from Components.datetimePickerModal import DateTimePickerModal
from utils import setEntryValue

class AddTreatmentViewRevamp(customtkinter.CTkFrame):

    beforeLevelField = [ dbCol.treatmentPainLevel, dbCol.treatmentNumbLevel, dbCol.treatmentSoreLevel, dbCol.treatmentTenseLevel ]
    afterLevelField = [ dbCol.treatmentPainLevelAfter, dbCol.treatmentNumbLevelAfter, dbCol.treatmentSoreLevelAfter, dbCol.treatmentTenseLevelAfter]
    entryFieldList = [ dbCol.treatmentDescription ]
    
    def createLabelWithInputfield(self, root, label, entryFields,selectedLevelVar, isSelectBox=False, ):

        frame = customtkinter.CTkFrame(root)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=2)
        customtkinter.CTkLabel(frame, text =label, pady=1).grid(row=0, column=0)
        entry = None

        if isSelectBox: 
            entry = customtkinter.CTkOptionMenu(
                frame,
                variable=selectedLevelVar,
                values=self.optionLevel)
        else:  
            if label is dbCol.treatmentDescription:
                entry = customtkinter.CTkTextbox(frame)  
            else:
                entry = customtkinter.CTkTextbox(frame)
        customtkinter.CTkLabel(frame, text="", width=30).grid(row=0, column=1)

        entry.grid(row=0, column=2, sticky='w')
        if entryFields.get(label) is None:
            entryFields[label] = entry

        return frame

    def createTreatment(self, conditionId, entryFields, saveMode=False):
        # Get combined datetime value
        datetime_str = self.datetime_value.get().strip()  # e.g., "2025-10-17 11:24 PM"

        try:
            combined_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M %p")
            final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")  # for storage
        except ValueError:
            combined_datetime = datetime.now()
            final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        appointment_datetime_str = ''
        try:
            appointment_datetime_raw = self.appointment_datetime_value.get().strip()
            combined_appointment_dt = datetime.strptime(appointment_datetime_raw, "%Y-%m-%d %I:%M %p")
            appointment_datetime_str = combined_appointment_dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            # Fallback or empty if not provided or parse error
            appointment_datetime_str = ''
        
        payment_data = {}
        for method, var in self.payment_vars.items():
            if var.get():  # Checkbox selected
                fee_text = self.payment_entries[method].get().strip()
                if fee_text:
                    try:
                        payment_data[method] = float(f"{float(fee_text):.2f}")
                    except ValueError:
                        continue  # Skip invalid input

                if method == "Others" and method in self.payment_other_desc_entries:
                    desc = self.payment_other_desc_entries[method].get().strip()
                    if desc:
                        # Replace the "Others" key with actual description
                        payment_data[desc] = payment_data.pop("Others", 0.0)

        # Fallback to "0.00" if no payment data is entered
        if payment_data:
            formatted_cost = json.dumps(payment_data)
        else:
            formatted_cost = "0.00"

        params = {
            "pConditionId": conditionId,
            "pTreatmentDescription": entryFields[dbCol.treatmentDescription].get("1.0", customtkinter.END).strip(),
            "pNumbLevel": self.selected_levels[dbCol.treatmentNumbLevel].get(),
            "pPainLevel": self.selected_levels[dbCol.treatmentPainLevel].get(),
            "pSoreLevel": self.selected_levels[dbCol.treatmentSoreLevel].get(),
            "pTenseLevel": self.selected_levels[dbCol.treatmentTenseLevel].get(),
            "pNumbLevelAfter": self.selected_levels[dbCol.treatmentNumbLevelAfter].get(),
            "pPainLevelAfter": self.selected_levels[dbCol.treatmentPainLevelAfter].get(),
            "pSoreLevelAfter": self.selected_levels[dbCol.treatmentSoreLevelAfter].get(),
            "pTenseLevelAfter": self.selected_levels[dbCol.treatmentTenseLevelAfter].get(),
            "pTreatmentDate": final_time_string,
            "pAppointmentDate": appointment_datetime_str,
            "pTreatmentCost": formatted_cost
        }

        if saveMode:
            params["pTreatmentId"] = self.treatmentModel.treatmentID
            params["pAmendmentDate"] = getFormattedDateTime(dateOnly=True)

        treatment = TreatmentModel(**params)

        if saveMode:
            res = TreatmentFunc.updateTreatmentByID(treatment)
            print("\nres:", res, "\nSaved Changes\n")
        else:
            TreatmentFunc.createTreatment(treatment)

        print("Create treatment button pressed")
        renderPopUpModal(self.parent, "Treatment added successfully","Successful", "Success")
        #self.newWindow.destroy()
        #Go back previous window
        self.backToPreviousWindow()
    
    
    def backToPreviousWindow(self):
        print("back to previous window")
        self.controller.setCustomerID(self.conditionModel.customerId)
        self.controller.setConditionModel(self.conditionModel)

        # Clean up the current frame from stack
        if len(self.controller.window_stack) > 0:
            self.controller.window_stack.pop()

        if self.previouWindow == WINDOW_CUSTOMER_DETAIL:
            self.controller.switch_frame(WINDOW_CUSTOMER_DETAIL, isFromBackButton=True)
        else:
            self.controller.switch_frame(WINDOW_CONDITION_DETAIL, isFromBackButton=True)
    
    def on_text_change(self, event=None):
        current_text = self.entryFields[dbCol.treatmentDescription].get("1.0", "end-1c")
        if not checkLengthOfInput(current_text, 0, TREATMENT_DESCRIPTION_CHARACTER_LIMIT):
            # Truncate extra characters
            self.entryFields[dbCol.treatmentDescription].delete("1.0", "end")
            self.entryFields[dbCol.treatmentDescription].insert("1.0", current_text[:TREATMENT_DESCRIPTION_CHARACTER_LIMIT])
            self.desc_warning_label.configure(text=f"Maximum {TREATMENT_DESCRIPTION_CHARACTER_LIMIT} characters reached!", text_color="red")
        else:

            self.desc_warning_label.configure(text=f"{len(current_text)}/{TREATMENT_DESCRIPTION_CHARACTER_LIMIT}", text_color="green")

    
    def populateTimeFields(self, treatmentDate=None, appointmentDate=None):
        if treatmentDate:
            try:
                dt = datetime.strptime(treatmentDate, "%Y-%m-%d %H:%M:%S")
                self.datetime_value.configure(state="normal")
                self.datetime_value.delete(0, "end")
                self.datetime_value.insert(0, dt.strftime("%Y-%m-%d %I:%M %p"))
                self.datetime_value.configure(state="disabled")
            except ValueError as e:
                print("[ERROR] Failed to parse treatment date:", e)

        if appointmentDate:
            try:
                appt_dt = datetime.strptime(appointmentDate, "%Y-%m-%d %H:%M:%S")
                self.appointment_datetime_value.configure(state="normal")
                self.appointment_datetime_value.delete(0, "end")
                self.appointment_datetime_value.insert(0, appt_dt.strftime("%Y-%m-%d %I:%M %p"))
                self.appointment_datetime_value.configure(state="disabled")
            except ValueError as e:
                print("[WARNING] Failed to parse appointment datetime:", e)


    def populate_payment_fields(self):
        try:
            cost_value = self.treatmentCost

            # Case 1: If it's a JSON string, try to parse
            if isinstance(cost_value, str) and cost_value.strip().startswith("{"):
                try:
                    cost_data = json.loads(cost_value)
                except json.JSONDecodeError:
                    cost_data = None
            else:
                cost_data = None

            # Case 2: If it's a valid dictionary (parsed from JSON)
            if isinstance(cost_data, dict):
                for method, amount in cost_data.items():
                    if method == "OthersDesc":
                        if "Others" in self.payment_other_desc_entries:
                            self.payment_other_desc_entries["Others"].grid()
                            self.payment_other_desc_entries["Others"].insert(0, str(amount))
                    elif method in self.payment_vars:
                        self.payment_vars[method].set(True)
                        self.payment_entries[method].grid()
                        self.payment_entries[method].insert(0, str(amount))

            # Case 3: Not a JSON dict — assume it's a plain amount (Cash)
            else:
                amount = float(cost_value)
                self.payment_vars["Cash"].set(True)
                self.payment_entries["Cash"].grid()
                self.payment_entries["Cash"].insert(0, f"{amount:.2f}")

        except Exception as e:
            print("[ERROR] Failed to populate payment fields:", e)

         
    def deleteRecord(self):
        TreatmentFunc.deleteTreatmentByID(self.treatmentModel.treatmentID)
        renderPopUpModal(self.parent, "Treatment removed successfully","Successful", "Success")
        #Go back previous window
        self.backToPreviousWindow()
        
    def validate_numeric_input(self, entry_widget):
        value = entry_widget.get()

        # Check if the input is a valid number (allowing only 1 dot)
        if not value.replace('.', '', 1).isdigit():
            # Remove invalid characters
            cleaned = ''.join([c for c in value if c.isdigit() or c == '.'])
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, cleaned)

            # Show warning
            self.cost_warning_label.configure(text="Only numbers allowed")
        else:
            # Clear warning if input is valid
            self.cost_warning_label.configure(text="")


    def openDatePicker(self):
        DatePickerModal.open_date_picker(
            parent=self,
            current_date_str=self.date_value.get(),
            on_selected=lambda date_str: setEntryValue(self.date_value, date_str)
        )

    
    def openTimePicker(self):
        TimeSpinBoxPickerModal.open_time_picker(
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
    
    def toggle_payment_fields(self, method):
        if self.payment_vars[method].get():
            # Show fee entry
            self.payment_entries[method].grid()
            
            # If field is empty, reset placeholder
            if self.payment_entries[method].get().strip() == "":
                self.payment_entries[method].configure(placeholder_text="Fee")

            # Handle 'Others' description
            if method == "Others" and method in self.payment_other_desc_entries:
                self.payment_other_desc_entries[method].grid()
                if self.payment_other_desc_entries[method].get().strip() == "":
                    self.payment_other_desc_entries[method].configure(placeholder_text="Please specify")

        else:
            # Hide fee entry and clear value
            self.payment_entries[method].delete(0, 'end')
            self.payment_entries[method].grid_remove()

            # Hide and clear 'Others' description
            if method == "Others" and method in self.payment_other_desc_entries:
                self.payment_other_desc_entries[method].delete(0, 'end')
                self.payment_other_desc_entries[method].grid_remove()


    
    def update_payment_fields(self):
        for method, var in self.payment_vars.items():
            entry = self.payment_entries[method]
            if var.get():
                entry.configure(state="normal")
                if method == "Others" and self.payment_other_desc:
                    self.payment_other_desc.configure(state="normal")
            else:
                entry.delete(0, "end")
                entry.configure(state="disabled")
                if method == "Others" and self.payment_other_desc:
                    self.payment_other_desc.delete(0, "end")
                    self.payment_other_desc.configure(state="disabled")


    def __init__(self, parent, controller, conditionID, conditionModel, isEditMode=False, previousWindow=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.conditionModel = conditionModel
        self.previouWindow = previousWindow
    
        self.entryFields = {} #Store the label name(variables) corresponding to the entry fields

        # initialize data
        self.optionLevel = ['1', '2', '3','4', '5', '6', '7', '8','9','10']        

        self.selected_levels = {
            dbCol.treatmentPainLevel:customtkinter.StringVar(value='0'), 
            dbCol.treatmentNumbLevel:customtkinter.StringVar(value='0'),
            dbCol.treatmentSoreLevel:customtkinter.StringVar(value='0'),
            dbCol.treatmentTenseLevel:customtkinter.StringVar(value='0'),
            dbCol.treatmentPainLevelAfter:customtkinter.StringVar(value='0'),
            dbCol.treatmentNumbLevelAfter:customtkinter.StringVar(value='0'),
            dbCol.treatmentSoreLevelAfter:customtkinter.StringVar(value='0'),
            dbCol.treatmentTenseLevelAfter:customtkinter.StringVar(value='0')
            }
       
       # Payment Type and Treatment Fees
        self.payment_methods = ["Cash", "TnG/QR", "Merchant", "Transfer", "Others"]
        self.payment_vars = {}
        self.payment_entries = {}
        self.payment_other_desc_entries = {}

        #Get data and prepopulate fields if is in edit mode
        if isEditMode:
            print("-------------------: ")
            print("IS IN EDIT MODE NOW")
            print("")
            print("self.controller.getTreatmentID(): ", self.controller.getTreatmentID())
            if self.controller.getTreatmentID() is not None:
                #Get the treatment data model
                self.treatmentModel = TreatmentFunc.getTreatmentByID(treatmentID=self.controller.getTreatmentID())
               
                print("Treatment model: ", self.treatmentModel)
                self.selected_levels = {
                    dbCol.treatmentPainLevel:customtkinter.StringVar(value=self.treatmentModel.painLevel), 
                    dbCol.treatmentNumbLevel:customtkinter.StringVar(value=self.treatmentModel.numbLevel),
                    dbCol.treatmentSoreLevel:customtkinter.StringVar(value=self.treatmentModel.soreLevel),
                    dbCol.treatmentTenseLevel:customtkinter.StringVar(value=self.treatmentModel.tenseLevel),
                    dbCol.treatmentPainLevelAfter:customtkinter.StringVar(value=self.treatmentModel.painLevelAfter),
                    dbCol.treatmentNumbLevelAfter:customtkinter.StringVar(value=self.treatmentModel.numbLevelAfter),
                    dbCol.treatmentSoreLevelAfter:customtkinter.StringVar(value=self.treatmentModel.soreLevelAfter),
                    dbCol.treatmentTenseLevelAfter:customtkinter.StringVar(value=self.treatmentModel.tenseLevelAfter)
                }

                self.treatmentDescription = self.treatmentModel.treatmentDescription
                self.treatmentCost = self.treatmentModel.treatmentCost
                
                print("treatment id: ", self.treatmentModel.treatmentID)
                print("condition id: ", self.treatmentModel.conditionID)
                print("condition id param, ", conditionID)
                print("")
                print("")

        self.entryGridFrame = customtkinter.CTkFrame(self, width=500, fg_color="transparent", bg_color="transparent")
        self.entryGridFrame.grid_columnconfigure(0, weight=2)
        self.entryGridFrame.grid_columnconfigure(1, weight=1)
        self.entryGridFrame.grid_columnconfigure(2, weight=2)
        self.entryGridFrame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        index = 1

        for idx, field in enumerate(self.entryFieldList):
            #render text
            customtkinter.CTkLabel(self.entryGridFrame, text =dbCol.TreatmentModelAttributeToField[field], font=FONT["LABEL"], pady=1).grid(row=idx+1, column=0, sticky='nw', pady=10)
            customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(row=idx+1, column=1, sticky='nw')
            
            # entry = None
            
            #render entry
            if field is dbCol.treatmentDescription:
                #create enty text 
                treatmentDescFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
                treatmentDescFrame.grid(row=idx+1, column=2, sticky='w')

                entry = customtkinter.CTkTextbox(treatmentDescFrame, width=STANDARD_TEXT_BOX_WIDTH)
                entry.insert("0.0", self.treatmentDescription if isEditMode else "")
                entry.bind("<KeyRelease>", self.on_text_change)
                entry.bind("<<Paste>>", lambda e: self.after(1, self.on_text_change))
                
                entry.grid(row=0, column=0, sticky='w')

                self.desc_warning_label = customtkinter.CTkLabel(treatmentDescFrame, text="", text_color="red")
                self.desc_warning_label.grid(row=1, column=0, sticky='e')

                #self.createLabelWithInputfield(self.newWindow, field, self.entryFields, None, False).grid(row=idx+1, column=0, sticky='w')
            
            if self.entryFields.get(field) is None:
                self.entryFields[field] = entry
            
            index+=1

        # Payment Methods Section
        customtkinter.CTkLabel(self.entryGridFrame, text="Payment Methods", font=FONT["LABEL"]).grid(
            row=index, column=0, sticky='w', pady=(10, 5)
        )
        index += 1

        payment_frame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent")
        payment_frame.grid(row=index, column=2, sticky='w')

        for i, method in enumerate(self.payment_methods):
            var = customtkinter.BooleanVar()
            self.payment_vars[method] = var

            row_frame = customtkinter.CTkFrame(payment_frame, fg_color="transparent")
            row_frame.grid(row=i, column=0, sticky='w', pady=5)

            # Checkbox
            cb = customtkinter.CTkCheckBox(
                row_frame, text=method, variable=var,
                command=lambda m=method: self.toggle_payment_fields(m)
            )
            cb.grid(row=0, column=0, sticky='w')

            # Fee Entry (initially hidden)
            fee_entry = customtkinter.CTkEntry(row_frame, width=80, placeholder_text="Fee")
            fee_entry.grid(row=0, column=1, padx=10)
            fee_entry.grid_remove()
            self.payment_entries[method] = fee_entry

            # Special handling for "Others"
            if method == "Others":
                other_entry = customtkinter.CTkEntry(row_frame, width=100, placeholder_text="Please specify")
                other_entry.grid(row=0, column=2, padx=10)
                other_entry.grid_remove()
                self.payment_other_desc_entries[method] = other_entry

        index += 1  # for next form section

        if isEditMode:
            self.populate_payment_fields()
        
        # Before Treatment Levels
        customtkinter.CTkLabel(self.entryGridFrame, text="Before Treatment Levels", font=('Arial', 12, 'bold')).grid(
            row=index, column=0, sticky='w', pady=(20, 5)
        )
        index += 1

        for field in self.beforeLevelField:
            customtkinter.CTkLabel(self.entryGridFrame, text=dbCol.TreatmentModelAttributeToField[field]).grid(
                row=index, column=0, sticky='w'
            )
            entry = customtkinter.CTkOptionMenu(
                self.entryGridFrame,
                variable=self.selected_levels[field],
                values=self.optionLevel
            )
            entry.grid(row=index, column=2, sticky='w', pady=(0, 5))
            self.entryFields[field] = entry
            index += 1

        # After Treatment Levels
        customtkinter.CTkLabel(self.entryGridFrame, text="After Treatment Levels", font=('Arial', 12, 'bold')).grid(
            row=index, column=0, sticky='w', pady=(25, 5)
        )
        index += 1

        for field in self.afterLevelField:
            customtkinter.CTkLabel(self.entryGridFrame, text=dbCol.TreatmentModelAttributeToField[field]).grid(
                row=index, column=0, sticky='w'
            )
            entry = customtkinter.CTkOptionMenu(
                self.entryGridFrame,
                variable=self.selected_levels[field],
                values=self.optionLevel
            )
            entry.grid(row=index, column=2, sticky='w', pady=(0, 5))
            self.entryFields[field] = entry
            index += 1
        
        # ======================== Date-Time Section ========================
        index += 1

        # === Combined DateTime Row ===
        customtkinter.CTkLabel(self.entryGridFrame, text="Treatment Date Time:", font=FONT["LABEL"], pady=1).grid(
            row=index, column=0, sticky="w", pady=(30, 10)
        )
        customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(
            row=index, column=1
        )
        datetimeInputFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent")
        datetimeInputFrame.grid(row=index, column=2, sticky="w")

        self.datetime_value = customtkinter.CTkEntry(datetimeInputFrame, width=180)
        self.datetime_value.insert(0, datetime.now().strftime("%Y-%m-%d %I:%M %p"))
        self.datetime_value.configure(state="disabled")
        self.datetime_value.grid(row=0, column=0, padx=(0, 10))

        self.datetime_edit_button = customtkinter.CTkButton(
            datetimeInputFrame, text="Modify", width=60, command=self.openDateTimePicker
        )
        self.datetime_edit_button.grid(row=0, column=1)

        index += 1  # move to next row

        # === Appointment Date Time Row ===
        customtkinter.CTkLabel(self.entryGridFrame, text="Appointment Date Time:", font=FONT["LABEL"], pady=1).grid(
            row=index, column=0, sticky="w", pady=(20, 10)
        )
        customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(
            row=index, column=1
        )
        appointmentInputFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent")
        appointmentInputFrame.grid(row=index, column=2, sticky="w")

        self.appointment_datetime_value = customtkinter.CTkEntry(appointmentInputFrame, width=180)
        self.appointment_datetime_value.insert(0, datetime.now().strftime("%Y-%m-%d %I:%M %p"))
        self.appointment_datetime_value.configure(state="disabled")
        self.appointment_datetime_value.grid(row=0, column=0, padx=(0, 10))

        self.appointment_datetime_edit_button = customtkinter.CTkButton(
            appointmentInputFrame, text="Modify", width=60,
            command=lambda: DateTimePickerModal.open_datetime_picker(
                parent=self,
                current_datetime_str=self.appointment_datetime_value.get().strip(),
                on_selected=lambda datetime_str: setEntryValue(self.appointment_datetime_value, datetime_str)
            )
        )
        self.appointment_datetime_edit_button.grid(row=0, column=1)

        index += 1  # move to the next row for buttons


        # Add frame for buttons
        self.actionButtonsFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
        self.actionButtonsFrame.grid(row=index, column=0)
        self.actionButtonsFrame.grid_columnconfigure(0, weight=1)
        self.actionButtonsFrame.grid_columnconfigure(1, minsize=50)
        self.actionButtonsFrame.grid_columnconfigure(2, weight=1)


        if isEditMode:
            self.populateTimeFields(
                treatmentDate=self.treatmentModel.treatmentDate,
                appointmentDate=self.treatmentModel.appointmentDate
            )

            customtkinter.CTkButton(self.actionButtonsFrame, text="Save", command=lambda: self.createTreatment(conditionID, self.entryFields, saveMode=True)).grid(row=0, column=0, pady=(20, 0))
            customtkinter.CTkButton(self.actionButtonsFrame, text="Delete", fg_color="red", text_color="white", hover_color="darkred", command=lambda: self.deleteRecord()).grid(row=0, column=1, padx=(10,0), pady=(20, 0))
        else:
            customtkinter.CTkButton(self.actionButtonsFrame, text="Add", command=lambda: self.createTreatment(conditionID, self.entryFields)).grid(row=0, column=0, pady=(20, 0))