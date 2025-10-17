# datetime_picker_modal.py

import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, date
from utils import center_popup_window
from Components.timeSpinBoxPickerModal import SpinBox


class DateTimePickerModal:
    def open_datetime_picker(parent, current_datetime_str, on_selected):
        def handle_selection(datetime_str):
            on_selected(datetime_str)

        DateTimePickerModal.open(parent, current_datetime_str, handle_selection)

    def open(master, current_datetime_str=None, on_datetime_selected=None):
        popup = ctk.CTkToplevel(master)
        popup.title("Select Date and Time")
        popup.resizable(False, False)

        popup_width, popup_height = 340, 300
        center_popup_window(popup, master, popup_width, popup_height)
        popup.grab_set()

        # Default values
        default_date = date.today()
        default_time = "12:00 AM"

        if current_datetime_str:
            try:
                dt = datetime.strptime(current_datetime_str, "%Y-%m-%d %I:%M %p")
                default_date = dt.date()
                default_time = dt.strftime("%I:%M %p")  # convert back to 12-hour format for spinbox
            except Exception as e:
                print(f"[WARN] Failed to parse datetime: {e}")

        # ─── Date ─── #
        label_date = ctk.CTkLabel(popup, text="Choose date:")
        label_date.pack(pady=(20, 0))

        date_entry = DateEntry(popup,
                               date_pattern="yyyy-mm-dd",
                               year=default_date.year,
                               month=default_date.month,
                               day=default_date.day,
                               width=12)
        date_entry.pack(pady=(5, 20))

        # ─── Time ─── #
        label_time = ctk.CTkLabel(popup, text="Choose time:")
        label_time.pack()

        time_frame = ctk.CTkFrame(popup)
        time_frame.pack(pady=(5, 20))

        hours = [str(i) for i in range(1, 13)]
        minutes = [str(i) for i in range(0, 60)]
        periods = ["AM", "PM"]

        init_hour, init_minute, init_period = "12", "00", "AM"
        try:
            dt_time = datetime.strptime(default_time, "%I:%M %p")
            init_hour = str(int(dt_time.strftime("%I")))
            init_minute = str(int(dt_time.strftime("%M")))
            init_period = dt_time.strftime("%p")
        except Exception as e:
            print(f"[WARN] Failed to parse time: {e}")

        hour_box = SpinBox(time_frame, values=hours, width=60, allow_typing=True)
        hour_box.set(init_hour)
        hour_box.pack(side="left", padx=(0, 10))

        minute_box = SpinBox(time_frame, values=minutes, width=60, allow_typing=True)
        minute_box.set(init_minute)
        minute_box.pack(side="left", padx=(0, 10))

        period_box = SpinBox(time_frame, values=periods, width=60, allow_typing=False)
        period_box.set(init_period)
        period_box.pack(side="left")

        hour_box.entry.focus_set()

        # ─── Confirm Button ─── #
        def confirm():
            hour_box.validate_input()
            minute_box.validate_input()
            period_box.validate_input()

            date_str = date_entry.get_date().strftime("%Y-%m-%d")
            hrs = hour_box.get().zfill(2)
            mins = minute_box.get().zfill(2)
            period = period_box.get()

            formatted_input = f"{hrs}:{mins} {period}"
            try:
                time_obj = datetime.strptime(formatted_input, "%I:%M %p")
                time_str_12h = time_obj.strftime("%I:%M %p")
                full_datetime_str = f"{date_str} {time_str_12h}"
            except ValueError:
                full_datetime_str = f"{date_str} 12:00 AM"  # fallback


            if on_datetime_selected:
                on_datetime_selected(full_datetime_str)

            popup.destroy()

        confirm_btn = ctk.CTkButton(popup, text="OK", command=confirm)
        confirm_btn.pack(pady=10)

        popup.mainloop()
