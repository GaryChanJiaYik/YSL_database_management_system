import customtkinter as ctk
from windows.conditionDetailsView import ConditionDetailsView


def instantiateConditionModelBlock(parentFrame, conditionModel, column, row, openConditionDetailsWindowCallback):
    # Create a frame for the condition model block
    conditionFrame = ctk.CTkFrame(master=parentFrame, bg_color="transparent",fg_color="transparent", corner_radius=20)
    conditionFrame.grid_columnconfigure(0, weight=1)
    conditionFrame.grid(column=column, row=row, sticky="nsew")

    # Create a label for the condition model block
    ctk.CTkLabel(
        conditionFrame,
        text=conditionModel.conditionDate,  # Assuming conditionModel has a date attribute
        bg_color='transparent',  # Make the label background transparent
        font=('Arial', 16),
        anchor="w"  # Align text inside label to left
    ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)

    ctk.CTkLabel(
    conditionFrame,
        text="Undergoing Treatment" if conditionModel.undergoingTreatment else "",  # Assuming conditionModel has a date attribute
        bg_color='transparent',  # Make the label background transparent
        font=('Arial', 16),
        anchor="w"  # Align text inside label to left
    ).grid(row=0, column=1, sticky="w", padx=(10, 5), pady=5)

    conditionSubFrame = ctk.CTkFrame(master=conditionFrame, bg_color="transparent", fg_color="transparent")
    conditionSubFrame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=(10, 5), pady=5)

    # Set equal weight to both columns
    conditionSubFrame.grid_columnconfigure(0, weight=2)  # Label
    conditionSubFrame.grid_columnconfigure(1, weight=2) 
    conditionSubFrame.grid_columnconfigure(2, weight=0)  # Button stays tight

    # Label to the left (west)
    ctk.CTkLabel(
        conditionSubFrame,
        text=conditionModel.conditionDescription,
        bg_color='transparent',
        font=('Arial', 16),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)

    ctk.CTkLabel(
        conditionSubFrame,
        text=" ",
        width=100,
        bg_color='transparent',
    ).grid(row=0, column=1, sticky="w", padx=(0, 5), pady=5)


    # Button to the right (east)
    ctk.CTkButton(
        master=conditionSubFrame,
        text="View Details",
        command=lambda: openConditionDetailsWindowCallback(cm = conditionModel),
    ).grid(row=0, column=2, sticky="e", padx=(0, 5), pady=5)