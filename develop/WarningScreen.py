# Imports
import tkinter as tk
from tkinter import ttk
import os

# Application
class Application:

    def __init__(self, screen=None, message=None):
        self.screen = screen
        self.message = message

        self.settingsScreen()
        self.setup_style()
        self.interface()

    def settingsScreen(self):
        self.screen.title("LidSwitch")
        self.screen.configure(bg="#313131")
        
        # Geometry Screen
        self.width = 650
        self.height = 150
        screen_width = self.screen.winfo_screenwidth()
        screen_height = self.screen.winfo_screenheight()

        pos_x = (screen_width - self.width) // 2
        pos_y = (screen_height - self.height) // 2

        self.screen.geometry(f"{self.width}x{self.height}+{pos_x}+{pos_y}")
        self.screen.resizable(False, False)

    def destroyScreen(self): 
        self.screen.destroy()

    def rebootSystem(self): 
        self.destroyScreen()
        os.system("reboot")

    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        bg_color = "#313131"
        button_cancel_bg_color = "#505050"
        buttonFont = ("Arial", 12, "bold")

        self.style.configure("Main.TFrame",
                             background=bg_color)
        
        self.style.configure("Message.TLabel",
                             background=bg_color,
                             foreground="white",
                             font=("Arial", 14),
                             )
        
        self.style.configure("Button.TFrame",
                             background=bg_color)
        
        self.style.configure("Cancel.TButton",
                             background=button_cancel_bg_color,
                             foreground="white",
                             width=30,
                             height=5,
                             cursor="hand2",
                             font=buttonFont,
                             bordercolor=button_cancel_bg_color,
                             borderwidth=1,
                             relief="solid",
                             )
        
        self.style.map("Cancel.TButton",
                       background=[("active", "#999999")],
                       bordercolor=[("active", "#999999")])
        
        self.style.configure("Reboot.TButton",
                             background="#e71414",
                             foreground="white",
                             width=30,
                             height=5,
                             cursor="hand2",
                             font=buttonFont,
                             bordercolor="#d31010",
                             borderwidth=1,
                             relief="solid",
                             )
        
        self.style.map("Reboot.TButton",
                       background=[("active", "#f52d2d")],
                       bordercolor=[("active", "#e71414")])

    def interface(self):
        # Main Frame
        mainFrame = ttk.Frame(
            self.screen, 
            width=self.screen.winfo_width(), 
            height=self.screen.winfo_height(),
            style="Main.TFrame"
            )
        mainFrame.pack(expand=True, padx=5, pady=5)

        # Message
        message = ttk.Label(
            mainFrame, 
            text=(self.message), 
            wraplength=self.width,
            justify="center",
            style="Message.TLabel"
            )
        message.pack(pady=15)

        # Buttons
        buttonFrame = ttk.Frame(
            mainFrame,
            style="Button.TFrame"
            )
        buttonFrame.pack()
        
        cancelButton = ttk.Button(
            buttonFrame, 
            text="Cancel", 
            command=self.destroyScreen, 
            style="Cancel.TButton"
            )
        cancelButton.pack(side="left", padx=5)

        rebootButton = ttk.Button(
            buttonFrame, 
            text="Reboot", 
            command=self.rebootSystem, 
            style="Reboot.TButton"
            )
        rebootButton.pack(side="right", padx=5)

# Function to read ".env" file
def load_env(arquivo=".env"):
    variables = {}

    try:
        with open(arquivo, "r", encoding="UTF-8") as file:
            for row in file:
                row = row.strip()
                
                if not row or row.startswith("#"): continue

                if "=" in row:
                    key, value = row.split("=", 1)
                    variables[key.strip()] = value.strip()

    except FileNotFoundError:
        print("File not found.")
    
    except Exception as Error:
        print(f"Error reading file: {Error}")

    return variables

# Screen
if __name__ == "__main__":
    message = "LidSwitch: Disabled. Your device will not work with the screen down. When lowered, it will go into sleep mode, but you need to restart to complete activation. Reboot your computer?" if int((load_env("/usr/local/lib/LidSwitch/config.env"))["STATUS_LIDSWITCH"]) == 0 else "LidSwitch: Enabled. Your device will work with the screen down, but needs to restart to complete activation. Reboot your computer?"

    root = tk.Tk()
    app = Application(root, message)
    root.mainloop()