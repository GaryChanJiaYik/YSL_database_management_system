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

    entryFieldList = [ dbCol.treatmentDescription, dbCol.treatmentPainLevel, dbCol.treatmentNumbLevel, dbCol.treatmentSoreLevel, dbCol.treatmentTenseLevel]
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
            combined_datetime = formatDateTime(
                self,
                self.hour_entry.get(), self.minute_entry.get(), self.am_pm_dropdown.get())
        final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")

        params = {
            "pConditionId": conditionId,
            "pTreatmentDescription": entryFields[dbCol.treatmentDescription].get("1.0", customtkinter.END).strip(),
            "pNumbLevel": self.selected_levels[dbCol.treatmentNumbLevel].get(),
            "pPainLevel": self.selected_levels[dbCol.treatmentPainLevel].get(),
            "pSoreLevel": self.selected_levels[dbCol.treatmentSoreLevel].get(),
            "pTenseLevel": self.selected_levels[dbCol.treatmentTenseLevel].get(),
            "pTreatmentDate": final_time_string,
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
        from windows.conditionDetailsView import ConditionDetailsView
        self.controller.setCustomerID(self.conditionModel.customerId)
        self.controller.setConditionModel(self.conditionModel)

        # Clean up the current frame from stack
        if len(self.controller.window_stack) > 0:
            self.controller.window_stack.pop()

        self.controller.switch_frame(WINDOW_CONDITION_DETAIL, isFromBackButton=True)

    def toggle_time_fields(self):
        if self.auto_time_var.get():       
            self.manualTimeDesc.grid_remove()
            self.hour_label.grid_remove()
            self.hour_entry.grid_remove()
            self.minute_label.grid_remove()
            self.minute_entry.grid_remove()
            self.am_pm_label.grid_remove()
            self.am_pm_dropdown.grid_remove()
        else:
            self.manualTimeDesc.grid(row=0, column=0, sticky="w")
            self.hourContainer.grid(row=1, column=0, sticky="w")
            self.minuteContainer.grid(row=1, column=1, sticky="w")  
            self.amPmContainer.grid(row=1, column=2, sticky="w")

            self.hour_entry.grid(row=0, column=1, sticky="w", padx=(20, 0))
            self.minute_label.grid(row=0, column=0, sticky="w")
            self.minute_entry.grid(row=0, column=1, sticky="w", padx=(20, 0))
            self.am_pm_label.grid(row=0, column=0, sticky="w")
            self.am_pm_dropdown.grid(row=0, column=1, sticky="w", padx=(20, 0))

    
    def on_text_change(self, event=None):
        current_text = self.entryFields[dbCol.treatmentDescription].get("1.0", "end-1c")
        if not checkLengthOfInput(current_text, 0, TREATMENT_DESCRIPTION_CHARACTER_LIMIT):
            # Truncate extra characters
            self.entryFields[dbCol.treatmentDescription].delete("1.0", "end")
            self.entryFields[dbCol.treatmentDescription].insert("1.0", current_text[:TREATMENT_DESCRIPTION_CHARACTER_LIMIT])
            self.warning_label.configure(text=f"Maximum {TREATMENT_DESCRIPTION_CHARACTER_LIMIT} characters reached!", text_color="red")
        else:

            self.warning_label.configure(text=f"{len(current_text)}/{TREATMENT_DESCRIPTION_CHARACTER_LIMIT}", text_color="green")

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

        except ValueError:
            print("Invalid datetime format. Expected: 'YYYY-MM-DD HH:MM:SS'")
            
    def deleteRecord(self):
        print("Remove record")

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

                self.warning_label = customtkinter.CTkLabel(treatmentDescFrame, text="", text_color="red")
                self.warning_label.grid(row=1, column=0, sticky='e')

                #self.createLabelWithInputfield(self.newWindow, field, self.entryFields, None, False).grid(row=idx+1, column=0, sticky='w')
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
        
        self.auto_time_var = customtkinter.BooleanVar()
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

        #2025-05-05 13:17:10

        # Add frame for buttons
        self.actionButtonsFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
        self.actionButtonsFrame.grid(row=index+3, column=0)
        self.actionButtonsFrame.grid_columnconfigure(0, weight=1)
        self.actionButtonsFrame.grid_columnconfigure(1, minsize=50)
        self.actionButtonsFrame.grid_columnconfigure(2, weight=1)
    
        


        if isEditMode:
            self.populateTimeFields(self.treatmentModel.treatmentDate)

            customtkinter.CTkButton(self.actionButtonsFrame, text="Save", command=lambda: self.createTreatment(conditionID, self.entryFields, saveMode=True)).grid(row=0, column=0)
            customtkinter.CTkButton(self.actionButtonsFrame, text="Delete", fg_color="red", text_color="white", hover_color="darkred", command=lambda: self.deleteRecord).grid(row=0, column=1, padx=(10,0))
        else:
            customtkinter.CTkButton(self.actionButtonsFrame, text="Add Treatment", command=lambda: self.createTreatment(conditionID, self.entryFields)).grid(row=0, column=0)

        self.toggle_time_fields()