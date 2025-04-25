import customtkinter
from Constant.appConstant import STANDARD_WINDOW_SIZE, STANDARD_TEXT_BOX_WIDTH
import datetime
import Constant.dbColumn as dbCol
from Constant.converterFunctions import formatDateTime
import Constant.treatmentDatabaseFunctions as TreatmentFunc
import Model.treatmentModel as TM
import datetime
from tkinter import ttk
from Components.popupModal import renderPopUpModal


class AddTreatmentViewRevamp:

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

    def createTreatment(self, conditionId, entryFields):
        now = datetime.datetime.now()

        if self.auto_time_var.get():
            combined_datetime = now
        else:
            combined_datetime = formatDateTime(
                self.newWindow,
                self.hour_entry.get(), self.minute_entry.get(), self.am_pm_dropdown.get())
        final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")

        treatment = TM.TreatmentModel(
            pConditionId=conditionId, 
            pTreatmentDescription=entryFields[dbCol.treatmentDescription].get("1.0", customtkinter.END).strip(), 
            pNumbLevel= self.selected_levels[dbCol.treatmentNumbLevel].get(),
            pPainLevel=self.selected_levels[dbCol.treatmentPainLevel].get(),
            pSoreLevel=self.selected_levels[dbCol.treatmentSoreLevel].get(),
            pTenseLevel=self.selected_levels[dbCol.treatmentTenseLevel].get(),
            pTreatmentDate=final_time_string,
            )
        TreatmentFunc.createTreatment(treatment)
        print("Create treatment button pressed")
        renderPopUpModal(self.root, "Treatment added successfully","Successful", "Success")
        self.newWindow.destroy()

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

    def __init__(self, root, conditionID):
        self.root = root
        self.newWindow = customtkinter.CTkToplevel(self.root)
        self.newWindow.columnconfigure(0, weight=1)
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Add Treatment")
        
        # sets the geometry of toplevel
        self.newWindow.geometry(STANDARD_WINDOW_SIZE)

        self.entryFields = {} #Store the label name(variables) corresponding to the entry field

        self.root = root
        self.newWindow = customtkinter.CTkToplevel(self.root)
        self.newWindow.title("Add treatment")
    
        # sets the geometry of toplevel
        self.newWindow.geometry(STANDARD_WINDOW_SIZE)
        self.newWindow.grid_columnconfigure(0, weight=1)

         
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

        self.entryGridFrame = customtkinter.CTkFrame(self.newWindow, width=500)
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
                entry = customtkinter.CTkTextbox(self.entryGridFrame, width=STANDARD_TEXT_BOX_WIDTH)
                entry.grid(row=idx+1, column=2, sticky='w')

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

        customtkinter.CTkButton(self.entryGridFrame, text="Add Treatment", command=lambda: self.createTreatment(conditionID, self.entryFields)).grid(row=index+3, column=0)
        self.toggle_time_fields()