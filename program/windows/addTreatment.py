import tkinter as tk
import Constant.dbColumn as dbCol
from Constant.converterFunctions import convertTimeStampToId, formatDateTime
from Constant.appConstant import STANDARD_WINDOW_SIZE
import Constant.treatmentDatabaseFunctions as TreatmentFunc
import Model.treatmentModel as TM
import datetime
from tkinter import ttk
from Components.popupModal import renderPopUpModal



class AddTreatmentView:

    entryFieldList = [dbCol.treatmentName, dbCol.treatmentDescription, dbCol.treatmentPainLevel, dbCol.treatmentNumbLevel, dbCol.treatmentSoreLevel, dbCol.treatmentTenseLevel]

    def createLabelWithInputfield(self, root, label, entryFields,selectedLevelVar, isSelectBox=False, ):

        frame = tk.Frame(root)
        tk.Label(frame, text =label, width=25, fg='black', font=('Arial',9), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
        entry = None

        if isSelectBox: 
            entry = ttk.OptionMenu(
                frame,
                selectedLevelVar,
                self.optionLevel[0],
                *self.optionLevel)
        else:  
            if label is dbCol.treatmentDescription:
                entry = tk.Text(frame, width=50, height=10, font=('Arial',9))  
            else:
                entry = tk.Text(frame,width=50, height=2,font=('Arial', 9))
        

        entry.grid(row=0, column=2, sticky='w')
        if entryFields.get(label) is None:
            entryFields[label] = entry

        return frame
    


    def createTreatment(self, customerID, entryFields):
        now = datetime.datetime.now()

        if self.manual_time_var.get():
            combined_datetime = formatDateTime(
                self.newWindow,
                self.hour_entry.get(), self.minute_entry.get(), self.am_pm_dropdown.get())
        else:
            combined_datetime = now
        

        final_time_string = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")


        print(entryFields)
        print("OK PASSED DATE CONVERSION")
        treatment = TM.TreatmentModel(
            pCustomerId=customerID, 
            pTreatmentName= entryFields[dbCol.treatmentName].get("1.0", tk.END).strip() ,
            pTreatmentDescription=entryFields[dbCol.treatmentDescription].get("1.0", tk.END).strip(), 
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
        if self.manual_time_var.get():
            self.manualTimeDesc.grid(row=0, column=0, sticky="w")
            self.hour_label.grid(row=1, column=0, sticky="w")
            self.hour_entry.grid(row=1, column=1)
            self.minute_label.grid(row=1, column=2, sticky="w")
            self.minute_entry.grid(row=1, column=3)
            self.am_pm_label.grid(row=1, column=4, sticky="w")
            self.am_pm_dropdown.grid(row=1, column=5)
        else:
            self.manualTimeDesc.grid_remove()
            self.hour_label.grid_remove()
            self.hour_entry.grid_remove()
            self.minute_label.grid_remove()
            self.minute_entry.grid_remove()
            self.am_pm_label.grid_remove()
            self.am_pm_dropdown.grid_remove()

    def __init__(self, root, customerId):
        #!!!!!!!!!!! customerId in timeStamp format
        self.entryFields = {} #Store the label name(variables) corresponding to the entry field


        self.root = root
        self.newWindow = tk.Toplevel(self.root)
        self.newWindow.title("Add treatment")
    
        # sets the geometry of toplevel
        self.newWindow.geometry(STANDARD_WINDOW_SIZE)

        tk.Label(self.newWindow, text=f'Add Treatment for customer: {convertTimeStampToId(customerId)}' , font=('Arial',12)).grid(column=0, row=0, sticky='w')

         # initialize data
        self.optionLevel = ['1', '2', '3','4', '5', '6', '7', '8','9','10']        

        self.selected_levels = {
            dbCol.treatmentPainLevel:tk.StringVar(value=self.optionLevel[0]), 
            dbCol.treatmentNumbLevel:tk.StringVar(value=self.optionLevel[0]),
            dbCol.treatmentSoreLevel:tk.StringVar(value=self.optionLevel[0]),
            dbCol.treatmentTenseLevel:tk.StringVar(value=self.optionLevel[0])
            }
        #self.selected_level = tk.StringVar(value=self.optionLevel[0])


        index = 1

        for idx, field in enumerate(self.entryFieldList):
            if field is dbCol.treatmentName or field is dbCol.treatmentDescription:
                self.createLabelWithInputfield(self.newWindow, field, self.entryFields, None, False).grid(row=idx+1, column=0, sticky='w')
            else:
                self.createLabelWithInputfield(self.newWindow, field, self.entryFields,self.selected_levels[field], isSelectBox=True,).grid(row=idx+1, column=0, sticky='w')
            index+=1


        self.manual_time_var = tk.BooleanVar()
        self.manual_time_check = tk.Checkbutton(self.newWindow, text="Manually enter time", variable=self.manual_time_var, command=self.toggle_time_fields)
        self.manual_time_check.grid(row=index+1, column=0, columnspan=6, sticky="w")


        self.manualTimeContainer = tk.Frame(self.newWindow)
        self.manualTimeContainer.grid(row=index+2, column=0, sticky="w")

        self.manualTimeDesc = tk.Label(self.manualTimeContainer, text="Enter time of treatment:")
       
        # Time entry fields (initially hidden)
        self.hour_label = tk.Label(self.manualTimeContainer, text="Hour:")
        self.hour_entry = tk.Entry(self.manualTimeContainer, width=5)

        self.minute_label = tk.Label(self.manualTimeContainer, text="Minute:")
        self.minute_entry = tk.Entry(self.manualTimeContainer, width=5)

        self.am_pm_label = tk.Label(self.manualTimeContainer, text="AM/PM:")
        self.am_pm_dropdown = ttk.Combobox(self.manualTimeContainer, values=["AM", "PM"], width=5, state="readonly")
        




        tk.Button(self.newWindow, text="Add Treatment", command=lambda: self.createTreatment(convertTimeStampToId(customerId), self.entryFields)).grid(row=index+3, column=0)
