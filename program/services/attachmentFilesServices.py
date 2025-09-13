import os
import platform
import subprocess
import shutil
from Components.popupModal import renderPopUpModal, renderChoiceModal
from tkinter.filedialog import askopenfilenames, askdirectory
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


def handleAttachmentUpload(customer_id, root, attachment_type, entity_id=None):
        upload_option = ["Folder", "Files"]
        choice = renderChoiceModal(
            root, 
            title="Select Upload Type", 
            message="What would you like to upload?", 
            choices=upload_option)
        all_success = True

        if choice == "Files":
            file_paths = askopenfilenames(
                title="Select files to upload",
                filetypes=[
                    ("All Files", "*.*"),
                    ("ZIP Files", "*.zip"),
                    ("PDF Files", "*.pdf"),
                    ("Images", "*.jpg *.jpeg *.png"),
                ]
            )
            if not file_paths:
                return
            
            for filePath in file_paths:
                result = saveAttachmentFile(customer_id, filePath, attachment_type, entity_id)
                if result != SUCCESS:
                    all_success = False

        elif choice == "Folder":
            folder_path = askdirectory(title="Select folder to upload")
            if not folder_path:
                return
            
            result = saveAttachmentFolder(customer_id, folder_path, attachment_type, entity_id)
            if result != SUCCESS:
                all_success = False
        else:
            return
        
        if all_success:
            renderPopUpModal(root, f"All {choice} uploaded successfully", "Upload", "Success")
        else:
            renderPopUpModal(root, f"Some {choice} failed to upload", "Upload", "Warning")


def saveAttachmentFile(customer_id, file_path, attachment_type, entity_id=None, relative_path=None):
    if not file_path:
        return ERROR  # No file, silently return

    fileNameWithExtension = os.path.basename(file_path)
    fileNameWithoutExtension, extension = os.path.splitext(fileNameWithExtension)

    # Base folder path
    if entity_id:
        base_folder_path = os.path.join(attachment_path, customer_id, attachment_type, entity_id)
    else:
        base_folder_path = os.path.join(attachment_path, customer_id, attachment_type)

    # If relative_path is given (for folders), append its directory structure
    if relative_path:
        relative_folder = os.path.dirname(relative_path)
        customer_folder_path = os.path.join(base_folder_path, relative_folder)
    else:
        customer_folder_path = base_folder_path

    # Create the directory if it doesn't exist
    os.makedirs(customer_folder_path, exist_ok=True)

    # Handle file name conflicts with auto-increment
    counter = 1
    new_file_path = os.path.join(customer_folder_path, fileNameWithExtension)
    while os.path.exists(new_file_path):
        new_file_name = f"{fileNameWithoutExtension} ({counter}){extension}"
        new_file_path = os.path.join(customer_folder_path, new_file_name)
        counter += 1

    # Copy the file
    try:
        shutil.copyfile(file_path, new_file_path)
        return SUCCESS
    except Exception as e:
        print(f"Error copying file: {e}")
        return ERROR


def saveAttachmentFolder(customer_id, file_path, attachment_type, entity_id=None):
    parent_dir = os.path.dirname(file_path.rstrip(os.sep))  # Parent directory of folder_path
    base_len = len(parent_dir) + 1  # +1 to include the path separator

    all_success = True
    for root_dir, _, files in os.walk(file_path):
        for file in files:
            full_path = os.path.join(root_dir, file)
            relative_path = full_path[base_len:]  # includes the top folder name now
            success = saveAttachmentFile(
                customer_id,
                full_path,
                attachment_type,
                entity_id=entity_id,
                relative_path=relative_path
            )
            if success != SUCCESS:
                all_success = False

    return SUCCESS if all_success else ERROR


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