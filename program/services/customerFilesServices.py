import os
from pdfModule.pdfFunctions import openPdf
from Constant.fileKeywords import CONSENT_FORM_KEYWORD
import shutil
from Components.popupModal import renderPopUpModal
#CONSTANTs
attachment_path = "C:\\Users\\User\\Desktop\\YSL\\data\\attachment"


def customerHasConsentForm(customer_id):
    """
    Checks if a consent form file exists for a given customer ID
    within the data/attachment directory.

    Args:
        customer_id (str): The ID of the customer.

    Returns:
        bool: True if the consentForm file exists within the
              customer's ID folder, False otherwise.
    """
   
    customer_folder_path = os.path.join(attachment_path, customer_id)
    consent_form_filename = CONSENT_FORM_KEYWORD
    consent_form_path = os.path.join(customer_folder_path, f'{consent_form_filename}.pdf')
    print("consent_form_path")
    print(consent_form_path)
    # Check if the customer's ID folder exists
    if os.path.isdir(customer_folder_path):
        # If the folder exists, check if the consentForm file exists inside it
        if os.path.isfile(consent_form_path):
            return True
        else:
            return False
    else:
        return False
        
def viewCustomerFilePDF(customerId):
    """
    This function retrieves the customer consent form from the database.
    :return: The customer consent form.
    """

    # Go to the folder with customer ID
    #get the file with the name consentForm
    customer_folder_path = os.path.join(attachment_path, customerId)
    consent_form_filename = CONSENT_FORM_KEYWORD
    consent_form_path = os.path.join(customer_folder_path, f'{consent_form_filename}.pdf')

    print("Viewing customer file PDF")
    openPdf(consent_form_path)



def uploadCustomerFile(customer_id, filePath, root):
    #check if foolder to store customer file exist 
    customer_folder_path = os.path.join(attachment_path, customer_id)

    # if no folder storing customer file exist create one
    if not os.path.exists(customer_folder_path):
        os.makedirs(customer_folder_path)
    new_file_path = os.path.join(customer_folder_path, f'{CONSENT_FORM_KEYWORD}.pdf')
    
    #Save the file in the folder with the name consentForm
    try:
        shutil.copyfile(filePath, new_file_path)  # Copy the selected file to the target location
        renderPopUpModal(root, "File uploaded successfully", "Upload", "Success")
    except Exception as e:
        renderPopUpModal(root, "Error uploading file", "Upload", "Error")

        print(f"Error copying file: {e}")