import customtkinter
import Constant.dbColumn as dbCol
from Constant.appConstant import STANDARD_TEXT_BOX_WIDTH, STANDARD_TEXT_BOX_HEIGHT, WINDOW_CUSTOMER_DETAIL
from services.conditionDbFunctions import updateConditionByID, deleteCondition
from Components.popupModal import renderPopUpModal
from Components.datePickerModal import DatePickerModal
from Components.timePickerModal import TimePickerModal
from datetime import datetime


class EditConditionView(customtkinter.CTkFrame):
    
    entryFieldList = [dbCol.conditionDescription]
    
    def saveCondition(self):
        updated_desc = self.entryFields[dbCol.conditionDescription].get("1.0", customtkinter.END).strip()
        date_str = self.date_value.get().strip()
        time_str = self.time_value.get().strip()
        # Warning
        # if not updated_desc:
        #     self.desc_warning_label.configure(text="Description cannot be empty.")
        #     return
        # else:
        #     self.desc_warning_label.configure(text="")
        try:
            combined_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
            final_datetime_str = combined_datetime.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            final_datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        success = updateConditionByID(self.conditionModel.conditionId, updated_desc, final_datetime_str)

        if success:
            renderPopUpModal(self.parent, "Condition updated successfully", "Success", "Success")
            print("Condition updated")
        else:
            renderPopUpModal(self.parent, "Failed to update condition", "Error", "Error")
            print("Failed to update condition")
        
        self.backToPreviousWindow()
    
    
    def deleteCondition(self):
        #  Confirmation
        # confirm = customtkinter.CTkInputDialog(text="Are you sure you want to delete this condition?", title="Confirm Delete")
        # if confirm.get_input() != "yes":
        #     return
        success = deleteCondition(self.conditionModel.conditionId)

        if success:
            renderPopUpModal(self.parent, "Condition deleted successfully", "Deleted", "Success")
            print("Condition deleted")
        else:
            renderPopUpModal(self.parent, "Failed to delete condition", "Error", "Error")
            print("Failed to delete condition")
   
        self.backToPreviousWindow()
    
    
    def backToPreviousWindow(self):
        self.controller.setCustomerID(self.conditionModel.customerId)
        self.controller.setConditionModel(self.conditionModel)

        # Clean up the current frame from stack
        if len(self.controller.window_stack) > 0:
            self.controller.window_stack.pop()

        self.controller.switch_frame(WINDOW_CUSTOMER_DETAIL, isFromBackButton=True)
    
    
    def openDatePicker(self):
        DatePickerModal.open_date_picker(
            parent=self,
            current_date_str=self.date_value.get(),
            on_selected=lambda date_str: self._set_date_value(date_str)
        )

    def _set_date_value(self, date_str):
        self.date_value.configure(state="normal")
        self.date_value.delete(0, "end")
        self.date_value.insert(0, date_str)
        self.date_value.configure(state="disabled")

    
    def openTimePicker(self):
        TimePickerModal.open_time_picker(
            parent=self,
            current_time_str=self.time_value.get().strip(),
            on_selected=lambda time_str: self._set_time_value(time_str)
        )

    def _set_time_value(self, time_str):
        self.time_value.configure(state="normal")
        self.time_value.delete(0, "end")
        self.time_value.insert(0, time_str)
        self.time_value.configure(state="disabled")
    
    
    def populateDateTimeFields(self, datetime_string):
        try:
            dt = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")
            formatted_date = dt.strftime("%Y-%m-%d")
            formatted_time = dt.strftime("%I:%M %p")

            self.date_value.configure(state="normal")
            self.date_value.delete(0, "end")
            self.date_value.insert(0, formatted_date)
            self.date_value.configure(state="disabled")

            self.time_value.configure(state="normal")
            self.time_value.delete(0, "end")
            self.time_value.insert(0, formatted_time)
            self.time_value.configure(state="disabled")

        except ValueError:
            print("Invalid datetime format.")
    
    
    def __init__(self, parent, controller, customerId, conditionModel):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.customerId = customerId
        self.conditionModel = conditionModel
        
        self.entryFields = {}
        
        self.entryGridFrame = customtkinter.CTkFrame(self, width=500, fg_color="transparent", bg_color="transparent")
        self.entryGridFrame.grid_columnconfigure(0, weight=2)
        self.entryGridFrame.grid_columnconfigure(1, weight=1)
        self.entryGridFrame.grid_columnconfigure(2, weight=2)
        self.entryGridFrame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        index = 1

        for idx, field in enumerate(self.entryFieldList):
            #render text
            customtkinter.CTkLabel(self.entryGridFrame, text =dbCol.ConditionModelAttributeToField[field], pady=1).grid(row=idx+1, column=0, sticky='nw', pady=10)
            customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(row=idx+1, column=1, sticky='nw')
            
            # entry = None
            
            #render entry
            if field is dbCol.conditionDescription:
                #create enty text 
                conditionDescFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
                conditionDescFrame.grid(row=idx+1, column=2, sticky='w')

                entry = customtkinter.CTkTextbox(conditionDescFrame, width=STANDARD_TEXT_BOX_WIDTH, height=STANDARD_TEXT_BOX_HEIGHT)
                entry.insert("0.0", self.conditionModel.conditionDescription)
                # entry.bind("<KeyRelease>", self.on_text_change)
                # entry.bind("<<Paste>>", lambda e: self.after(1, self.on_text_change))
                
                entry.grid(row=0, column=0, sticky='w')

                self.desc_warning_label = customtkinter.CTkLabel(conditionDescFrame, text="", text_color="red")
                self.desc_warning_label.grid(row=1, column=0, sticky='e')

                #self.createLabelWithInputfield(self.newWindow, field, self.entryFields, None, False).grid(row=idx+1, column=0, sticky='w')
            
            if self.entryFields.get(field) is None:
                self.entryFields[field] = entry
            
            index+=1
        
        # === Date ===
        customtkinter.CTkLabel(self.entryGridFrame, text="Date:", pady=1).grid(
            row=index, column=0, sticky="w", pady=10
        )
        customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(
            row=index, column=1
        )

        dateInputFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent")
        dateInputFrame.grid(row=index, column=2, sticky="w")

        self.date_value = customtkinter.CTkEntry(dateInputFrame, width=120)
        self.date_value.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_value.configure(state="disabled")
        self.date_value.grid(row=0, column=0, padx=(0, 10))

        customtkinter.CTkButton(dateInputFrame, text="Edit", width=60, command=self.openDatePicker).grid(row=0, column=1)

        # === Time ===
        customtkinter.CTkLabel(self.entryGridFrame, text="Time:", pady=1).grid(
            row=index + 1, column=0, sticky="w", pady=10
        )
        customtkinter.CTkLabel(self.entryGridFrame, text=" ", width=50).grid(
            row=index + 1, column=1
        )

        timeInputFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent")
        timeInputFrame.grid(row=index + 1, column=2, sticky="w")

        self.time_value = customtkinter.CTkEntry(timeInputFrame, width=120)
        self.time_value.insert(0, datetime.now().strftime("%I:%M %p"))
        self.time_value.configure(state="disabled")
        self.time_value.grid(row=0, column=0, padx=(0, 10))

        customtkinter.CTkButton(timeInputFrame, text="Edit", width=60, command=self.openTimePicker).grid(row=0, column=1)
        
        self.populateDateTimeFields(self.conditionModel.conditionDate)
            
        # Add frame for buttons
        self.actionButtonsFrame = customtkinter.CTkFrame(self.entryGridFrame, fg_color="transparent", bg_color="transparent")
        self.actionButtonsFrame.grid(row=index+3, column=0)
        self.actionButtonsFrame.grid_columnconfigure(0, weight=1)
        self.actionButtonsFrame.grid_columnconfigure(1, minsize=50)
        self.actionButtonsFrame.grid_columnconfigure(2, weight=1)

        customtkinter.CTkButton(self.actionButtonsFrame, text="Save", command=self.saveCondition).grid(row=0, column=0)
        customtkinter.CTkButton(self.actionButtonsFrame, text="Delete", fg_color="red", text_color="white", hover_color="darkred", command=self.deleteCondition).grid(row=0, column=1, padx=(10,0))
        
        