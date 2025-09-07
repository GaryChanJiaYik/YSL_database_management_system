import os
import platform
import subprocess
import shutil
from Components.popupModal import renderPopUpModal
from Constant.errorCode import ERROR, SUCCESS
#CONSTANTs
attachment_path = os.path.join(os.getcwd(), "data", "attachment")

def HasAttachment(customer_id, attachment_type, entity_id=None):
    """
    Checks if any attachment file exists for a given customer ID
    within the data/attachment directory.

    Args:
        customer_id (str): The ID of the customer.

    Returns:
        bool: True if any attachment file exists within the
              customer's ID folder, False otherwise.
    """
    if entity_id:
        customer_folder_path = os.path.join(attachment_path, customer_id, attachment_type, entity_id)
    else:
        customer_folder_path = os.path.join(attachment_path, customer_id, attachment_type)

    # Check if the customer's ID folder exists
    if os.path.isdir(customer_folder_path):
        # If the folder exists, check if there are any files inside it
        if os.listdir(customer_folder_path):
            return True
        else:
            return False
    else:
        return False


def uploadAttachmentFile(customer_id, filePath, root, attachment_type, entity_id=None):
    if not filePath:
        return ERROR  # No file, silently return

    fileNameWithExtension = os.path.basename(filePath)
    fileNameWithoutExtension, extension = os.path.splitext(fileNameWithExtension)

    #check if foolder to store customer file exist
    if entity_id:
        customer_folder_path = os.path.join(attachment_path, customer_id, attachment_type, entity_id)
    else:
        customer_folder_path = os.path.join(attachment_path, customer_id, attachment_type)

    # if no folder storing customer file exist create one
    if not os.path.exists(customer_folder_path):
        os.makedirs(customer_folder_path)

    # Handle auto-increment to avoid overwriting
    counter = 1
    new_file_path = os.path.join(customer_folder_path, f'{fileNameWithExtension}')
    
    while os.path.exists(new_file_path):
        new_file_name = f"{fileNameWithoutExtension} ({counter}){extension}"
        new_file_path = os.path.join(customer_folder_path, new_file_name)
        counter += 1
        
    #Save the file in the folder with the name consentForm
    try:
        shutil.copyfile(filePath, new_file_path)  # Copy the selected file to the target location
        return SUCCESS
    except Exception as e:
        print(f"Error copying file: {e}")
        return ERROR


def openAttachmentDirectory(customerId, root, attachment_type, entity_id=None):
    # Build the path to the customer's attachment folder
    if entity_id:
        customer_folder_path = os.path.join(attachment_path, customerId, attachment_type, entity_id)
    else:
        customer_folder_path = os.path.join(attachment_path, customerId, attachment_type)

    # Make sure the folder exists
    if not os.path.exists(customer_folder_path):
        renderPopUpModal(root, "This customer has no attachments yet.", "Not Found", "Error")
        return

    try:
        if platform.system() == "Windows":
            os.startfile(customer_folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", customer_folder_path])
        else:  # Linux and others
            subprocess.Popen(["xdg-open", customer_folder_path])
    except Exception as e:
        renderPopUpModal(root, f"Could not open folder: {str(e)}", "Not Found", "Error")