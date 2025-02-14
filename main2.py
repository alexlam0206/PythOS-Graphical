import os
import tkinter as tk
from tkinter import Button, Frame, Label, messagebox, PhotoImage, Toplevel
try:
    import pygame #type:ignore
except:
    os.system("pip install pygame")
    import pygame #type:ignore
try:
    import sounddevice as sd #type: ignore
    import soundfile as sf #type: ignore
except:
    os.system("pip install sounddevice soundfile")
    import sounddevice as sd #type:ignore
    import soundfile as sf #type:ignore
os.system("cls")

pygame.init()

# Create the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PythOS Graphical")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)

# Load up the boot logo
boot_logo = pygame.image.load("PythOS/boot/boot.png")
scaled_boot_logo = pygame.transform.scale(boot_logo, (300, 350))

# Fonts
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16)

# Load and play boot sound
data, samplerate = sf.read("PythOS/boot/boot.mp3")

# Loading screen function
def show_loading_screen():
    screen.fill(BLACK)  # Black background
    loading_text = font.render("Booting PythOS...", True, WHITE)
    screen.blit(loading_text, (30, (600 - 30)))
    screen.blit(scaled_boot_logo, (250, 50))
    pygame.display.flip()
    pygame.time.delay(3000)  # Show loading screen for 3 seconds
    pygame.quit()


# Show the loading screen
show_loading_screen()
sd.play(data, samplerate)


class VirtualDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("PythOS Graphical")
        try:
            self.root.state("zoomed")
        except:
            self.root.attributes("-zoomed", True)

        # Get the screen resolution
        self.device_screen_h = self.root.winfo_screenheight()
        self.device_screen_w = self.root.winfo_screenwidth()

        # Represent background
        self.desktop = tk.Canvas(root, bg="blue")
        self.desktop.pack(expand=True, fill="both")

        # Create taskbar
        self.taskbar = Frame(root, bg="white", height=int(self.device_screen_h * 0.04))
        self.taskbar.pack(side="bottom", fill="x")
        self.taskbar.pack_propagate(False)

        # Start menu state
        self.start_menu_open = False
        self.start_menu = None

        # Load background logo
        try:
            self.bkgnd_logo = PhotoImage(file="PythOS/boot/boot.png")
            self.desktop.create_image(
                self.device_screen_w // 2,
                self.device_screen_h // 2,
                image=self.bkgnd_logo,
                anchor="center",
            )
        except Exception as e:
            messagebox.showerror(
                "Continuable error",
                f"Error: {e}.\n\nPlease contact the developer for further maintenance",
            )
        # Check dev mode and add resolution label to taskbar
        with open("PythOS/logon/userdata/devmode.txt", "r") as devcheck:
            if devcheck.read() == "True":
                self.resolution = Label(
                    self.taskbar,
                    text=f"{self.device_screen_w}x{self.device_screen_h}",
                    bg="white",
                    fg="black",
                )
                self.resolution.pack(side="right", padx=10)
        
        
        # Add Start button to taskbar
        self.startbtn = Button(self.taskbar, text="Start", command=self.toggle_start_menu)
        self.startbtn.pack(side="left", padx=10)

    def shutdown(self):
        self.root.destroy()  # Close the Tkinter window
        boot_logo = pygame.image.load("PythOS/boot/boot.png")
        scaled_boot_logo = pygame.transform.scale(boot_logo, (300, 350))
        pygame.init()
        screen = pygame.display.set_mode((800,600))
        screen.fill(BLACK)  # Black background
        font = pygame.font.SysFont("Arial", 20)
        shutdown_text = font.render("Shutting Down...", True, WHITE)
        seeunexttime = font.render("See you next time!", True, WHITE)
        screen.blit(shutdown_text, (30, (600 - 50)))
        screen.blit(seeunexttime, (30, (600-30)))
        screen.blit(scaled_boot_logo, (250, 50))
        pygame.display.flip()
        pygame.time.delay(3000)  # Show shutdown screen for 3 seconds
        pygame.quit()
    def reboot(self):
        self.root.destroy()  # Close the Tkinter window
        boot_logo = pygame.image.load("PythOS/boot/boot.png")
        scaled_boot_logo = pygame.transform.scale(boot_logo, (300, 350))
        pygame.init()
        screen = pygame.display.set_mode((800,600))
        screen.fill(BLACK)  # Black background
        font = pygame.font.SysFont("Arial", 20)
        shutdown_text = font.render("Reboot...", True, WHITE)
        screen.blit(shutdown_text, (30, (600 - 50)))
        screen.blit(scaled_boot_logo, (250, 50))
        pygame.display.flip()
        pygame.time.delay(3000)  # Show shutdown screen for 3 seconds
        pygame.quit()
        os.system("python3 bootloader.py")
        
    def bootoptions(self):
        def confrim_boot_selection():
            with open("PythOS/boot/boot_selection.txt", "w") as write_boot_selection:
                write_boot_selection.write(str(self.boot_option_var.get()))
            with open("PythOS/boot/boot_selection.txt", "r") as read_boot_selection:
                read_boot_selection = read_boot_selection.read()
                if read_boot_selection == "1":
                    pass
                elif read_boot_selection == "2":
                    messagebox.showinfo("Terminal Boot notice", "To boot GUI mode instantly, type 'startgui' and reboot. If you want to switch the setting back to GUI mode, please reboot the system in GUI mode and modify the setting.")
            self.boot_options_window.destroy()
        self.boot_options_window = Toplevel(self.root)
        self.boot_options_window.title("Boot Options")
        
        self.boot_option_var = tk.IntVar()
        
        self.boot_options_window.geometry("300x200")
        boot_options_label = Label(self.boot_options_window, text="Please select a boot option:")
        boot_options_label.pack()
        gui_boot = tk.Radiobutton(self.boot_options_window, text="GUI boot", variable=self.boot_option_var, value=1)
        gui_boot.pack()
        text_boot = tk.Radiobutton(self.boot_options_window, text="Terminal boot", variable=self.boot_option_var, value=2)
        text_boot.pack()

        boot_confirm_btn = Button(self.boot_options_window, text="Confirm", command=confrim_boot_selection)
        boot_confirm_btn.pack(side="right")
        
        cancel_btn = Button(self.boot_options_window, text="Cancel", command=self.boot_options_window.destroy)
        cancel_btn.pack(side="left")
            
    def power_options(self):
        def get_selection():
            power_option_int = self.power_option_var.get()
            if power_option_int == 1:
                self.shutdown()
            elif power_option_int == 2:
                self.reboot()
        self.power_options_window = Toplevel(self.root)
        
        self.power_option_var = tk.IntVar()
        
        self.power_options_window.title("Power Options")
        self.power_options_window.geometry("300x200")
        power_options_hint = Label(self.power_options_window, text="Please select Power Option:")
        power_options_hint.pack()
        
        shutdown_radiobtn = tk.Radiobutton(self.power_options_window, text="Shutdown", variable=self.power_option_var, value=1)
        reboot_radiobtn = tk.Radiobutton(self.power_options_window, text="Reboot", variable=self.power_option_var, value=2)
        
        shutdown_radiobtn.pack()
        reboot_radiobtn.pack()
        
        power_options_confirm_btn = Button(self.power_options_window, text="Confirm", command=get_selection)
        power_options_confirm_btn.pack(side="right")
        
        cancel_power_options_btn = Button(self.power_options_window, text="Cancel", command=self.power_options_window.destroy)
        cancel_power_options_btn.pack(side="left")
        
        
        
    def toggle_start_menu(self):
        """Toggle the Start Menu-like box."""
        if self.start_menu_open:
            self.close_start_menu()
        else:
            self.open_start_menu()

    def open_start_menu(self):
        """Open the Start Menu-like box."""
        self.start_menu = Toplevel(self.root)
        self.start_menu.overrideredirect(True)  # Remove window decorations
        self.start_menu.configure(bg="lightgray")

        # Set the size of the Start Menu
        menu_width = self.device_screen_w // 5
        menu_height = self.device_screen_h // 2
        self.start_menu.geometry(f"{menu_width}x{menu_height}")

        # Position the Start Menu above the taskbar button
        button_x = self.startbtn.winfo_rootx()
        button_y = self.startbtn.winfo_rooty()
        self.start_menu.geometry(f"+{button_x}+{button_y - menu_height}")

        # Add options to the Start Menu
        options = [
            ("Settings", self.open_settings),
            ("Notepad", self.open_notepad),
            ("Calculator", self.open_calculator),
            ("Boot Options", self.bootoptions),
            ("Power Options", self.power_options),
        ]
        for option, command in options:
            button = Button(
                self.start_menu,
                text=option,
                bg="lightgray",
                fg="black",
                relief="flat",  # Remove button border
                width=20,
                anchor="w",  # Align text to the left
                command=command,
            )
            button.pack(fill="x", pady=2)

        # Close the Start Menu when it loses focus
        self.start_menu.bind("<FocusOut>", lambda e: self.close_start_menu())

        # Set the Start Menu as focused
        self.start_menu.focus_set()

        # Update the state
        self.start_menu_open = True

    def close_start_menu(self):
        """Close the Start Menu-like box."""
        if self.start_menu_open and self.start_menu:
            self.start_menu.destroy()
            self.start_menu_open = False

    # Placeholder methods for Start Menu options
    def open_settings(self):
        """Open the Settings window."""
        settings_window = Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        Label(settings_window, text="Settings in development").pack()
    def open_notepad(self):
        """Open the Notepad window."""
        notepad_window = Toplevel(self.root)
        notepad_window.title("Notepad")
        notepad_window.geometry("500x400")
        text_area = tk.Text(notepad_window)
        text_area.pack(expand=True, fill="both")

    def open_calculator(self):
        """Open the Calculator window."""
        calculator_window = Toplevel(self.root)
        calculator_window.title("Calculator")
        calculator_window.geometry("300x400")
        Label(calculator_window, text="This is the Calculator window.").pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    desktop = VirtualDesktop(root)
    root.mainloop()