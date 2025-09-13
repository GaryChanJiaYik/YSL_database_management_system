import tkinter as tk
from utils import center_popup_window

def renderPopUpModal(root , message, title, status):
    # Create a Toplevel window
    modal = tk.Toplevel(root)
    modal.title(title)
    
    popup_width, popup_height = 300, 150
    center_popup_window(modal, root, popup_width, popup_height)

    # Keep popup on top
    modal.transient(root)
    # Make it modal
    modal.grab_set()

    # Add a label and close button
    label = tk.Label(modal, text=message)
    label.pack(pady=20)

    close_button = tk.Button(modal, text="Close", command=modal.destroy)
    close_button.pack(pady=10)


def renderChoiceModal(root, title, message, choices=None):
    if not choices:
        raise ValueError("You must provide at least one choice.")

    response = {'value': None}

    modal = tk.Toplevel(root)
    modal.title(title)
    popup_width, popup_height = 300, 150 + 5 * len(choices)
    center_popup_window(modal, root, popup_width, popup_height)

    modal.transient(root)
    modal.grab_set()

    label = tk.Label(modal, text=message, wraplength=280, justify="center")
    label.pack(pady=20)

    btn_frame = tk.Frame(modal)
    btn_frame.pack(pady=10)

    for choice in choices:
        def handler(value=choice):
            response['value'] = value
            modal.destroy()

        btn = tk.Button(btn_frame, text=choice, width=12, command=handler)
        btn.pack(side="left", padx=5)

    modal.wait_window()
    return response['value']
