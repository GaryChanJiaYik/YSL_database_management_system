import tkinter as tk
import customtkinter as ctk
import json
from datetime import datetime
from Constant.converterFunctions import getDatefromTimeStamp
from PIL import Image
from utils import bindClickEventRecursively, bindHoverEventRecursively
from services.customerFilesServices import renderFilePicker, uploadCustomerFile
from Components.popupModal import renderPopUpModal
from Constant.errorCode import SUCCESS
from Constant.appConstant import IMG_PATH


def create_level_cell(parent, row, col, label_text, value_text):
    container = tk.Frame(parent, padx=5, pady=5)
    container.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    label = tk.Label(container, text=label_text, font=('Arial', 9), anchor="w")
    label.grid(row=0, column=0, sticky="w")

    value = tk.Label(container, text=value_text, font=('Arial', 9), anchor="w")
    value.grid(row=1, column=0, sticky="w")


def create_level_cell_revamp(parent, row, col, label_text, value_text):
    container = ctk.CTkFrame(parent, corner_radius=0, height=40, width=40, fg_color="transparent")
    container.grid_propagate(False)
    container.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    label = ctk.CTkLabel(container, text=label_text, font=('Arial', 12), height=16, width=40, anchor="center")
    label.grid(row=0, column=0, sticky="nsew")

    value = ctk.CTkLabel(container, text=value_text, font=('Arial', 12), height=16,width=40, anchor="center")
    value.grid(row=1, column=0, sticky="nsew")


def renderTreatmentSummaryBlockFunction(parentContainer, treatmentModel, on_click=None):
    marginContainer = tk.Frame(parentContainer, pady=2)
    wrapperContainer = tk.Frame(marginContainer, highlightbackground='black', highlightthickness=1)
    wrapperContainer.grid_columnconfigure(0, weight=1)

    treatmentDetailContainer = tk.Frame(wrapperContainer, padx=15, pady=1) 

    treatmentDescriptionLabel = tk.Label(treatmentDetailContainer, text=treatmentModel.treatmentDescription, font=('Arial', 9), anchor="w")
    treatmentDescriptionLabel.grid(row=1, column=0, sticky="w") 

    treatmentDateLabel = tk.Label(treatmentDetailContainer, text=treatmentModel.treatmentDate, font=('Arial', 9), anchor="w")
    treatmentDateLabel.grid(row=2, column=0, sticky="w") 

    treatmentDetailContainer.grid(row=0, column=0, sticky="w")

    treatmentLevelsContainer = tk.Frame(wrapperContainer,)
    treatmentLevelsContainer.grid(row=0, column=1, rowspan=3, columnspan=2, sticky="w",) 

    # Levels Container
    create_level_cell(treatmentLevelsContainer, 0, 0, "Pain", treatmentModel.painLevel)
    create_level_cell(treatmentLevelsContainer, 1, 0, "Tense", treatmentModel.tenseLevel)
    create_level_cell(treatmentLevelsContainer, 0, 1, "Sore", treatmentModel.soreLevel)
    create_level_cell(treatmentLevelsContainer, 1, 1, "Numb", treatmentModel.numbLevel)

    if on_click:
        marginContainer.bind("<Button-1>", lambda e: on_click(treatmentModel))
        # Also bind children to make sure the whole area is clickable
        for child in marginContainer.winfo_children():
            child.bind("<Button-1>", lambda e: on_click(treatmentModel))


    wrapperContainer.grid(row=0, column=0, sticky="w")
    return marginContainer


def handleUploadTreatmentPicture(treatmentModel, parentContainer):
    filePath = renderFilePicker(
        pdefaultextension='',
        pfiletypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("All files", "*.*")
        ],
        ptitle="Select a treatment picture"
    )

    if not filePath:
        return  # User canceled

    result = uploadCustomerFile(treatmentModel.customerId, filePath, parentContainer, treatmentModel.treatmentID)

    if result == SUCCESS:
        renderPopUpModal(
            title="Upload Successful",
            message=f"Successfully uploaded treatment picture for Treatment ID: {treatmentModel.treatmentID}"
        )
    else:
        renderPopUpModal(
            title="Upload Failed",
            message=f"Failed to upload treatment picture for Treatment ID: {treatmentModel.treatmentID}. Please try again."
        )


def renderTreatmentSummaryBlockFunctionRevamp(parentContainer, treatmentModel, isHiddenAccess, hideButtons=False, on_click_view=None, on_click=None, on_click_report=None, showEditButton=False,row_index=0, customerModel=None, conditionModel=None):
    def _on_enter(event):
        wrapperContainer.configure(border_width=2)  # Show border

    def _on_leave(event):
        wrapperContainer.configure(border_width=0)  # Hide border
    
    row_bg_color = (
        ["#f1f5f9", "#1f2937"] if row_index % 2 == 0 else ["#ffffff", "#111827"]
    )
    
    # Margin container
    marginContainer = ctk.CTkFrame(master=parentContainer, height=90, width=500, corner_radius=10, fg_color="transparent")

    # Wrapper with border (customtkinter style)
    wrapperContainer = ctk.CTkFrame(
        master=marginContainer,
        height=80, width=500, corner_radius=10,
        fg_color=row_bg_color
    )
    wrapperContainer.grid(sticky="ew", padx=10, pady=5)
    # Change the cursor to indicate it's clickable
    wrapperContainer.configure(cursor="hand2")
    wrapperContainer.grid_columnconfigure(0, weight=2)
    wrapperContainer.grid_columnconfigure(1, weight=1)
    wrapperContainer.grid_columnconfigure(2, weight=2)
    wrapperContainer.grid_columnconfigure(3, weight=2)
    wrapperContainer.grid_columnconfigure(4, weight=1)
    
    treatmentDetailContainer = ctk.CTkFrame(master=wrapperContainer, fg_color="transparent", height=125, width=350)
    treatmentDetailContainer.grid(row=0, column=0, sticky="nw", padx=12, pady=5)
    treatmentDetailContainer.grid_propagate(False)


    # Date label
    treatmentDateLabel = ctk.CTkLabel(
        master=treatmentDetailContainer,
        text=getDatefromTimeStamp(treatmentModel.treatmentDate),
        font=('Arial', 13, "bold"),
        anchor="w"
    )
    treatmentDateLabel.grid(row=0, column=0, sticky="w")


    treatmentDescriptionLabel = ctk.CTkLabel(
        master=treatmentDetailContainer,
        text=treatmentModel.treatmentDescription,
        font=('Arial', 13),
        anchor="w"
    )
    treatmentDescriptionLabel.grid(row=1, column=0, sticky="w")

    # Next Appointment Date
    appointment_date_str = ""
    if treatmentModel.appointmentDate:
        try:
            dt = datetime.strptime(treatmentModel.appointmentDate, "%Y-%m-%d %H:%M:%S")
            appointment_date_str = dt.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            print("Failed to parse appointmentDate:", e)
            appointment_date_str = treatmentModel.appointmentDate  # fallback

    appointmentDateLabel = ctk.CTkLabel(
        master=treatmentDetailContainer,
        text=f"Next Appointment: {appointment_date_str or "N/A"}",
        font=('Arial', 13, "italic"),
        anchor="w",
        text_color="#C2C2C2"  # subtle color for appointment
    )
    appointmentDateLabel.grid(row=2, column=0, sticky="w")

    if isHiddenAccess:
        cost_value = treatmentModel.treatmentCost
        try:
            if isinstance(cost_value, (float, int)):
                # Just show amount with no payment type
                cost_display = f"RM {cost_value:.2f}"
            elif isinstance(cost_value, str):
                try:
                    payment_data = json.loads(cost_value)
                    if isinstance(payment_data, dict):
                        payment_strings = [
                            f"RM {float(amount):.2f} ({method})" for method, amount in payment_data.items()
                        ]
                        cost_display = ", ".join(payment_strings)
                    else:
                        # JSON parsed but not a dict - just show amount only
                        cost_display = f"RM {float(payment_data):.2f}"
                except (json.JSONDecodeError, TypeError, ValueError):
                    # Not JSON, try parse as float string - just show amount only
                    amount = float(cost_value)
                    cost_display = f"RM {amount:.2f}"
            else:
                cost_display = "RM 0.00"
        except Exception:
            cost_display = "RM 0.00"

        treatmentDescriptionCost = ctk.CTkLabel(
            master=treatmentDetailContainer,
            text=f"Fee: {cost_display}",
            font=('Arial', 13, "bold"),
            anchor="w"
        )
        treatmentDescriptionCost.grid(row=3, column=0, sticky="w")


    #Space
    ctk.CTkLabel(
        master=wrapperContainer,
        text=" "
    ).grid(row=0, column=1, sticky="w")


    # Treatment levels container
    # Treament levels container left
    treatmentLevelsContainerLeft = ctk.CTkFrame(master=wrapperContainer, fg_color="transparent")
    treatmentLevelsContainerLeft.grid(row=0, column=2, rowspan=1, sticky="w", pady=5, padx=4)
    treatmentLevelsContainerLeft.grid_columnconfigure((0, 1, 2), weight=1)

    beforeLabel = ctk.CTkLabel(
        master=treatmentLevelsContainerLeft,
        text="Before",
        font=('Arial', 13, "bold"),
        anchor="center"
    )
    beforeLabel.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 5))
    
    create_level_cell_revamp(treatmentLevelsContainerLeft, 1, 0, "Pain", treatmentModel.painLevel)
    create_level_cell_revamp(treatmentLevelsContainerLeft, 2, 0, "Tense", treatmentModel.tenseLevel)
    create_level_cell_revamp(treatmentLevelsContainerLeft, 1, 1, "Sore", treatmentModel.soreLevel)
    create_level_cell_revamp(treatmentLevelsContainerLeft, 2, 1, "Numb", treatmentModel.numbLevel)

    # treament levels container right
    treatmentLevelsContainerRight = ctk.CTkFrame(master=wrapperContainer, fg_color="transparent")
    treatmentLevelsContainerRight.grid(row=0, column=3, rowspan=1, sticky="w", pady=5, padx=4)
    treatmentLevelsContainerRight.grid_columnconfigure((0, 1, 2), weight=1)
    afterLabel = ctk.CTkLabel(
        master=treatmentLevelsContainerRight,
        text="After",
        font=('Arial', 13, "bold"),
        anchor="center"
    )
    afterLabel.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 5))
    
    create_level_cell_revamp(treatmentLevelsContainerRight, 1, 0, "Pain", treatmentModel.painLevelAfter or "0")
    create_level_cell_revamp(treatmentLevelsContainerRight, 2, 0, "Tense", treatmentModel.tenseLevelAfter or "0")
    create_level_cell_revamp(treatmentLevelsContainerRight, 1, 1, "Sore", treatmentModel.soreLevelAfter or "0")
    create_level_cell_revamp(treatmentLevelsContainerRight, 2, 1, "Numb", treatmentModel.numbLevelAfter or "0")
    
    
    if not hideButtons:
        # Edit treatment button
        editButtonFrame = ctk.CTkFrame(master=wrapperContainer,  width=250, height=50, fg_color="transparent")
        editButtonFrame.grid(row=0, column=4,  rowspan=2, columnspan=1, sticky="nsew", pady=5, padx=4)
        editButtonFrame.grid_propagate(False)

        bindClickEventRecursively(wrapperContainer, lambda event: on_click_view(treatmentModel))
        bindHoverEventRecursively(wrapperContainer, _on_enter, _on_leave)

        #Get the image
        try:
            image_path = IMG_PATH["EDIT"]
            button_image = Image.open(image_path)
            resized_image = button_image.resize((20, 20)) # Resize if needed
            ctk_button_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image)
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            ctk_button_image = None # Handle the case where the image is not found

        if ctk_button_image:
            button = ctk.CTkButton(master=editButtonFrame,
                        width=100,
                        text="Edit",
                        image=ctk_button_image,
                        compound="right",  # Display image to the left of the text
                        command=lambda: on_click(treatmentModel))
            button.place(relx=0.25, rely=0.5, anchor=ctk.CENTER)

        else:
            # Create a button without an image if the image loading failed
            button = ctk.CTkButton(
                    master=editButtonFrame,
                    width=100,
                    text="Edit",
                    command=lambda: on_click(treatmentModel))
            button.place(relx=0.25, rely=0.5, anchor=ctk.CENTER)

        viewButton = ctk.CTkButton(
                    master=editButtonFrame,
                    width=80,
                    text="View",
                    fg_color='green',
                    command=lambda: on_click_view(treatmentModel))
        viewButton.place(relx=0.65, rely=0.5, anchor=ctk.CENTER)
        #viewButtonFrame.grid_propagate(False)
        
        # Upload Treatment Picture Button
        # uploadButton = ctk.CTkButton(
        #     master=editButtonFrame,
        #     width=120,
        #     text="Upload Picture",
        #     fg_color='green',
        #     command=lambda: handleUploadTreatmentPicture(treatmentModel, parentContainer)
        # )
        # uploadButton.place(relx=0.65, rely=0.5, anchor=ctk.CENTER)
        
        generateReportButton = ctk.CTkButton(
            master=editButtonFrame,
            width=140,
            text="Generate Report",
            fg_color='#6A5ACD',  
            hover_color='#144870',
            command=lambda: on_click_report(treatmentModel)
        )
        generateReportButton.place(relx=0.45, rely=0.75, anchor=ctk.CENTER)

    # # Click binding
    # if on_click:
    #     marginContainer.bind("<Button-1>", lambda e: on_click(treatmentModel))

    return marginContainer 
