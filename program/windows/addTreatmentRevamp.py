import customtkinter
from Constant.appConstant import STANDARD_WINDOW_SIZE, STANDARD_TEXT_BOX_WIDTH, TREATMENT_DESCRIPTION_CHARACTER_LIMIT,WINDOW_CONDITION_DETAIL
import datetime
import Constant.dbColumn as dbCol
from Constant.converterFunctions import formatDateTime, getFormattedDateTime
import Constant.treatmentDatabaseFunctions as TreatmentFunc
from Model.treatmentModel import TreatmentModel
from datetime import datetime
from tkinter import ttk
from Components.popupModal import renderPopUpModal
from Constant.inputValidations import checkLengthOfInput

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
        now = datetime.now()

        if self.auto_time_var.get():
            combined_datetime = now
        else:
            day = self.day_entry.get()
            month = self.month_entry.get()
            year = self.year_entry.get()

            hour = self.hour_entry.get()
            minute = self.minute_entry.get()
            am_pm = self.am_pm_dropdown.get()

            # Convert to 24-hour format
            if am_pm == "PM" and hour != "12":
                hour = str(int(hour) + 12)
            elif am_pm == "AM" and hour == "12":
                hour = "00"
        
            combined_datetime = datetime.strptime(f"{year}-{month}-{day} {hour}:{minute}:00", "%Y-%m-%d %H:%M:%S")
        final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")

        params = {
            "pConditionId": conditionId,
            "pTreatmentDescription": entryFields[dbCol.treatmentDescription].get("1.0", customtkinter.END).strip(),
            "pNumbLevel": self.selected_levels[dbCol.treatmentNumbLevel].get(),
            "pPainLevel": self.selected_levels[dbCol.treatmentPainLevel].get(),
            "pSoreLevel": self.selected_levels[dbCol.treatmentSoreLevel].get(),
            "pTenseLevel": self.selected_levels[dbCol.treatmentTenseLevel].get(),
            "pTreatmentDate": final_time_string,
            "pTreatmentCost": float(entryFields[dbCol.treatmentCost].get().strip() or 0)
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
    
    def toggle_time_fields(self):
        if self.auto_time_var.get():
            self.manualTimeContainer.grid_remove()
        else:
            self.manualTimeContainer.grid()
            self.manualTimeDesc.grid(row=0, column=0, sticky="w", columnspan=3, pady=(0, 5))
            self.hourContainer.grid(row=1, column=0, sticky="w")
            self.minuteContainer.grid(row=1, column=1, sticky="w")
            self.amPmContainer.grid(row=1, column=2, sticky="w")  
            self.dayContainer.grid(row=2, column=0, sticky="w")
            self.monthContainer.grid(row=2, column=1, sticky="w")
            self.yearContainer.grid(row=2, column=2, sticky="w")
    
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
            
            # Convert 24-hour format to 12-hour format
            hour_24 = dt.hour
            minute = dt.minute

            if hour_24 == 0:
                hour_12 = 12
                am_pm = "AM"
            elif hour_24 == 12:
                hour_12 = 12
                am_pm = "PM"
            elif hour_24 > 12:
                hour_12 = hour_24 - 12
                am_pm = "PM"
            else:
                hour_12 = hour_24
                am_pm = "AM"

            # Populate the fields
            self.hour_entry.delete(0, "end")
            self.hour_entry.insert(0, str(hour_12).zfill(2))

            self.minute_entry.delete(0, "end")
            self.minute_entry.insert(0, str(minute).zfill(2))

            self.am_pm_dropdown.set(am_pm)
            
            self.day_entry.delete(0, "end")
            self.day_entry.insert(0, str(dt.day).zfill(2))

            self.month_entry.delete(0, "end")
            self.month_entry.insert(0, str(dt.month).zfill(2))

            self.year_entry.delete(0, "end")
            self.year_entry.insert(0, str(dt.year))

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
                entry.insert(0, self.treatmentCost if isEditMode else "")
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
        
        self.auto_time_var = customtkinter.BooleanVar(value=True)
        self.manual_time_check = customtkinter.CTkCheckBox(self.entryGridFrame, text="Auto current time date", variable=self.auto_time_var, command=self.toggle_time_fields)
        self.manual_time_check.grid(row=index+1, column=0,sticky="w")
        

        self.manualTimeContainer = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
        self.manualTimeContainer.grid(row=index+2, column=0, sticky="nsew", columnspan=3, padx=10, pady=10)
        self.manualTimeContainer.grid_columnconfigure(0, weight=1)
        self.manualTimeContainer.grid_columnconfigure(1, weight=1)
        self.manualTimeContainer.grid_columnconfigure(2, weight=1)
        
        self.manualTimeDesc = customtkinter.CTkLabel(self.manualTimeContainer, text="Enter time of treatment:")
       
        # Time entry fields (initially hidden)
        self.hourContainer = customtkinter.CTkFrame(self.manualTimeContainer, fg_color="transparent", bg_color="transparent")
        self.hour_label = customtkinter.CTkLabel(self.hourContainer, text="Hour:")
        self.hour_label.grid(row=0, column=0, sticky="w")
        self.hour_entry = customtkinter.CTkEntry(self.hourContainer, width=50)
        self.hour_entry.grid(row=0, column=1, sticky="w", padx=(20, 0))

        self.minuteContainer = customtkinter.CTkFrame(self.manualTimeContainer,fg_color="transparent", bg_color="transparent")
        self.minute_label = customtkinter.CTkLabel(self.minuteContainer, text="Minute:")
        self.minute_label.grid(row=0, column=0, sticky="w")
        self.minute_entry = customtkinter.CTkEntry(self.minuteContainer, width=50)
        self.minute_entry.grid(row=0, column=1, sticky="w", padx=(20, 0))

        self.amPmContainer = customtkinter.CTkFrame(self.manualTimeContainer,fg_color="transparent", bg_color="transparent")
        self.am_pm_label = customtkinter.CTkLabel(self.amPmContainer, text="AM/PM:")
        self.am_pm_dropdown = customtkinter.CTkComboBox(self.amPmContainer, values=["AM", "PM"], width=70, state="readonly")
        self.am_pm_label.grid(row=0, column=0, sticky="w")
        self.am_pm_dropdown.grid(row=0, column=1, sticky="w", padx=(20, 0))

        # Day
        self.dayContainer = customtkinter.CTkFrame(self.manualTimeContainer, fg_color="transparent", bg_color="transparent")
        self.day_label = customtkinter.CTkLabel(self.dayContainer, text="Day:")
        self.day_label.grid(row=0, column=0, sticky="w")
        self.day_entry = customtkinter.CTkEntry(self.dayContainer, width=50)
        self.day_entry.grid(row=0, column=1, sticky="w", padx=(20, 0), pady=(10, 0))
        self.dayContainer.grid(row=2, column=0, sticky="w")

        # Month
        self.monthContainer = customtkinter.CTkFrame(self.manualTimeContainer, fg_color="transparent", bg_color="transparent")
        self.month_label = customtkinter.CTkLabel(self.monthContainer, text="Month:")
        self.month_label.grid(row=0, column=0, sticky="w")
        self.month_entry = customtkinter.CTkEntry(self.monthContainer, width=50)
        self.month_entry.grid(row=0, column=1, sticky="w", padx=(20, 0), pady=(10, 0))
        self.monthContainer.grid(row=2, column=1, sticky="w")

        # Year
        self.yearContainer = customtkinter.CTkFrame(self.manualTimeContainer, fg_color="transparent", bg_color="transparent")
        self.year_label = customtkinter.CTkLabel(self.yearContainer, text="Year:")
        self.year_label.grid(row=0, column=0, sticky="w")
        self.year_entry = customtkinter.CTkEntry(self.yearContainer, width=70)
        self.year_entry.grid(row=0, column=1, sticky="w", padx=(20, 0), pady=(10, 0))
        self.yearContainer.grid(row=2, column=2, sticky="w")

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
            customtkinter.CTkButton(self.actionButtonsFrame, text="Add Treatment", command=lambda: self.createTreatment(conditionID, self.entryFields)).grid(row=0, column=0, pady=(20, 0))

        self.toggle_time_fields()