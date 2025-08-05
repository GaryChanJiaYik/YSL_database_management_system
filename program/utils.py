import os
import sys
import customtkinter as ctk

def resourcePath(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

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