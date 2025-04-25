import os
from pdfModule.pdfFunctions import openPdf
from Constant.fileKeywords import CONSENT_FORM_KEYWORD
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



def uploadCustomerFile():
    #check if foolder to store customer file exist 

    #If yes the get the path
    if os.path.exists("..\\..\\data\\attachment"):
        # Placeholder for actual implementation
        pass

    else:
        #if no create one and get the path


        os.makedirs("..\\..\\data\\attachment")
    
    
    pass