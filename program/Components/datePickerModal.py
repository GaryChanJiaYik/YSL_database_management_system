import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, date
from utils import center_popup_window

class DatePickerModal:
    def open_date_picker(parent, current_date_str, on_selected):
        try:
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d").date()
        except ValueError:
            current_date = date.today()

        def handle_selection(date_str):
            on_selected(date_str)

        DatePickerModal.open(parent, current_date=current_date, on_date_selected=handle_selection)
        
    
    def open(master, current_date=None, on_date_selected=None):
        popup = ctk.CTkToplevel(master)  # use CTkToplevel for auto theming
        popup.title("Select Date")
        popup.resizable(False, False)

        popup_width, popup_height = 200, 130

        center_popup_window(popup, master, popup_width, popup_height)
        popup.after(100, lambda: popup.grab_set())

        today = datetime.today().date()
        init = current_date if current_date else today

        label = ctk.CTkLabel(popup, text="Choose date:")
        label.pack(padx=10, pady=(10, 0))

        date_entry = DateEntry(popup,
                               date_pattern="yyyy-mm-dd",
                               year=init.year,
                               month=init.month,
                               day=init.day,
                               width=12)
        date_entry.pack(padx=10, pady=10)

        def confirm():
            selected = date_entry.get_date()
            if on_date_selected:
                on_date_selected(selected.strftime("%Y-%m-%d"))
            popup.destroy()

        btn = ctk.CTkButton(popup, text="OK", command=confirm)
        btn.pack(pady=(0,10))

        popup.mainloop()
