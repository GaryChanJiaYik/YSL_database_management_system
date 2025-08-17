from utils import resourcePath
from pathlib import Path

APP_NAME = "Patient Care Patient Good"

STANDARD_WINDOW_WIDTH = 900
STANDARD_WINDOW_HEIGHT = 600
STANDARD_WINDOW_SIZE = f'{STANDARD_WINDOW_WIDTH}x{STANDARD_WINDOW_HEIGHT}' #widthxheight
STANDARD_TEXT_BOX_WIDTH = 450
STANDARD_TEXT_BOX_HEIGHT = 100
TREATMENT_DESCRIPTION_CHARACTER_LIMIT = 400


#window name constant
WINDOW_LANDING = "LandingWindow"
WINDOW_CUSTOMER_DETAIL = "CustomerDetailWindow"
WINDOW_CONDITION_DETAIL = "ConditionDetailWindow"
WINDOW_TREATMENT_DETAIL = "TreatmentDetailWindow"
WINDOW_ADD_TREATMENT = "AddTreatmentWindow"
WINDOW_EDIT_TREATMENT = "EditTreatmentWindow"
WINDOW_EDIT_CONDITION = "EditConditionWindow"
WINDOW_ADD_CUSTOMER = "AddCustomerWindow"
WINDOW_EDIT_CUSTOMER = "EditCustomerWindow"


#color
BLUE = "#1f6aa5"
RED = "#E74C3C"
GREEN = "#27AE60"

#font design
FONT_FAMILY = 'Arial'
FONT = {
    "HEADER": (FONT_FAMILY, 18, 'bold'),
    "LABEL": (FONT_FAMILY, 13, 'bold'),
    "CONTENT": (FONT_FAMILY, 13)
}


# CSV path
DB_PATH = {
    "MAIN": Path(resourcePath('./data/db.csv')),
    "CONDITION": Path(resourcePath('./data/conditionDb.csv')),
    "TREATMENT": Path(resourcePath('./data/treatmentDb.csv')),
    "TREATMENT_REV": Path(resourcePath('./data/treatmentRevisionHistory.csv')),
}


# image path
IMG_PATH = {
    "EDIT": Path(resourcePath("program/asset/icons/edit.png"))
}
