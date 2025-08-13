import os
import platform
import subprocess
import pathlib
import webbrowser

def openPdf(filePath):
    path = pathlib.Path(filePath).resolve()
    try:
        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.check_call(['open', path])
        else:  # Linux and others
            subprocess.check_call(['xdg-open', path])
    except Exception as e:
        print(f"Native open failed: {e}")
        try:
            file_url = path.as_uri()
            webbrowser.open(file_url)
            print("Opened PDF in browser as fallback.")
        except Exception as e2:
            print(f"Also failed to open PDF in browser: {e2}")


# import webbrowser

# def openPdf(filePath):
#     """
#     Open a PDF file and return the file object.
#     """
#     try:
#         webbrowser.open_new(filePath)

#     except FileNotFoundError:
#         print(f"File not found: {filePath}")
#         return None
#     except Exception as e:
#         print(f"An error occurred while opening the file: {e}")
#         return None