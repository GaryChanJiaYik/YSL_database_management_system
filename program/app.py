import customtkinter as ctk
from Constant.appConstant import STANDARD_WINDOW_SIZE 
from windows.landing import LandingWindow

class App:
    def __init__(self):        
        self.appRoot = ctk.CTk()
        self.appRoot.title("YSL DB Management")
        self.appRoot.geometry("800x600")  # Replace with your STANDARD_WINDOW_SIZE

        self.container = ctk.CTkFrame(self.appRoot)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.switch_frame(LandingWindow)

        self.appRoot.mainloop()

    def switch_frame(self, FrameClass, *args, **kwargs):
        # Destroy current frame if exists
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Create new frame and pack it
        self.current_frame = FrameClass(self.container, self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)
