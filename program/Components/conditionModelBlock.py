import csv
import customtkinter as ctk
import Constant.dbColumn as dbCol
from windows.conditionDetailsView import ConditionDetailsView

DB_PATH = './data/treatmentDb.csv'

def instantiateConditionModelBlock(parentFrame, conditionModel, column, row, openConditionDetailsWindowCallback):
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

    ctk.CTkLabel(
        conditionFrame,
        text="Undergoing Treatment" if conditionModel.undergoingTreatment else "",
        bg_color='transparent',
        font=('Arial', 16),
        anchor="e"
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
    detailSubFrame.grid_columnconfigure(0, weight=2)
    detailSubFrame.grid_columnconfigure(1, weight=2)
    detailSubFrame.grid_columnconfigure(2, weight=0)
    
    ctk.CTkLabel(
        master=detailSubFrame,
        text=f"Total: RM{getConditionTotalCost(conditionModel.conditionId):.2f}",
        bg_color='transparent',
        font=('Arial', 16),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=5)
    
    ctk.CTkButton(
        detailSubFrame,
        text="View Details",
        command=lambda: openConditionDetailsWindowCallback(cm=conditionModel),
    ).grid(row=0, column=2, sticky="e", padx=(0, 5), pady=5)

def getConditionTotalCost(conditionId):
    total_cost = 0.0

    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)
        
        # Get the index of relevant columns
        condition_id_index = header.index(dbCol.conditionId)
        treatment_cost_index = header.index(dbCol.treatmentCost)

        # Loop through the CSV lines
        for line in csvFile:
            if line and line[condition_id_index] == conditionId:
                try:
                    total_cost += float(line[treatment_cost_index])
                except ValueError:
                    print(f"Invalid cost value: {line[treatment_cost_index]}")
    
    return total_cost