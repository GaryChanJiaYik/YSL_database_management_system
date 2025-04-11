import tkinter as tk
import Constant.dbColumn as dbCol
from Constant.converterFunctions import convertTimeStampToId
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
        tk.Label(frame, text =label, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
        entry = None

        if isSelectBox: 
            entry = ttk.OptionMenu(
                frame,
                selectedLevelVar,
                self.optionLevel[0],
                *self.optionLevel)
        else:    
            entry = tk.Entry(frame, bg='lightgray')
        

        entry.grid(row=0, column=2, sticky='w')
        if entryFields.get(label) is None:
            entryFields[label] = entry

        return frame
    


    def createTreatment(self, customerID, entryFields):
        print(entryFields)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        treatment = TM.TreatmentModel(
            pCustomerId=customerID, 
            pTreatmentName= entryFields[dbCol.treatmentName].get() ,
            pTreatmentDescription=entryFields[dbCol.treatmentDescription].get(), 
            pNumbLevel= self.selected_levels[dbCol.treatmentNumbLevel].get(),
            pPainLevel=self.selected_levels[dbCol.treatmentPainLevel].get(),
            pSoreLevel=self.selected_levels[dbCol.treatmentSoreLevel].get(),
            pTenseLevel=self.selected_levels[dbCol.treatmentTenseLevel].get(),
            pTreatmentDate=date,
            )
        TreatmentFunc.createTreatment(treatment)
        print("Create treatment button pressed")
        renderPopUpModal(self.root, "Treatment added successfully","Successful", "Success")
        self.newWindow.destroy()

   


    def __init__(self, root, customerId):
        #!!!!!!!!!!! customerId in timeStamp format
        self.entryFields = {} #Store the label name(variables) corresponding to the entry field


        self.root = root
        self.newWindow = tk.Toplevel(self.root)
        self.newWindow.title("Add treatment")
    
        # sets the geometry of toplevel
        self.newWindow.geometry(STANDARD_WINDOW_SIZE)

        tk.Label(self.newWindow, text=f'Add Treatment for customer: {convertTimeStampToId(customerId)}' ).grid(column=0, row=0)

         # initialize data
        self.optionLevel = ['1', '2', '3','4', '5', '6', '7', '8','9','10']        

        self.selected_levels = {
            dbCol.treatmentPainLevel:tk.StringVar(value=self.optionLevel[0]), 
            dbCol.treatmentNumbLevel:tk.StringVar(value=self.optionLevel[0]),
            dbCol.treatmentSoreLevel:tk.StringVar(value=self.optionLevel[0]),
            dbCol.treatmentTenseLevel:tk.StringVar(value=self.optionLevel[0])
            }
        #self.selected_level = tk.StringVar(value=self.optionLevel[0])




        for idx, field in enumerate(self.entryFieldList):
            if field is dbCol.treatmentName or field is dbCol.treatmentDescription:
                self.createLabelWithInputfield(self.newWindow, field, self.entryFields, None, False).grid(row=idx+1, column=0, sticky='w')
            else:
                self.createLabelWithInputfield(self.newWindow, field, self.entryFields,self.selected_levels[field], isSelectBox=True,).grid(row=idx+1, column=0, sticky='w')

       


        tk.Button(self.newWindow, text="Add Treatment", command=lambda: self.createTreatment(convertTimeStampToId(customerId), self.entryFields)).grid(row=10, column=0)
