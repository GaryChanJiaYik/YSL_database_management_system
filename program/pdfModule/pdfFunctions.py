
import webbrowser

def openPdf(filePath):
    """
    Open a PDF file and return the file object.
    """
    try:
        webbrowser.open_new(filePath)

    except FileNotFoundError:
        print(f"File not found: {filePath}")
        return None
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return None