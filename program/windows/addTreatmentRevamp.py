import customtkinter
from Constant.appConstant import STANDARD_WINDOW_SIZE, STANDARD_TEXT_BOX_WIDTH, TREATMENT_DESCRIPTION_CHARACTER_LIMIT,WINDOW_CONDITION_DETAIL
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
from utils import set_entry_value  # adjust the path if needed

class AddTreatmentViewRevamp(customtkinter.CTkFrame):

    entryFieldList = [ dbCol.treatmentDescription, dbCol.treatmentCost, dbCol.treatmentPainLevel, dbCol.treatmentNumbLevel, dbCol.treatmentSoreLevel, dbCol.treatmentTenseLevel]
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
        # Get date and time from pickers
        date_str = self.date_value.get()
        time_str = self.time_value.get()

        try:
            # Parse time (12-hour format with AM/PM)
            dt_time = datetime.strptime(time_str, "%I:%M %p").time()

            # Parse date and combine with time
            combined_datetime = datetime.strptime(date_str, "%Y-%m-%d").replace(
                hour=dt_time.hour, minute=dt_time.minute, second=0
            )

            final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # fallback to current datetime if parsing fails
            combined_datetime = datetime.now()
            final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
        raw_cost = entryFields[dbCol.treatmentCost].get().strip() or "0"
        try:
            formatted_cost = float(f"{float(raw_cost):.2f}")  # Ensures 2 decimal places
        except ValueError:
            formatted_cost = 0.00  # fallback

        params = {
            "pConditionId": conditionId,
            "pTreatmentDescription": entryFields[dbCol.treatmentDescription].get("1.0", customtkinter.END).strip(),
            "pNumbLevel": self.selected_levels[dbCol.treatmentNumbLevel].get(),
            "pPainLevel": self.selected_levels[dbCol.treatmentPainLevel].get(),
            "pSoreLevel": self.selected_levels[dbCol.treatmentSoreLevel].get(),
            "pTenseLevel": self.selected_levels[dbCol.treatmentTenseLevel].get(),
            "pTreatmentDate": final_time_string,
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
        renderPopUpModal(self, "Treatment added successfully","Successful", "Success")
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

    def populateTimeFields(self, datetime_string):
        try:
            # Parse the datetime string into a datetime object
            dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

            # Format date and time
            formatted_date = dt.strftime("%Y-%m-%d")
            formatted_time = dt.strftime("%I:%M %p")  # 12-hour format with AM/PM

            # Update the date entry
            self.date_value.configure(state="normal")
            self.date_value.delete(0, "end")
            self.date_value.insert(0, formatted_date)
            self.date_value.configure(state="disabled")

            # Update the time entry
            self.time_value.configure(state="normal")
            self.time_value.delete(0, "end")
            self.time_value.insert(0, formatted_time)
            self.time_value.configure(state="disabled")

        except ValueError:
            print("Invalid datetime format. Expected: 'YYYY-MM-DD HH:MM:SS'")
            
    def deleteRecord(self):
        TreatmentFunc.deleteTreatmentByID(self.treatmentModel.treatmentID)
        renderPopUpModal(self, "Treatment removed successfully","Successful", "Success")
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
            on_selected=lambda date_str: set_entry_value(self.date_value, date_str)
        )

    
    def openTimePicker(self):
        TimePickerModal.open_time_picker(
            parent=self,
            current_time_str=self.time_value.get().strip(),
            on_selected=lambda time_str: set_entry_value(self.time_value, time_str)
        )


    def __init__(self, parent, controller, conditionID, conditionModel, isEditMode=False):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.conditionModel = conditionModel
    
        self.entryFields = {} #Store the label name(variables) corresponding to the entry field
         
        #customtkinter.CTkLabel(self.newWindow, text=f'Add Treatment' , font=('Arial',12)).grid(column=0, row=0, sticky='w')

        # initialize data
        self.optionLevel = ['1', '2', '3','4', '5', '6', '7', '8','9','10']        

        self.selected_levels = {
            dbCol.treatmentPainLevel:customtkinter.StringVar(value='0'), 
            dbCol.treatmentNumbLevel:customtkinter.StringVar(value='0'),
            dbCol.treatmentSoreLevel:customtkinter.StringVar(value='0'),
            dbCol.treatmentTenseLevel:customtkinter.StringVar(value='0')
            }
        #self.selected_level = customtkinter.StringVar(value=self.optionLevel[0])

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
                    dbCol.treatmentTenseLevel:customtkinter.StringVar(value=self.treatmentModel.tenseLevel)
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
            customtkinter.CTkLabel(self.entryGridFrame, text =dbCol.TreatmentModelAttributeToField[field], pady=1).grid(row=idx+1, column=0, sticky='nw', pady=10)
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
            elif field is dbCol.treatmentCost:
                treatmentCostContainer = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
                treatmentCostContainer.grid(row=idx+1, column=2, sticky='w')

                entry = customtkinter.CTkEntry(treatmentCostContainer, width=100)
                entry.grid(row=0, column=1, sticky="w")
                if isEditMode:
                    cost = float(self.treatmentCost)
                    cost_str = str(int(cost)) if cost.is_integer() else f"{cost:.2f}"
                    entry.insert(0, cost_str)
                else:
                    entry.insert(0, "")
                entry.bind("<KeyRelease>", lambda e: self.validate_numeric_input(entry))
                
                entry.grid(row=0, column=0, sticky='w')

                self.cost_warning_label = customtkinter.CTkLabel(treatmentCostContainer, text="", text_color="red")
                self.cost_warning_label.grid(row=1, column=0, sticky='e')
            else:
                #create select box
                entry = customtkinter.CTkOptionMenu(
                    self.entryGridFrame,
                    variable=self.selected_levels[field],
                    values=self.optionLevel)
                entry.grid(row=idx+1, column=2, sticky='w')

                #self.createLabelWithInputfield(self.newWindow, field, self.entryFields,self.selected_levels[field], isSelectBox=True,).grid(row=idx+1, column=0, sticky='w')
            
            if self.entryFields.get(field) is None:
                self.entryFields[field] = entry
            
            index+=1

        # ======================== Date-Time Section ========================
        date_time_row = index + 1

        # === Date Row ===
        customtkinter.CTkLabel(self.entryGridFrame, text="Date:", pady=1).grid(
            row=date_time_row, column=0, sticky="w", pady=10
        )
        customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(
            row=date_time_row, column=1
        )

        dateInputFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent")
        dateInputFrame.grid(row=date_time_row, column=2, sticky="w")

        self.date_value = customtkinter.CTkEntry(dateInputFrame, width=120)
        self.date_value.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_value.configure(state="disabled")
        self.date_value.grid(row=0, column=0, padx=(0, 10))

        self.date_edit_button = customtkinter.CTkButton(dateInputFrame, text="Edit", width=60, command=self.openDatePicker)
        self.date_edit_button.grid(row=0, column=1)

        # === Time Row ===
        customtkinter.CTkLabel(self.entryGridFrame, text="Time:", pady=1).grid(
            row=date_time_row + 1, column=0, sticky="w", pady=10
        )
        customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(
            row=date_time_row + 1, column=1
        )

        timeInputFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent")
        timeInputFrame.grid(row=date_time_row + 1, column=2, sticky="w")

        self.time_value = customtkinter.CTkEntry(timeInputFrame, width=120)
        self.time_value.insert(0, datetime.now().strftime("%I:%M %p"))  # 12-hour format
        self.time_value.configure(state="disabled")
        self.time_value.grid(row=0, column=0, padx=(0, 10))

        self.time_edit_button = customtkinter.CTkButton(timeInputFrame, text="Edit", width=60, command=self.openTimePicker)
        self.time_edit_button.grid(row=0, column=1)


        # Add frame for buttons
        self.actionButtonsFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
        self.actionButtonsFrame.grid(row=index+3, column=0)
        self.actionButtonsFrame.grid_columnconfigure(0, weight=1)
        self.actionButtonsFrame.grid_columnconfigure(1, minsize=50)
        self.actionButtonsFrame.grid_columnconfigure(2, weight=1)


        if isEditMode:
            self.populateTimeFields(self.treatmentModel.treatmentDate)

            customtkinter.CTkButton(self.actionButtonsFrame, text="Save", command=lambda: self.createTreatment(conditionID, self.entryFields, saveMode=True)).grid(row=0, column=0, pady=(20, 0))
            customtkinter.CTkButton(self.actionButtonsFrame, text="Delete", fg_color="red", text_color="white", hover_color="darkred", command=lambda: self.deleteRecord()).grid(row=0, column=1, padx=(10,0), pady=(20, 0))
        else:
            customtkinter.CTkButton(self.actionButtonsFrame, text="Add", command=lambda: self.createTreatment(conditionID, self.entryFields)).grid(row=0, column=0, pady=(20, 0))