import customtkinter as ctk
from Constant.appConstant import STANDARD_WINDOW_SIZE
from securityModule import security 
from Components.popupModal import renderPopUpModal
from Constant.errorCode import ERROR, INVALID_CREDENTIALS,SUCCESS
import json
import os
class SignInWindow:    
    def __init__(self, controller, root):

        self.sysUsername = ""
        self.sysPassword = ""    
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(base_dir, "..", "config.json")
        with open(self.config_path, "r") as f:
            config = json.load(f)

            self.sysUsername = config["adminUsername"]
            self.sysPassword = config["adminPassword"]



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

        self.cancelButton = ctk.CTkButton(self.signInFormContainer, text="Change Password", command=self.changePassword, fg_color="green", text_color="white")
        self.cancelButton.grid(row=5, column=0, columnspan=2, padx=10, pady=5)


        # Set the grid weight to make the frame responsive
        self.signInWindowContainer.grid_rowconfigure(0, weight=1)
        self.signInWindowContainer.grid_columnconfigure(0, weight=1)
        self.signInFormContainer.grid_rowconfigure(0, weight=1)
        self.signInFormContainer.grid_columnconfigure(0, weight=1)  
        self.signInFormContainer.grid_columnconfigure(1, weight=1)


    def changePassword(self):
        self.modal = ctk.CTkToplevel(self.signInWindow)

        self.modal.title("Change Password")
        self.modal.geometry("400x300")
        self.modal.grab_set()  # Make it modal

        frame = ctk.CTkFrame(self.modal, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        old_password_label = ctk.CTkLabel(frame, text="Old password")
        old_password_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        old_password_entry = ctk.CTkEntry(frame, placeholder_text="Enter Old Password", width=200)
        old_password_entry.grid(row=0, column=1, padx=10, pady=10)


        label = ctk.CTkLabel(frame, text="New password")
        label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        new_password_entry = ctk.CTkEntry(frame, show="*", placeholder_text="Enter new password", width=200)
        new_password_entry.grid(row=1, column=1, padx=10, pady=10)

        confirm_label = ctk.CTkLabel(frame, text="Confirm password")
        confirm_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        confirm_password_entry = ctk.CTkEntry(frame, show="*", placeholder_text="Confirm new password", width=200)
        confirm_password_entry.grid(row=2, column=1, padx=10, pady=10)

        submit_button = ctk.CTkButton(self.modal, text="Submit", command=lambda: self.changePasswordValidation( old_password_entry.get(), new_password_entry.get(), confirm_password_entry.get()))
        submit_button.pack(pady=10)

        close_button = ctk.CTkButton(self.modal, text="Close", command=self.modal.destroy)
        close_button.pack(pady=5)

    def changePasswordValidation(self, oldPassword, newPassword, confirmPassword):
        if oldPassword == "" or newPassword == "" or confirmPassword == "":
            renderPopUpModal(self.signInWindow, "All fields are required", ERROR, ERROR)
            return False
        
        if security.sha256_hash(oldPassword) != self.sysPassword:
            renderPopUpModal(self.signInWindow, "Old password is incorrect", ERROR, ERROR)
            return False

        if newPassword != confirmPassword:
            renderPopUpModal(self.signInWindow,"New password and confirm password do not match", ERROR,ERROR)
            return False
        
        if len(newPassword) < 8:
            renderPopUpModal(self.signInWindow, "Password must be at least 8 characters long", ERROR,ERROR)
            return False
        
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)

            # Step 2: Modify the key you want
            config["adminPassword"] = security.sha256_hash(newPassword)

            # Step 3: Write it back to the file
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)

            self.sysPassword = security.sha256_hash(newPassword)  # Update the sysPassword in memory
            renderPopUpModal(self.signInWindow, "Password changed successfully", SUCCESS, SUCCESS)

            self.modal.destroy()

            return True
        except Exception as e:
            renderPopUpModal(self.signInWindow, f"Error changing password: {str(e)}", ERROR, ERROR)
            return False
    
    def validation(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        username = security.sha256_hash(username)
        password = security.sha256_hash(password)

        if username == self.sysUsername and password == self.sysPassword:
            print("Sign In Successful")
            # Close the sign-in window
            self.controller.setAdminAccess(True)
            print("Admin access: ", self.controller.getIsAdminAccess())

            self.signInWindow.destroy()
        else:
            self.errorLabel.configure(text=INVALID_CREDENTIALS)