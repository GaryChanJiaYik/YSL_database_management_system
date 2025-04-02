import tkinter as tk
import Constant.dbColumn as dbCol
from Constant.converterFunctions import convertTimeStampToId
from Constant.appConstant import STANDARD_WINDOW_SIZE
import Constant.treatmentDatabaseFunctions as TreatmentFunc
import Model.treatmentModel as TM
import datetime

class AddTreatmentView:

    entryFieldList = [dbCol.treatmentName, dbCol.treatmentDescription, dbCol.treatmentPainLevel, dbCol.treatmentNumbLevel, dbCol.treatmentSoreLevel, dbCol.treatmentTenseLevel]

    def createLabelWithTextfield(self, root, label, entryFields):

        frame = tk.Frame(root)
        tk.Label(frame, text =label, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
        entry = tk.Entry(frame, bg='lightgray')
        entry.grid(row=0, column=2)
        if entryFields.get(label) is None:
            entryFields[label] = entry

        return frame


    def createTreatment(self, customerID, entryFields):
        print(entryFields)
        date = datetime.datetime.now()
        
        treatment = TM.TreatmentModel(
            pCustomerId=customerID, 
            pTreatmentName= entryFields[dbCol.treatmentName].get() ,
            pTreatmentDescription=entryFields[dbCol.treatmentDescription].get(), 
            pNumbLevel= entryFields[dbCol.treatmentNumbLevel].get(),
            pPainLevel=entryFields[dbCol.treatmentPainLevel].get(),
            pSoreLevel=entryFields[dbCol.treatmentSoreLevel].get(),
            pTenseLevel=entryFields[dbCol.treatmentTenseLevel].get(),
            pTreatmentDate=date,
            )
        TreatmentFunc.createTreatment(treatment)
        print("Create treatment button pressed")



    def __init__(self, root, customerId):
        #!!!!!!!!!!! customerId in timeStamp format
        self.entryFields = {} #Store the label name(variables) corresponding to the entry field


        self.root = root
        self.newWindow = tk.Toplevel(self.root)
        self.newWindow.title("Add treatment")
    
        # sets the geometry of toplevel
        self.newWindow.geometry(STANDARD_WINDOW_SIZE)

        tk.Label(root, text=f'Add Treatment for customer: {convertTimeStampToId(customerId)}' ).grid(column=0, row=0)


        for idx, field in enumerate(self.entryFieldList):
            self.createLabelWithTextfield(self.newWindow, field, self.entryFields).grid(row=idx+1, column=0)


        '''
        #For 
        self.frame1 = tk.Frame(self.newWindow)
        tk.Label(self.frame1, text=dbCol.treatmentName, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)
        self.treatmentNameEntry = tk.Entry(self.frame1, bg='lightgray')
        self.treatmentNameEntry.grid(row=0, column=2)
        self.frame1.grid(row=2, column=0)

        self.frame2 = tk.Frame(self.newWindow)
        tk.Label(self.frame2, text=dbCol.treatmentDescription, width=25, fg='black', font=('Arial', 12), justify="left", anchor="w", pady=1).grid(row=0, column=0, columnspan=2)

        self.treatmentDescriptionEntry = tk.Entry(self.frame2, bg='lightgray')
        self.treatmentDescriptionEntry.grid(row=0, column=2)

        self.frame2.grid(row=3, column=0)
'''
        tk.Button(self.newWindow, text="Add Treatment", command=lambda: self.createTreatment(convertTimeStampToId(customerId), self.entryFields)).grid(row=10, column=0)