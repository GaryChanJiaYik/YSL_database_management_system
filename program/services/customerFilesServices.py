import os
from pdfModule.pdfFunctions import openPdf
from Constant.fileKeywords import CONSENT_FORM_KEYWORD
import shutil
from Components.popupModal import renderPopUpModal
from tkinter.filedialog import askopenfilename
import glob
from Constant.errorCode import ERROR, SUCCESS
#CONSTANTs
attachment_path = os.path.join(os.getcwd(), "data", "attachment")


def customerHasConsentForm(customer_id, attachment_type):
    """
    Checks if a consent form file exists for a given customer ID
    within the data/attachment directory.

    Args:
        customer_id (str): The ID of the customer.

    Returns:
        bool: True if the consentForm file exists within the
              customer's ID folder, False otherwise.
    """
   
    customer_folder_path = os.path.join(attachment_path, customer_id, attachment_type)
    consent_form_filename = CONSENT_FORM_KEYWORD
    consent_form_path = os.path.join(customer_folder_path, f'{consent_form_filename}.pdf')
    print(f"consent_form_path: {consent_form_path}")
    # Check if the customer's ID folder exists
    if os.path.isdir(customer_folder_path):
        # If the folder exists, check if the consentForm file exists inside it
        if os.path.isfile(consent_form_path):
            return True
        else:
            return False
    else:
        return False
        
def viewCustomerFilePDF(customerId, attachmentType):
    """
    This function retrieves the customer consent form from the database.
    :return: The customer consent form.
    """

    # Go to the folder with customer ID
    #get the file with the name consentForm
    customer_folder_path = os.path.join(attachment_path, customerId, attachmentType)
    consent_form_filename = CONSENT_FORM_KEYWORD
    consent_form_path = os.path.join(customer_folder_path, f'{consent_form_filename}.pdf')

    print("Viewing customer file PDF")
    openPdf(consent_form_path)


def uploadCustomerFile(customer_id, filePath, root, fileName, attachmentType):
    if not filePath:
        return ERROR  # No file, silently return

    _, extension = os.path.splitext(filePath)

    #check if foolder to store customer file exist 
    if fileName is not CONSENT_FORM_KEYWORD:
        customer_folder_path = os.path.join(attachment_path, customer_id, attachmentType, fileName)
    else:
        customer_folder_path = os.path.join(attachment_path, customer_id, attachmentType)

    # if no folder storing customer file exist create one
    if not os.path.exists(customer_folder_path):
        os.makedirs(customer_folder_path)

    new_file_path = os.path.join(customer_folder_path, f'{fileName}{extension}')
    
    #Save the file in the folder with the name consentForm
    try:
        shutil.copyfile(filePath, new_file_path)  # Copy the selected file to the target location
        renderPopUpModal(root, "File uploaded successfully", "Upload", "Success")
        return SUCCESS
    except Exception as e:
        renderPopUpModal(root, "Error uploading file", "Upload", "Error")
        print(f"Error copying file: {e}")
        return ERROR


def getConditionPicturePath(customerId, conditionId, attachmentType):
    """
    This function retrieves the condition picture path for a given customer ID and condition ID.
    :param customerId: The ID of the customer.
    :param conditionId: The ID of the condition.
    :return: The path to the condition picture.
    """
    customer_folder_path = os.path.join(attachment_path, customerId, attachmentType, conditionId)
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.webp')

    # Find all files starting with conditionId and any extension
    pattern = os.path.join(customer_folder_path, f"{conditionId}.*")
    matches = glob.glob(pattern)

    # Filter only image files
    for file_path in matches:
        if file_path.lower().endswith(allowed_extensions):
            return file_path

    return None


def getTreatmentPicturePath(customerId, treatmentId, attachmentType):
    """
    Retrieves the treatment picture path for a given customer ID and treatment ID.
    :param customerId: The ID of the customer.
    :param treatmentId: The ID of the treatment.
    :return: The path to the treatment picture or None.
    """
    customer_folder_path = os.path.join(attachment_path, customerId, attachmentType, treatmentId)
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.webp')

    # Find all files starting with treatmentId and any extension
    pattern = os.path.join(customer_folder_path, f"{treatmentId}.*")
    matches = glob.glob(pattern)

    for file_path in matches:
        if file_path.lower().endswith(allowed_extensions):
            return file_path

    return None


def renderFilePicker(pdefaultextension, pfiletypes, ptitle=""):
    """
    This function renders a file picker dialog to select a file.
    :return: The path of the selected file.
    """
    file_path = askopenfilename(defaultextension=pdefaultextension, filetypes=pfiletypes, title=ptitle)
    return file_path


def deleteCustomerFile(customer_id, file_keyword, attachmentType):
    possible_extensions = ['.pdf']  # Stick with this if you want future flexibility
    customer_folder_path = os.path.join(attachment_path, customer_id, attachmentType)

    for ext in possible_extensions:
        file_path = os.path.join(customer_folder_path, f'{file_keyword}{ext}')
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
    return False