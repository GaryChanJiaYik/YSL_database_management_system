import customtkinter as ctk
import time
import threading
from Constant.appConstant import *
from windows.landing import LandingWindow
from windows.customerDetailsRevamp import CustomerDetailsViewRevamp
from windows.conditionDetailsView import ConditionDetailsView
from windows.addTreatmentRevamp import AddTreatmentViewRevamp
from windows.treatmentDetails import TreatmentDetailView
from windows.editCondition import EditConditionView
from windows.addCustomerView import AddCustomerView
from windows.viewSalesView import ViewSalesView
from windows.viewAppointmentView import ViewAppointmentView
from windows.viewGenerateReportView import ViewGenerateReportView
from Components.previousWindowButton import PreviousWindowButton
from version import __version__
from Components.tooltip import ToolTip
from windows.signIn import SignInWindow

class App:

    currentCustomerID = None
    currentCustomerName = None
    currentTreatmentID = None
    currentConditionID = None
    currentConditionModel = None
    adminAccess = False

    window_stack = []

    def setCustomerID(self, customerID):
        self.currentCustomerID = customerID

    def setCustomerIC(self, customerIC):
        self.currentCustomerIC = customerIC
        
    def setCustomerName(self, customerName):
        self.currentCustomerName = customerName
    
    def setTreatmentID(self, treatmentID):
        self.currentTreatmentID = treatmentID

    def setConditionID(self, conditionID):
        self.currentConditionID = conditionID

    def getCustomerID(self):
        return self.currentCustomerID

    def getCustomerIC(self):
        return self.currentCustomerIC
    
    def getCustomerName(self):
        return self.currentCustomerName
    
    def getTreatmentID(self):
        return self.currentTreatmentID
    
    def getConditionID(self):
        return self.currentConditionID

    def setConditionModel(self, conditionModel):
        self.currentConditionModel = conditionModel
    
    def getConditionModel(self):
        return self.currentConditionModel
    
    def setCustomerModel(self, customerModel):
        self.currentCustomerModel = customerModel
    
    def getCustomerModel(self):
        return self.currentCustomerModel

    def setAdminAccess(self, access):
        self.adminAccess = access
        if access:
            print("Admin Access Granted")
            self.resetWindow()

        print("Stack: ", self.window_stack)

    def getIsAdminAccess(self):
        return self.adminAccess
    
    def getIsHiddenAccess(self):
        return self.hiddenAccess
    
    def resetWindow(self):
        self.window_stack = []
        print("Stack: ", self.window_stack)
        self.appRoot.destroy()
        self.__init__() 
        

    def renderAdminButton(self):
        if self.adminAccess:
            return ctk.CTkButton(self.buttonContainer, text="Logout", command=self.adminLogout, fg_color="red", text_color="white", hover_color="darkred")
        else:
            return ctk.CTkButton(self.buttonContainer, text="Admin", command=self.signInWindow)

    def adminLogout(self):
        self.adminAccess = False
        self.resetWindow()

    def getAppVersion(self):
        return __version__

    def __init__(self):        
        ctk.set_appearance_mode("dark")
        self.hiddenAccess = False
        self.click_count = 0
        self.last_click_time = 0
        self.listener_mode = False
        self.typed_sequence = ""
        self.current_frame_name = None
        self.listener_timeout_timer = None
        
        self.appRoot = ctk.CTk()
        self.appRoot.title(APP_NAME)
        #self.appRoot.geometry("1100x600")  # Replace with your STANDARD_WINDOW_SIZE
        self.center_window(1200, 600)

        self.appCommonHeaderContainer = ctk.CTkFrame(self.appRoot, bg_color="transparent", fg_color="transparent", height=50)
        self.appCommonHeaderContainer.grid_rowconfigure(0, weight=1)
        
        self.appCommonHeaderContainer.grid_columnconfigure(0, weight=3)  
        self.appCommonHeaderContainer.grid_columnconfigure(1, weight=1)  
        self.appCommonHeaderContainer.grid_columnconfigure(2, weight=1)

        self.appNameLabel = ctk.CTkLabel(self.appCommonHeaderContainer, text="(ADMIN) " + APP_NAME if self.adminAccess else APP_NAME, font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.appNameLabel.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ToolTip(self.appNameLabel, f"Version: {__version__}")
        # Bind click event to app name label
        self.appNameLabel.bind("<Button-1>", self.on_app_name_click)

        self.buttonContainer = ctk.CTkFrame(self.appCommonHeaderContainer, fg_color="transparent", bg_color="transparent", height=50)
        self.buttonContainer.grid(row=0, column=2, padx=0, pady=0)

        # Add buttons to the buttonContainer if needed
        self.backButtonContainer = ctk.CTkFrame(self.buttonContainer, fg_color="transparent", bg_color="transparent", height=50)
        self.backButtonContainer.grid(row=0, column=0, padx=0, pady=0)

        self.adminSignInButton = self.renderAdminButton()
        self.adminSignInButton.grid(row=0, column=1, padx=2, pady=0, sticky="e")

        self.appCommonHeaderContainer.pack(pady=2, fill="x")

        self.container = ctk.CTkScrollableFrame(self.appRoot)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.current_frame = None
        self.switch_frame(WINDOW_LANDING)

      
        self.appRoot.mainloop()
        
        # Debug Window stack
        # self.print_window_stack()

    def back_window(self):
        if len(self.window_stack) > 1:
            self.window_stack.pop()

        self.switch_frame(self.window_stack[-1], isFromBackButton=True)

    def switch_frame(self, frameClass, isFromBackButton=False, **kwargs):
        if not isFromBackButton:
            self.window_stack.append(frameClass)

        previousWindow = kwargs.get("previousWindow")
        
        # Destroy current frame if exists
        if self.current_frame is not None:
            self.current_frame.destroy()

        if frameClass == WINDOW_LANDING:
            self.current_frame = LandingWindow(self.container, self)
        elif frameClass == WINDOW_CUSTOMER_DETAIL:
            self.current_frame = CustomerDetailsViewRevamp(self.container, self, self.getCustomerID())
        elif frameClass == WINDOW_CONDITION_DETAIL:
            self.current_frame = ConditionDetailsView(self.container, self, self.currentCustomerID, self.currentConditionModel)
        elif frameClass == WINDOW_TREATMENT_DETAIL:
            self.current_frame =  TreatmentDetailView(self.container, self, self.currentTreatmentID)
        elif frameClass == WINDOW_ADD_TREATMENT:
            self.current_frame = AddTreatmentViewRevamp(self.container, self, self.currentConditionID, self.currentConditionModel, isEditMode=False, previousWindow=previousWindow)
        elif frameClass == WINDOW_EDIT_TREATMENT:
            self.current_frame = AddTreatmentViewRevamp(self.container, self, self.currentConditionID, self.currentConditionModel, isEditMode=True)
        elif frameClass == WINDOW_EDIT_CONDITION:
            self.current_frame = EditConditionView(self.container, self, self.currentCustomerID, self.currentConditionModel)
        elif frameClass == WINDOW_ADD_CUSTOMER:
            self.current_frame = AddCustomerView(self.container, self, isEditMode=False)
        elif frameClass == WINDOW_EDIT_CUSTOMER:
            customerId = self.getCustomerID()
            self.current_frame = AddCustomerView(self.container, self, isEditMode=True, customerId=customerId, previousWindow=previousWindow)
        elif frameClass == WINDOW_VIEW_SALE:
            self.current_frame = ViewSalesView(self.container, self)
        elif frameClass == WINDOW_VIEW_APPOINTMENT:
            self.current_frame = ViewAppointmentView(self.container, self)
        elif frameClass == WINDOW_VIEW_GENERATE_REPORT:
            self.current_frame = ViewGenerateReportView(self.container, self, self.getCustomerModel(), self.getConditionModel(), self.getTreatmentID())

        self.current_frame.pack(fill="both", expand=True)

        self.container._parent_canvas.yview_moveto(0)
        
        self.set_header()
        self.current_frame_name = frameClass
        # Debug Window stack
        # self.print_window_stack()

    def set_header(self):
        if len(self.window_stack) > 1:
            print("setting header back button")
            PreviousWindowButton(self, self.backButtonContainer)
        else:
            
            #hide the back button if it's the first frame
            for widget in self.backButtonContainer.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    widget.destroy()
    
    def center_window(self, width, height):
        screen_width = self.appRoot.winfo_screenwidth()
        screen_height = self.appRoot.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.appRoot.geometry(f"{width}x{height}+{x}+{y}")
    
    def signInWindow(self):
        # Placeholder for sign-in logic
        # This should open a new window for admin sign-in
        print("Sign In logic goes here")
        SignInWindow(self, self.appRoot)
        
    def print_window_stack(self):
        print("===== Window Stack =====")
        for i, frame in enumerate(self.window_stack):
            if hasattr(frame, '__name__'):
                print(f"{i + 1}: {frame.__name__}")
            else:
                print(f"{i + 1}: {str(frame)}")
        print("========================")


    def on_app_name_click(self, event):
        if  self.listener_mode:
            return
        
        current_time = time.time()
        if current_time - self.last_click_time > 1:
            self.click_count = 0  # Reset if too slow

        self.click_count += 1
        self.last_click_time = current_time

        print(f"Title clicked {self.click_count} time(s)")

        if self.click_count == 5:
            self.click_count = 0  # Always reset

            if self.hiddenAccess:
                self.deactivate_hidden_access()
            else:
                self.activate_listener_mode()


    def activate_listener_mode(self):
        self.listener_mode = True
        self.typed_sequence = ""
        print("Listener mode activated")
        self.appRoot.bind("<Key>", self.on_key_press)

        # Start a timer to cancel listener mode after X seconds
        if self.listener_timeout_timer:
            self.listener_timeout_timer.cancel()  # Cancel previous timer if still running

        self.listener_timeout_timer = threading.Timer(3.0, self.cancel_listener_mode)
        self.listener_timeout_timer.start()


    def cancel_listener_mode(self):
        self.listener_mode = False
        self.typed_sequence = ""
        self.appRoot.unbind("<Key>")
        print("Listener mode timed out")

       
    def deactivate_hidden_access(self):
        self.hiddenAccess = False
        self.listener_mode = False
        self.typed_sequence = ""
        self.appRoot.unbind("<Key>")
        if self.listener_timeout_timer:
            self.listener_timeout_timer.cancel()
        print("Hidden access deactivated")
        self.switch_frame(self.current_frame_name, True)


    def on_key_press(self, event):
        if not self.listener_mode:
            return

        # Only accept alphanumeric input
        if event.char.isalnum():
            self.typed_sequence += event.char
            print(f"Key typed: {event.char} -> Sequence: {self.typed_sequence}")

            if self.typed_sequence.endswith("ADMIN"):
                self.unlock_hidden_access()

            # Optional: prevent overflow
            if len(self.typed_sequence) > 10:
                self.typed_sequence = self.typed_sequence[-10:]


    def unlock_hidden_access(self):
        self.hiddenAccess = True
        self.listener_mode = False
        print("Hidden access granted!")

        if self.listener_timeout_timer:
            self.listener_timeout_timer.cancel()

        self.appRoot.unbind("<Key>")
        self.switch_frame(self.current_frame_name, True)