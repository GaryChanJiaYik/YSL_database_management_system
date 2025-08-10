import tkinter as tk
from utils import center_popup_window

def renderPopUpModal(root , message, title, status):
        # Create a Toplevel window
    modal = tk.Toplevel(root)
    modal.title(title)
    
    popup_width, popup_height = 300, 150
    center_popup_window(modal, root, popup_width, popup_height)

    # Make it modal
    modal.grab_set()

    # Add a label and close button
    label = tk.Label(modal, text=message)
    label.pack(pady=20)

    close_button = tk.Button(modal, text="Close", command=modal.destroy)
    close_button.pack(pady=10)