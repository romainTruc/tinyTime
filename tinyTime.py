import tkinter as tk
import time

class CustomWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.overrideredirect(True)  # Remove the title bar and borders
        self.geometry('160x50')  # Set the window size
        self.configure(bg='#282828')  # Set the background color
        
        # Create a label for the timer display
        self.timer_label = tk.Label(
            self,
            text='45:00',
            font=('Arial', 23, 'bold', 'italic'),
            fg='#FFCA0B',
            bg='#282828'
        )
        self.timer_label.pack(pady=10)
        
        # Initialize the timer variables
        self.timer_running = False
        self.timer_start = 0
        self.timer_value = 45 * 60
        
        # Bind mouse events to the window
        self.bind('<ButtonPress-3>', self.start_move)
        self.bind('<B3-Motion>', self.move_window)
        self.bind('<ButtonRelease-3>', self.stop_move)
        self.bind('<Button-1>', self.start_pause_timer)
        self.bind('<Double-Button-1>', self.reset_timer)
        self.bind_all('<MouseWheel>', self.time_change)
        
        # Bind Escape key event to close the window
        self.bind('<Escape>', self.close_window)
        
        # Bind Ctrl + Shift + T key event to set the timer to 3 seconds
        self.bind('<Control-Shift-T>', self.set_timer_3_seconds)
        
        # Set the window always on top
        self.wm_attributes('-topmost', True)
        
        # Initialize variables for window movement
        self.start_x = 0
        self.start_y = 0
        
        # Start the timer
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.timer_start
            self.timer_value = max(self.timer_value - elapsed_time, 0)
            self.timer_start = time.time()

        minutes = int(self.timer_value // 60)
        seconds = int(self.timer_value % 60)

        if self.timer_value <= 0 and self.timer_running:
            self.timer_label.configure(text="OVER", fg='#F23B15', font=('Arial', 23, 'bold'))  # Set text, color, and font size
        else:
            timer_text = f'{minutes:02d}:{seconds:02d}'
            self.timer_label.configure(text=timer_text, fg='#2CCE3C', font=('Arial', 25, 'bold', 'italic'))  # Set text, color, and font size

        if self.timer_running and self.timer_value > 0:
            self.timer_label.configure(fg='#2CCE3C')  # Change text color to #2CCE3C when timer is running and not at 0
        elif not self.timer_running:
            self.timer_label.configure(fg='#FFCA0B')  # Change text color to white when timer is paused or stopped

        self.after(10, self.update_timer)  # Repeat the timer update every second



    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def move_window(self, event):
        self.geometry(f'+{event.x_root - self.start_x}+{event.y_root - self.start_y}')
    
    def stop_move(self, event):
        pass
    
    def start_pause_timer(self, event):
        if self.timer_running:
            self.timer_running = False
        else:
            self.timer_running = True
            self.timer_start = time.time()
    
    def reset_timer(self, event):
        self.timer_running = False
        self.timer_value = 45 * 60
    
    def time_change(self, event):
        if not self.timer_running:
            delta = event.delta
            if event.state & 0x4:  # Check if the Ctrl key is pressed
                if delta > 0:
                    self.timer_value += 60
                else:
                    self.timer_value = max(self.timer_value - 60, 60)
            else:
                if delta > 0:
                    if self.timer_value == 60:
                        self.timer_value += 9 * 60
                    else:
                        self.timer_value += 10 * 60
                else:
                    self.timer_value = max(self.timer_value - 10 * 60, 60)

    
    def close_window(self, event):
        self.destroy()
    
    def set_timer_3_seconds(self, event):
        if not self.timer_running:
            self.timer_value = 3
            self.update_timer()

window = CustomWindow()
window.mainloop()
