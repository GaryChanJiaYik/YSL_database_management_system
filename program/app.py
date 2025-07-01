import customtkinter as ctk
from Constant.appConstant import *
from windows.landing import LandingWindow
from windows.customerDetailsRevamp import CustomerDetailsViewRevamp
from windows.conditionDetailsView import ConditionDetailsView
from windows.addTreatmentRevamp import AddTreatmentViewRevamp
from windows.treatmentDetails import TreatmentDetailView
from Components.previousWindowButton import PreviousWindowButton
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
        
    def setCustomerName(self, customerName):
        self.currentCustomerName = customerName
    
    def setTreatmentID(self, treatmentID):
        self.currentTreatmentID = treatmentID

    def setConditionID(self, conditionID):
        self.currentConditionID = conditionID

    def getCustomerID(self):
        return self.currentCustomerID
    
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

    def setAdminAccess(self, access):
        self.adminAccess = access
        if access:
            print("Admin Access Granted")
            self.resetWindow()

        print("Stack: ", self.window_stack)

    def getIsAdminAccess(self):
        return self.adminAccess
    
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

    def __init__(self):        
        self.appRoot = ctk.CTk()
        self.appRoot.title("YSL DB Management")
        self.appRoot.geometry("800x600")  # Replace with your STANDARD_WINDOW_SIZE

        self.appCommonHeaderContainer = ctk.CTkFrame(self.appRoot, bg_color="transparent", fg_color="transparent", height=50)
        self.appCommonHeaderContainer.grid_rowconfigure(0, weight=1)
        
        self.appCommonHeaderContainer.grid_columnconfigure(0, weight=3)  
        self.appCommonHeaderContainer.grid_columnconfigure(1, weight=1)  
        self.appCommonHeaderContainer.grid_columnconfigure(2, weight=1)  

        ctk.CTkLabel(self.appCommonHeaderContainer, text="(ADMIN) YSL DB Management" if self.adminAccess else "YSL DB Management", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")

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

    def switch_frame(self, frameClass, isFromBackButton=False):
        if not isFromBackButton:
            self.window_stack.append(frameClass)

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
            self.current_frame = AddTreatmentViewRevamp(self.container, self, self.currentConditionID, self.currentConditionModel)
        elif frameClass == WINDOW_EDIT_TREATMENT:
            self.current_frame = AddTreatmentViewRevamp(self.container, self, self.currentConditionID, self.currentConditionModel, isEditMode=True)

        self.current_frame.pack(fill="both", expand=True)
    
        self.set_header()
        
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
