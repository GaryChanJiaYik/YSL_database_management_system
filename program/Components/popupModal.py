import tkinter as tk

def renderPopUpModal(root , message, title, status):
        # Create a Toplevel window
    modal = tk.Toplevel(root)
    modal.title(title)
    modal.geometry("300x150")

    # Make it modal
    modal.grab_set()

    # Add a label and close button
    label = tk.Label(modal, text=message)
    label.pack(pady=20)

    close_button = tk.Button(modal, text="Close", command=modal.destroy)
    close_button.pack(pady=10)