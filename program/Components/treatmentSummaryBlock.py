import tkinter as tk

def create_level_cell(parent, row, col, label_text, value_text):
    container = tk.Frame(parent, padx=5, pady=5)
    container.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    label = tk.Label(container, text=label_text, font=('Arial', 9), anchor="w")
    label.grid(row=0, column=0, sticky="w")

    value = tk.Label(container, text=value_text, font=('Arial', 9), anchor="w")
    value.grid(row=1, column=0, sticky="w")


def renderTreatmentSummaryBlockFunction(parentContainer, treatmentModel, on_click=None):
    marginContainer = tk.Frame(parentContainer, pady=2)
    wrapperContainer = tk.Frame(marginContainer, highlightbackground='black', highlightthickness=1)
    wrapperContainer.grid_columnconfigure(0, weight=1)

    treatmentDetailContainer = tk.Frame(wrapperContainer, padx=5, pady=5) 

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