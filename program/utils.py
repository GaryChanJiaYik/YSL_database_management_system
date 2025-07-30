import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def set_entry_value(entry_widget, value):
    entry_widget.configure(state="normal")
    entry_widget.delete(0, "end")
    entry_widget.insert(0, value)
    entry_widget.configure(state="disabled")