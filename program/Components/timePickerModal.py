import customtkinter as ctk
from tktimepicker import AnalogPicker, AnalogThemes, constants
from datetime import datetime


class TimePickerModal:
    def open_time_picker(parent, current_time_str, on_selected):

        def handle_selection(tstr):
            on_selected(tstr)

        TimePickerModal.open(parent, default_type=constants.HOURS12, on_time_selected=handle_selection, initial_time=current_time_str)
    
    
    def open(master, default_type=constants.HOURS12, on_time_selected=None, initial_time=None):
        popup = ctk.CTkToplevel(master)
        popup.title("Select Time")

        # Fixed popup size
        popup_width, popup_height = 400, 500

        # Centering logic:
        master.update_idletasks()
        main_x = master.winfo_rootx()
        main_y = master.winfo_rooty()
        main_width = master.winfo_width()
        main_height = master.winfo_height()

        pos_x = main_x + (main_width // 2) - (popup_width // 2)
        pos_y = main_y + (main_height // 2) - (popup_height // 2)

        popup.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")
        popup.grab_set()

        # Initialize AnalogPicker as before
        time_picker = AnalogPicker(popup, type=default_type)
        try:
            clean_time = initial_time.strip()
            dt = datetime.strptime(clean_time, "%I:%M %p")
            hour_12 = dt.strftime("%I")
            minute = dt.minute
            period = dt.strftime("%p")
            period_const = constants.PM if period == "PM" else constants.AM
            time_picker = AnalogPicker(popup, type=default_type, period=period_const)
            time_picker.setHours(int(hour_12))
            time_picker.setMinutes(int(minute))
        except Exception:
            time_picker = AnalogPicker(popup, type=default_type)

        time_picker.pack(expand=True, fill="both")

        # You can keep this if you want AnalogPicker themed, else remove:
        theme = AnalogThemes(time_picker)
        theme.setDracula()  # or remove if you want default

        def confirm():
            hrs, mins, period = time_picker.time()
            time_str = f"{int(hrs):02d}:{int(mins):02d} {period}"
            if on_time_selected:
                on_time_selected(time_str)
            popup.destroy()

        btn = ctk.CTkButton(popup, text="OK", command=confirm)
        btn.pack(pady=10)

        popup.mainloop()

