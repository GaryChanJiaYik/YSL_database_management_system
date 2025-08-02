import customtkinter as ctk
from PIL import Image
from windows.conditionDetailsView import ConditionDetailsView
from services.conditionDbFunctions import getTreatmentStatus
from Constant.treatmentDatabaseFunctions import getConditionTotalCost
from Constant.appConstant import GREEN, RED
from utils import resource_path


def handleConditionBlockEditClick(controller):
        print("Edit CondtionBlock")

def instantiateConditionModelBlock(parentFrame, conditionModel, column, row, openConditionDetailsWindowCallback, openEditConditionDetailsWindowCallback):
    # Invisible parent frame to add vertical margin
    wrapperFrame = ctk.CTkFrame(master=parentFrame, bg_color="transparent", fg_color="transparent")
    wrapperFrame.grid(column=column, row=row, sticky="ew", pady=10)  # Use sticky="ew" here
    wrapperFrame.grid_columnconfigure(0, weight=1)  # Make column expandable

    # Actual condition block inside the wrapper
    conditionFrame = ctk.CTkFrame(master=wrapperFrame, bg_color="transparent", corner_radius=10)
    conditionFrame.grid(row=0, column=0, sticky="ew")  # Expand to full width of wrapper
    conditionFrame.grid_columnconfigure(0, weight=2)
    conditionFrame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(
        conditionFrame,
        text=conditionModel.conditionDate,
        bg_color='transparent',
        font=('Arial', 16),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", padx=(20, 10), pady=5)

    conditionModel.undergoingTreatment = not getTreatmentStatus(conditionModel.customerId, conditionModel.conditionId)
    if conditionModel.undergoingTreatment:
        textColor = RED
        font = ("Arial", 16, "bold")
    else:
        textColor = GREEN
        font = ("Arial", 16)

    ctk.CTkLabel(
        conditionFrame,
        text="Undergoing" if conditionModel.undergoingTreatment else "Treated",
        bg_color='transparent',
        text_color=textColor,
        font=font,
        anchor="e",
        width=180
    ).grid(row=0, column=1, sticky="e", padx=(10, 20), pady=5)

    conditionSubFrame = ctk.CTkFrame(master=conditionFrame, bg_color="transparent", fg_color="transparent")
    conditionSubFrame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(10, 5), pady=5)
    conditionSubFrame.grid_columnconfigure(0, weight=0)

    ctk.CTkLabel(
        conditionSubFrame,
        text=conditionModel.conditionDescription,
        bg_color='transparent',
        font=('Arial', 16),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)


    detailSubFrame = ctk.CTkFrame(master=conditionFrame, bg_color="transparent", fg_color="transparent")
    detailSubFrame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(10, 5), pady=5)
    detailSubFrame.grid_columnconfigure(0, weight=1)
    detailSubFrame.grid_columnconfigure(1, weight=0)
    detailSubFrame.grid_columnconfigure(2, weight=0)
    
    # Total Label
    ctk.CTkLabel(
        master=detailSubFrame,
        text=f"Total: RM{getConditionTotalCost(conditionModel.conditionId):.2f}",
        bg_color='transparent',
        font=('Arial', 16),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)
    
    buttonFrame = ctk.CTkFrame(master=detailSubFrame, bg_color="transparent", fg_color="transparent")
    buttonFrame.grid(row=0, column=2, sticky="e", padx=(0, 5), pady=5)
    
    # Edit condition button
    try:
        image_path = resource_path("program\\asset\\icons\\edit.png")
        button_image = Image.open(image_path)
        resized_image = button_image.resize((15, 15)) # Resize if needed
        ctk_button_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image)
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        ctk_button_image = None # Handle the case where the image is not found
        
    ctk.CTkButton(
        buttonFrame,
        text="Edit",
        #image=ctk_button_image,
        width=28,
        height=28,
        command=lambda: openEditConditionDetailsWindowCallback(cm=conditionModel),
    ).grid(row=0, column=0, padx=(0, 5))
    
    # View Details Button
    ctk.CTkButton(
        buttonFrame,
        text="View Details",
        command=lambda: openConditionDetailsWindowCallback(cm=conditionModel),
    ).grid(row=0, column=1)