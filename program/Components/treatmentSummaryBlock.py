import tkinter as tk
import customtkinter as ctk
from Constant.converterFunctions import getDatefromTimeStamp
from PIL import Image

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



def renderTreatmentSummaryBlockFunctionRevamp(parentContainer, treatmentModel, hideButtons=False, on_click_view=None, on_click=None, showEditButton=False,):
    # Margin container
    marginContainer = ctk.CTkFrame(master=parentContainer, height=90, width=500, corner_radius=10, fg_color="transparent")

    # Wrapper with border (customtkinter style)
    wrapperContainer = ctk.CTkFrame(
        master=marginContainer,
        height=80, width=500, corner_radius=10,
    )
    wrapperContainer.grid(sticky="ew", padx=10, pady=5)
    wrapperContainer.grid_columnconfigure(0, weight=2)
    wrapperContainer.grid_columnconfigure(1, weight=1)
    wrapperContainer.grid_columnconfigure(2, weight=2)
    wrapperContainer.grid_columnconfigure(3, weight=1)
    
    treatmentDetailContainer = ctk.CTkFrame(master=wrapperContainer, fg_color="transparent", height=80, width=350)
    treatmentDetailContainer.grid(row=0, column=0, sticky="nw", padx=10)
    treatmentDetailContainer.grid_propagate(False)


    # Date label
    treatmentDateLabel = ctk.CTkLabel(
        master=treatmentDetailContainer,
        text=getDatefromTimeStamp(treatmentModel.treatmentDate),
        anchor="w"
    )
    treatmentDateLabel.grid(row=0, column=0, sticky="w")


    treatmentDescriptionLabel = ctk.CTkLabel(
        master=treatmentDetailContainer,
        text=treatmentModel.treatmentDescription,
        anchor="w"
    )
    treatmentDescriptionLabel.grid(row=1, column=0, sticky="w")


    treatmentDescriptionCost = ctk.CTkLabel(
        master=treatmentDetailContainer,
        text=f"Cost: RM {treatmentModel.treatmentCost:.2f}",
        anchor="w"
    )
    treatmentDescriptionCost.grid(row=2, column=0, sticky="w")

    #Space
    ctk.CTkLabel(
        master=wrapperContainer,
        text=" "
    ).grid(row=0, column=1, sticky="w")


    # Treatment levels container (right side)
    treatmentLevelsContainer = ctk.CTkFrame(master=wrapperContainer, fg_color="transparent", height=45, width=200)
    treatmentLevelsContainer.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="w", pady=5, padx=4) 

    create_level_cell_revamp(treatmentLevelsContainer, 0, 0, "Pain", treatmentModel.painLevel)
    create_level_cell_revamp(treatmentLevelsContainer, 1, 0, "Tense", treatmentModel.tenseLevel)
    create_level_cell_revamp(treatmentLevelsContainer, 0, 1, "Sore", treatmentModel.soreLevel)
    create_level_cell_revamp(treatmentLevelsContainer, 1, 1, "Numb", treatmentModel.numbLevel)

    if not hideButtons:
        # Edit treatment button
        editButtonFrame = ctk.CTkFrame(master=wrapperContainer,  width=250, height=50, fg_color="transparent")
        editButtonFrame.grid(row=0, column=3,  rowspan=2, columnspan=1, sticky="nsew", pady=5, padx=4)
        editButtonFrame.grid_propagate(False)


        #Get the image
        try:
            image_path = "program\\asset\\icons\\edit.png"
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


    # Click binding
    if on_click:
        marginContainer.bind("<Button-1>", lambda e: on_click(treatmentModel))

    return marginContainer 