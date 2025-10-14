import customtkinter as ctk

class FloatingInfoPanel(ctk.CTkToplevel):
    def __init__(self, parent, text_lines, **kwargs):
        super().__init__(parent, **kwargs)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#333333", border_width=1, border_color="#555555")

        self.withdraw()  # Initially hidden

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(padx=8, pady=6)

        for line in text_lines:
            ctk.CTkLabel(
                self.container,
                text=line,
                font=("Arial", 12),
                text_color="white"
            ).pack(anchor="w", pady=1)

    def show_at(self, x, y):
        self.geometry(f"+{x}+{y}")
        self.deiconify()

    def hide(self):
        self.withdraw()
        

def attach_floating_info(widget, parent, info_lines, x_offset=10, y_offset=20):
    """Attaches a floating panel to a widget that shows on hover."""
    panel = FloatingInfoPanel(parent, info_lines)
    polling_job = {"job": None}

    def get_mouse_position():
        try:
            return widget.winfo_pointerxy()
        except:
            return None

    def is_mouse_over_widget_or_panel():
        x, y = get_mouse_position()
        if x is None: return False

        # Widget bounds
        wx, wy = widget.winfo_rootx(), widget.winfo_rooty()
        ww, wh = widget.winfo_width(), widget.winfo_height()
        if wx <= x <= wx + ww and wy <= y <= wy + wh:
            return True

        # Panel bounds
        if not panel.winfo_ismapped():
            return False
        px, py = panel.winfo_rootx(), panel.winfo_rooty()
        pw, ph = panel.winfo_width(), panel.winfo_height()
        if px <= x <= px + pw and py <= y <= py + ph:
            return True

        return False

    def poll_mouse():
        if not is_mouse_over_widget_or_panel():
            panel.hide()
            polling_job["job"] = None
        else:
            polling_job["job"] = widget.after(100, poll_mouse)

    def on_enter(event=None):
        if polling_job["job"] is None:
            x = widget.winfo_rootx() + x_offset
            y = widget.winfo_rooty() + y_offset
            panel.show_at(x, y)
            polling_job["job"] = widget.after(100, poll_mouse)

    def on_leave(event=None):
        # Don’t hide immediately; polling will handle it
        pass

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
