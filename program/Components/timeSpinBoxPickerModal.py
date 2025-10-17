import customtkinter as ctk
from datetime import datetime
from utils import center_popup_window 

class SpinBox(ctk.CTkFrame):
    def __init__(self, master, values, width=60, height=28, allow_typing=True, **kwargs):
        super().__init__(master, **kwargs)
        self.values = values
        self.index = 0
        self.allow_typing = allow_typing

        self.entry = ctk.CTkEntry(self, width=width, height=height, justify="center")
        self.entry.grid(row=0, column=0, rowspan=2)
        self.entry.bind("<Up>", self._on_arrow_up)
        self.entry.bind("<Down>", self._on_arrow_down)
        self.entry.bind("<FocusOut>", self.validate_input)
        self.entry.bind("<Return>", self.validate_input)  # Optional: Enter key to confirm

        if self.allow_typing:
            vcmd = (self.entry.register(self._validate_numeric_input), "%P")
            self.entry.configure(validate="key", validatecommand=vcmd)

        # if not self.allow_typing:
        #     self.entry.bind("<Key>", self._block_typing)
        #     # Allow focus, block mouse clicks and paste (optional)
        #     self.entry.bind("<Button-1>", lambda e: "break")
        #     self.entry.bind("<Control-v>", lambda e: "break")
        #     self.entry.bind("<Button-3>", lambda e: "break")
        
        if not self.allow_typing:
            self.entry.bind("<Key>", self._block_typing)
            # Remove the blocking of <Button-1> so clicks allow focus
            # self.entry.bind("<Button-1>", lambda e: "break")  # REMOVE THIS LINE
            
            # Optionally still block paste and right-click menu:
            self.entry.bind("<Control-v>", lambda e: "break")
            self.entry.bind("<Button-3>", lambda e: "break")


        self.up_btn = ctk.CTkButton(self, text="▲", width=24, height=12, command=self.increment)
        self.up_btn.grid(row=0, column=1, sticky="nsew", padx=(2, 0))

        self.down_btn = ctk.CTkButton(self, text="▼", width=24, height=12, command=self.decrement)
        self.down_btn.grid(row=1, column=1, sticky="nsew", padx=(2, 0))

        self.set(self.values[0])  # Initialize

    def _on_arrow_up(self, event):
        self.increment()
        return "break"  # Prevent default behavior

    def _on_arrow_down(self, event):
        self.decrement()
        return "break"  # Prevent default behavior

    def increment(self):
        self.index = (self.index + 1) % len(self.values)
        self.set(self.values[self.index])

    def decrement(self):
        self.index = (self.index - 1) % len(self.values)
        self.set(self.values[self.index])

    def set(self, value):
        if value in self.values:
            self.index = self.values.index(value)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)

    def get(self):
        return self.entry.get().strip()

    def validate_input(self, event=None):
        typed_value = self.entry.get().strip()

        if self.allow_typing:
            if typed_value == "":
                # If called from a real event (focus out or return), reset to last valid
                if event is not None:
                    self.set(self.values[self.index])
                # If called manually (event is None), you may want to force reset as well:
                else:
                    self.set(self.values[self.index])
                return
            if typed_value in self.values:
                self.set(typed_value)
            else:
                matches = [v for v in self.values if v.startswith(typed_value)]
                if len(matches) == 1:
                    self.set(matches[0])
                else:
                    self.set(self.values[self.index])
        else:
            self.set(self.values[self.index])


    def _block_typing(self, event):
        # Allow navigation and control keys even if typing disallowed
        allowed_keys = {
            "Up", "Down", "Left", "Right", "Tab", "BackSpace", "Delete",
            "Home", "End", "Shift_L", "Shift_R", "Control_L", "Control_R"
        }
        if event.keysym in allowed_keys:
            return None  # Allow these keys
        return "break"  # Block everything else
    
    def _validate_numeric_input(self, proposed_text):
        # Allow empty string so user can delete text
        if proposed_text == "":
            return True
        # Allow only digits
        return proposed_text.isdigit()



class TimeSpinBoxPickerModal:
    def open_time_picker(parent, current_time_str, on_selected):
        def handle_selection(time_str):
            on_selected(time_str)

        TimeSpinBoxPickerModal.open(parent, current_time_str, handle_selection)

    def open(master, initial_time=None, on_time_selected=None):
        popup = ctk.CTkToplevel(master)
        popup.title("Select Time")

        popup_width, popup_height = 320, 180
        center_popup_window(popup, master, popup_width, popup_height)
        popup.grab_set()

        # Defaults
        init_hour = "12"
        init_minute = "0"
        init_period = "AM"

        if initial_time:
            try:
                dt = datetime.strptime(initial_time.strip(), "%I:%M %p")
                init_hour = str(int(dt.strftime("%I")))   # Remove leading zero
                init_minute = str(int(dt.strftime("%M"))) # Remove leading zero
                init_period = dt.strftime("%p")
            except Exception as e:
                print(f"Time parsing error: {e}")

        # ─── Time Selector Frame (Horizontal Layout) ─── #
        time_frame = ctk.CTkFrame(popup)
        time_frame.pack(pady=30, padx=10)

        # ─── Hour ───
        hours = [str(i) for i in range(1, 13)]
        hour_box = SpinBox(time_frame, values=hours, width=60, allow_typing=True)
        hour_box.set(init_hour)
        hour_box.pack(side="left", padx=(0, 10))

        # ─── Minute ───
        minutes = [str(i) for i in range(0, 60)]
        minute_box = SpinBox(time_frame, values=minutes, width=60, allow_typing=True)
        minute_box.set(init_minute)
        minute_box.pack(side="left", padx=(0, 10))

        # ─── AM/PM ───
        period_box = SpinBox(time_frame, values=["AM", "PM"], width=60, allow_typing=False)
        period_box.set(init_period)
        period_box.pack(side="left")

        # Set initial focus on hour entry for convenience
        hour_box.entry.focus_set()

        # ─── Confirm Button ─── #
        def confirm():
            # Force validation on all fields to prevent empty or invalid values
            hour_box.validate_input()
            minute_box.validate_input()
            period_box.validate_input()

            hrs = hour_box.get()
            mins = minute_box.get()
            period = period_box.get()
            time_str = f"{hrs.zfill(2)}:{mins.zfill(2)} {period}"
            if on_time_selected:
                on_time_selected(time_str)
            popup.destroy()


        confirm_btn = ctk.CTkButton(popup, text="OK", command=confirm)
        confirm_btn.pack(pady=10)

        popup.mainloop()
