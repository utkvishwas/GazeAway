import tkinter as tk
from tkinter import ttk, font, messagebox
import time
import threading
import os
import json
import sys
import winsound
from datetime import datetime
import pystray
from PIL import Image, ImageDraw
import winreg
import win32api
import win32event
import win32gui
import win32con
import winerror
from pathlib import Path

class EyeStrainReminder:
    def __init__(self):
        # Single instance check - must be done before creating any GUI elements
        self.check_single_instance()
        
        self.root = tk.Tk()
        self.root.title("Gaze Away")
        self.root.iconbitmap(self.resource_path("icon.ico"))
        
        # Set minimum window size
        self.root.minsize(400, 300)
        
        # Load settings
        self.settings = self.load_settings()
        
        # Get monitor information
        self.monitors = self.get_monitors()
        
        # Create settings window
        self.create_settings_window()
        
        # Create reminder windows
        self.reminders = []
        self.create_reminder_windows()
        
        # Initialize system tray
        self.setup_system_tray()
        
        # State variables
        self.running = True
        self.paused = True  # Start with timer paused
        self.timer_running = False
        
        # Bind close button
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Start timer thread
        self.thread = threading.Thread(target=self.run_timer)
        self.thread.daemon = True
        self.thread.start()
        
        # Timer restart event
        self.timer_restart_event = threading.Event()

    def check_single_instance(self):
        """Check if another instance is already running"""
        # Create a unique mutex name for this application
        mutex_name = "Global\\GazeAway_SingleInstance"
        
        try:
            # Try to create a mutex
            self.mutex = win32event.CreateMutex(None, False, mutex_name)
            
            # Check if the mutex already exists (another instance is running)
            if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
                print("GazeAway is already running!")
                # Try to bring the existing window to front
                try:
                    def enum_windows_callback(hwnd, windows):
                        if win32gui.IsWindowVisible(hwnd):
                            window_text = win32gui.GetWindowText(hwnd)
                            if "Gaze Away" in window_text:
                                windows.append(hwnd)
                        return True
                    
                    windows = []
                    win32gui.EnumWindows(enum_windows_callback, windows)
                    
                    if windows:
                        # Bring the first found window to front
                        win32gui.SetForegroundWindow(windows[0])
                        win32gui.ShowWindow(windows[0], win32con.SW_RESTORE)
                except:
                    pass
                
                # Show a message box to inform the user
                try:
                    import tkinter as tk
                    root = tk.Tk()
                    root.withdraw()  # Hide the root window
                    messagebox.showinfo("Gaze Away", "Gaze Away is already running!\nThe existing window has been brought to the front.")
                    root.destroy()
                except:
                    pass
                    
                sys.exit(1)
                
        except Exception as e:
            print(f"Error creating mutex: {e}")
            sys.exit(1)

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_monitors(self):
        """Get information about all connected monitors"""
        monitors = []
        try:
            monitor_info = win32api.EnumDisplayMonitors(None, None)
            for monitor in monitor_info:
                info = win32api.GetMonitorInfo(monitor[0])
                monitor_rect = info['Monitor']
                monitors.append({
                    'x': monitor_rect[0],
                    'y': monitor_rect[1],
                    'width': monitor_rect[2] - monitor_rect[0],
                    'height': monitor_rect[3] - monitor_rect[1]
                })
        except Exception as e:
            monitors = [{
                'x': 0,
                'y': 0,
                'width': self.root.winfo_screenwidth(),
                'height': self.root.winfo_screenheight()
            }]
        return monitors

    def create_settings_window(self):
        """Create the main settings window"""
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', padding=5)
        style.configure('TButton', padding=5)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Gaze Away  Settings", 
                               font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Timer Settings", padding=20)
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        # Interval setting
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(fill="x", pady=5)
        ttk.Label(interval_frame, text="Reminder Interval (minutes):").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value=str(self.settings["interval_minutes"]))
        interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var, width=10)
        interval_entry.pack(side=tk.RIGHT)
        
        # Break duration setting
        break_frame = ttk.Frame(settings_frame)
        break_frame.pack(fill="x", pady=5)
        ttk.Label(break_frame, text="Break Duration (seconds):").pack(side=tk.LEFT)
        self.break_var = tk.StringVar(value=str(self.settings["break_seconds"]))
        break_entry = ttk.Entry(break_frame, textvariable=self.break_var, width=10)
        break_entry.pack(side=tk.RIGHT)
        
        # Info text about saving settings
        info_label = ttk.Label(settings_frame, 
                              text="Click 'Save Settings' to apply timing changes", 
                              font=('Helvetica', 9),
                              foreground='#666666')
        info_label.pack(pady=(10, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=20)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        # Startup option
        self.startup_var = tk.BooleanVar(value=self.check_startup())
        startup_check = ttk.Checkbutton(options_frame, text="Start with Windows", 
                                      variable=self.startup_var, 
                                      command=self.toggle_startup)
        startup_check.pack(fill="x")
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=20)
        
        # Save button
        save_btn = ttk.Button(buttons_frame, text="Save Settings", 
                             command=self.save_settings)
        save_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # Start/Stop button
        self.timer_btn = ttk.Button(buttons_frame, text="Start Timer", 
                                   command=self.toggle_timer)
        self.timer_btn.pack(side=tk.LEFT, padx=5, expand=True)

    def create_reminder_windows(self):
        """Create reminder windows for each monitor"""
        for monitor in self.monitors:
            reminder = tk.Toplevel(self.root)
            reminder.withdraw()
            
            # Configure window
            reminder.overrideredirect(True)
            reminder.attributes('-topmost', True)
            
            # Set geometry for this monitor
            geometry = f"{monitor['width']}x{monitor['height']}+{monitor['x']}+{monitor['y']}"
            reminder.geometry(geometry)
            
            # Configure background
            reminder.configure(bg=self.settings["theme"]["bg_color"])
            reminder.attributes('-alpha', 0.95)
            
            # Content frame
            content_frame = tk.Frame(
                reminder,
                bg=self.settings["theme"]["bg_color"]
            )
            content_frame.place(relx=0.5, rely=0.5, anchor="center")
            
            # Labels
            title_label = tk.Label(
                content_frame,
                text="Time to Rest Your Eyes",
                font=("Helvetica", 48, "bold"),
                bg=self.settings["theme"]["bg_color"],
                fg=self.settings["theme"]["text_color"]
            )
            title_label.pack(pady=20)
            
            timer_label = tk.Label(
                content_frame,
                text=str(self.settings["break_seconds"]),
                font=("Helvetica", 120, "bold"),
                bg=self.settings["theme"]["bg_color"],
                fg=self.settings["theme"]["accent_color"]
            )
            timer_label.pack(pady=30)
            
            instruction_label = tk.Label(
                content_frame,
                text="Look at something 20 feet away",
                font=("Helvetica", 24),
                bg=self.settings["theme"]["bg_color"],
                fg=self.settings["theme"]["text_color"]
            )
            instruction_label.pack(pady=20)
            
            # Skip button
            skip_button = tk.Button(
                content_frame,
                text="Skip Break",
                font=("Helvetica", 16),
                bg=self.settings["theme"]["accent_color"],
                fg=self.settings["theme"]["bg_color"],
                relief="flat",
                command=self.skip_reminder,
                padx=20,
                pady=10
            )
            skip_button.pack(pady=30)
            
            skip_button.bind('<Enter>', 
                lambda e: e.widget.configure(bg=self.settings["theme"]["text_color"]))
            skip_button.bind('<Leave>', 
                lambda e: e.widget.configure(bg=self.settings["theme"]["accent_color"]))
            
            self.reminders.append({
                'window': reminder,
                'timer_label': timer_label
            })

    def setup_system_tray(self):
        """Initialize system tray icon and menu"""
        icon_image = self.create_tray_icon()
        menu = (
            pystray.MenuItem("Show Settings", self.show_settings),
            pystray.MenuItem("Pause/Resume", self.toggle_pause),
            pystray.MenuItem("Skip Break", self.skip_reminder),
            pystray.MenuItem("Exit", self.stop)
        )
        self.tray_icon = pystray.Icon("gaze_away", icon_image, "Gaze Away", menu)
        self.tray_icon.on_click = self.show_settings  # Left click to show settings
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def create_tray_icon(self, size=64):
        """Create the system tray icon"""
        image = Image.new('RGB', (size, size), color='white')
        d = ImageDraw.Draw(image)
        d.ellipse([size//4, size//4, 3*size//4, 3*size//4], outline='black', width=2)
        d.ellipse([3*size//8, 3*size//8, 5*size//8, 5*size//8], fill='black')
        return image

    def show_settings(self):
        """Show the settings window"""
        self.root.deiconify()
        self.root.lift()

    def check_startup(self):
        """Check if app is in startup registry"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                0, winreg.KEY_READ)
            winreg.QueryValueEx(key, "GazeAway")
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False

    def toggle_startup(self):
        """Toggle startup with Windows"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r"Software\Microsoft\Windows\CurrentVersion\Run", 
                            0, winreg.KEY_ALL_ACCESS)
        
        if self.startup_var.get():
            winreg.SetValueEx(key, "GazeAway", 0, winreg.REG_SZ, 
                             sys.executable)
        else:
            try:
                winreg.DeleteValue(key, "GazeAway")
            except WindowsError:
                pass
        
        winreg.CloseKey(key)

    def toggle_timer(self):
        """Toggle timer start/stop"""
        if self.paused:
            self.paused = False
            self.timer_btn.configure(text="Stop Timer")
        else:
            self.paused = True
            self.timer_btn.configure(text="Start Timer")

    def toggle_pause(self):
        """Toggle pause state"""
        self.toggle_timer()

    def on_close(self):
        """Handle window close event"""
        self.root.withdraw()

    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            "interval_minutes": 20,
            "break_seconds": 20,
            "theme": {
                "bg_color": "#1a1a1a",
                "text_color": "#ffffff",
                "accent_color": "#00ff9d"
            }
        }
        
        settings_path = os.path.join(os.getenv('APPDATA'), 'GazeAway', 'settings.json')
        
        try:
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            if os.path.exists(settings_path):
                with open(settings_path, "r") as f:
                    return {**default_settings, **json.load(f)}
        except:
            pass
        return default_settings

    def save_settings(self):
        """Save current settings to file"""
        try:
            self.settings["interval_minutes"] = int(self.interval_var.get())
            self.settings["break_seconds"] = int(self.break_var.get())
            
            settings_path = os.path.join(os.getenv('APPDATA'), 'GazeAway', 'settings.json')
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            
            with open(settings_path, "w") as f:
                json.dump(self.settings, f)
            
            # Restart timer thread with new interval if timer is running
            if self.running and not self.paused:
                self.restart_timer()
            
            messagebox.showinfo("Success", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for interval and break duration")

    def countdown(self):
        """Handle the countdown timer"""
        seconds_left = self.settings["break_seconds"]
        self.timer_running = True
        
        while seconds_left >= 0 and self.timer_running:
            # Update timer display on all screens
            for reminder in self.reminders:
                self.root.after(0, reminder['timer_label'].configure, {'text': str(seconds_left)})
            
            # Force update the display
            self.root.update()
            
            # Wait one second
            time.sleep(1)
            seconds_left -= 1
        
        # If timer completed normally, hide windows
        if seconds_left < 0 and self.timer_running:
            self.timer_running = False
            try:
                winsound.PlaySound(self.resource_path("notification.wav"), 
                                 winsound.SND_FILENAME | winsound.SND_ASYNC)
            except:
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            self.root.after(0, self.hide_reminders)

    def show_reminder(self):
        """Display the reminder on all monitors"""
        if self.paused:
            return
        
        # Show all windows
        for reminder in self.reminders:
            reminder['window'].deiconify()
        
        # Play notification sound
        try:
            winsound.PlaySound(self.resource_path("notification.wav"), 
                             winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        
        # Start countdown in a separate thread
        threading.Thread(target=self.countdown, daemon=True).start()

    def hide_reminders(self):
        """Hide all reminder windows"""
        self.timer_running = False
        for reminder in self.reminders:
            reminder['window'].withdraw()

    def skip_reminder(self):
        """Skip the current reminder"""
        self.timer_running = False
        self.hide_reminders()

    def restart_timer(self):
        """Restart the timer thread with new settings"""
        self.timer_restart_event.set()
    
    def run_timer(self):
        """Main timer loop"""
        while self.running:
            # Use a shorter sleep interval to be more responsive to setting changes
            sleep_interval = 1  # Check every second
            total_sleep_time = 0
            target_sleep_time = self.settings["interval_minutes"] * 60
            
            while total_sleep_time < target_sleep_time and self.running:
                # Sleep in small increments to check for restart events
                time.sleep(sleep_interval)
                total_sleep_time += sleep_interval
                
                # Check if timer should be restarted
                if self.timer_restart_event.is_set():
                    self.timer_restart_event.clear()
                    total_sleep_time = 0  # Reset timer
                    target_sleep_time = self.settings["interval_minutes"] * 60  # Update target
            
            if self.running and not self.paused:
                self.show_reminder()

    def stop(self):
        """Stop the application"""
        self.running = False
        self.timer_running = False
        
        # Signal timer thread to stop
        if hasattr(self, 'timer_restart_event'):
            self.timer_restart_event.set()
        
        # Stop the system tray icon
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.stop()
        
        # Hide all reminder windows
        self.hide_reminders()
        
        # Clean up mutex
        if hasattr(self, 'mutex') and self.mutex:
            try:
                import win32api
                win32api.CloseHandle(self.mutex)
            except:
                pass
        
        # Destroy the root window and all child windows
        if hasattr(self, 'root') and self.root:
            self.root.after(0, self.root.destroy)
        
        # Force exit the application
        os._exit(0)

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop()

if __name__ == "__main__":
    try:
        app = EyeStrainReminder()
        app.run()
    except Exception as e:
        print(f"Error running GazeAway: {e}")
        sys.exit(1)