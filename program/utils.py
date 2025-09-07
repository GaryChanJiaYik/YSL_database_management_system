import os
import sys
import customtkinter as ctk

def resourcePath(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def setEntryValue(entry_widget, value):
    entry_widget.configure(state="normal")
    entry_widget.delete(0, "end")
    entry_widget.insert(0, value)
    entry_widget.configure(state="disabled")


def bindHoverEventRecursively(widget, _on_enter, _on_leave):
    widget.bind("<Enter>", _on_enter)
    widget.bind("<Leave>", _on_leave)

    for child in widget.winfo_children():
        bindHoverEventRecursively(child, _on_enter, _on_leave)
    
    
def bindClickEventRecursively(widget, callback, cursor="hand2"):
    if not isinstance(widget, ctk.CTkButton):
        widget.bind("<Button-1>", callback)
        widget.configure(cursor=cursor)
    
    for child in widget.winfo_children():
        bindClickEventRecursively(child, callback, cursor)
        

def center_popup_window(popup, master, width, height):
    """
    Centers a popup window on top of the master window.

    Args:
        popup (Toplevel): The popup window to position.
        master (Widget): The main/root window.
        width (int): Width of the popup window.
        height (int): Height of the popup window.
    """
    master.update_idletasks()
    main_x = master.winfo_rootx()
    main_y = master.winfo_rooty()
    main_width = master.winfo_width()
    main_height = master.winfo_height()

    pos_x = main_x + (main_width // 2) - (width // 2)
    pos_y = main_y + (main_height // 2) - (height // 2)

    popup.geometry(f"{width}x{height}+{pos_x}+{pos_y}")