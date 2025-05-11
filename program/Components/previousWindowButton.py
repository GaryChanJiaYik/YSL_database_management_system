import customtkinter as ctk

class PreviousWindowButton:

    def __init__(self, controller, parent):
        self.controller = controller
        backButton = ctk.CTkButton(
            parent,
            text="Back",
            command=self.back_previous_window,
            fg_color="red",
            text_color="white",
            hover_color="darkred",
        )

        backButton.grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=(10, 5),
            sticky="nsew",
        )

    def back_previous_window(self):
        self.controller.back_window()
