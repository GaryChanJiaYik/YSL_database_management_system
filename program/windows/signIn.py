import customtkinter as ctk
from Constant.appConstant import STANDARD_WINDOW_SIZE
from securityModule import security 
from Components.popupModal import renderPopUpModal
from Constant.errorCode import ERROR, INVALID_CREDENTIALS
class SignInWindow:
    def __init__(self, controller, root):
        self.controller = controller
        self.signInWindow = ctk.CTkToplevel(root)
        self.signInWindow.title("Admin Sign In")
        self.signInWindow.geometry(STANDARD_WINDOW_SIZE) 
        # Ensure it stays above the root window
        self.signInWindow.transient(root)
        # Focus the new window
        self.signInWindow.grab_set()
        # Optional: Make it modal (user can't click other windows until it closes)
        self.signInWindow.focus_set()
        

        
        self.signInWindowContainer = ctk.CTkFrame(self.signInWindow, fg_color="transparent", bg_color="transparent")
        self.signInWindowContainer.pack(expand=True)

        ctk.CTkLabel(self.signInWindowContainer, text="Admin Sign In", font=("Arial", 24)).grid(row=0, column=0, padx=10, pady=0)

        #Sign in form
        self.signInFormContainer = ctk.CTkFrame(self.signInWindowContainer, fg_color="transparent", bg_color="transparent")
        self.signInFormContainer.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Username field
        self.usernameLabel = ctk.CTkLabel(self.signInFormContainer, text="Username")
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=5)
        self.usernameEntry = ctk.CTkEntry(self.signInFormContainer, placeholder_text="Username", width=200)
        self.usernameEntry.grid(row=0, column=1, padx=10, pady=5)

        # Password field
        self.passwordLabel = ctk.CTkLabel(self.signInFormContainer, text="Password")
        self.passwordLabel.grid(row=1, column=0, padx=10, pady=5)
        self.passwordEntry = ctk.CTkEntry(self.signInFormContainer, show="*", placeholder_text="Password",width=200)
        self.passwordEntry.grid(row=1, column=1, padx=10, pady=0)

        self.errorLabel = ctk.CTkLabel(self.signInFormContainer, text="", text_color="red")
        self.errorLabel.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 0))


        # Sign In button
        self.signInButton = ctk.CTkButton(self.signInFormContainer, text="Sign In", command=self.validation)
        self.signInButton.grid(row=3, column=0, columnspan=2, padx=10, pady=(10,5))
        # Cancel button
        self.cancelButton = ctk.CTkButton(self.signInFormContainer, text="Exit", command=self.signInWindow.destroy, fg_color="red", text_color="white")
        self.cancelButton.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        # Set the grid weight to make the frame responsive
        self.signInWindowContainer.grid_rowconfigure(0, weight=1)
        self.signInWindowContainer.grid_columnconfigure(0, weight=1)
        self.signInFormContainer.grid_rowconfigure(0, weight=1)
        self.signInFormContainer.grid_columnconfigure(0, weight=1)  
        self.signInFormContainer.grid_columnconfigure(1, weight=1)


        

    def validation(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        username = security.sha256_hash(username)
        password = security.sha256_hash(password)


        if username == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" and password == "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9":
            print("Sign In Successful")
            # Close the sign-in window
            self.controller.setAdminAccess(True)
            print("Admin access: ", self.controller.getIsAdminAccess())

            self.signInWindow.destroy()
        else:
            self.errorLabel.configure(text=INVALID_CREDENTIALS)