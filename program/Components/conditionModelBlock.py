import customtkinter as ctk
from windows.conditionDetailsView import ConditionDetailsView


def instantiateConditionModelBlock(parentFrame, conditionModel, column, row, openConditionDetailsWindowCallback):
    # Invisible parent frame to add vertical margin
    wrapperFrame = ctk.CTkFrame(master=parentFrame, bg_color="transparent", fg_color="transparent")
    wrapperFrame.grid(column=column, row=row, sticky="ew", pady=10)  # Use sticky="ew" here
    wrapperFrame.grid_columnconfigure(0, weight=1)  # Make column expandable

    # Actual condition block inside the wrapper
    conditionFrame = ctk.CTkFrame(master=wrapperFrame, bg_color="transparent", corner_radius=10)
    conditionFrame.grid_columnconfigure(0, weight=1)
    conditionFrame.grid(row=0, column=0, sticky="ew")  # Expand to full width of wrapper

    ctk.CTkLabel(
        conditionFrame,
        text=conditionModel.conditionDate,
        bg_color='transparent',
        font=('Arial', 16),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", padx=(20, 10), pady=5)

    ctk.CTkLabel(
        conditionFrame,
        text="Undergoing Treatment" if conditionModel.undergoingTreatment else "",
        bg_color='transparent',
        font=('Arial', 16),
        anchor="w"
    ).grid(row=0, column=1, sticky="w", padx=(20, 10), pady=5)

    conditionSubFrame = ctk.CTkFrame(master=conditionFrame, bg_color="transparent", fg_color="transparent")
    conditionSubFrame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=(10, 5), pady=5)

    conditionSubFrame.grid_columnconfigure(0, weight=2)
    conditionSubFrame.grid_columnconfigure(1, weight=2)
    conditionSubFrame.grid_columnconfigure(2, weight=0)

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

    ctk.CTkButton(
        master=conditionSubFrame,
        text="View Details",
        command=lambda: openConditionDetailsWindowCallback(cm=conditionModel),
    ).grid(row=0, column=2, sticky="e", padx=(0, 5), pady=5)
