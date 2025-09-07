import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, delay=1000):
        self.widget = widget
        self.text = text
        self.delay = delay  # Delay in ms before tooltip appears
        self.tooltip_window = None
        self.after_id = None

        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)


    def schedule_show(self, event=None):
        self.after_id = self.widget.after(self.delay, self.show_tooltip)


    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            background="#222",
            foreground="white",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 9)
        )
        label.pack(ipadx=6, ipady=3)


    def hide_tooltip(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


    def move_tooltip(self, event):
        # Optional: update position when mouse moves
        if self.tooltip_window:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            self.tooltip_window.geometry(f"+{x}+{y}")
