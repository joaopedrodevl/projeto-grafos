from tkinter import *

class Interface:
    def __init__(self, target_list):
        self.target = None
        self.window = Tk()
        self.window.title("Choose the target")
        
        # Centering the window
        window_width = 300
        window_height = 150

        # Getting the screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculating the x and y coordinates of the window
        posx = (screen_width // 2) - (window_width // 2)
        posy = (screen_height // 2) - (window_height // 2)

        # Setting the window's position
        self.window.geometry(f"{window_width}x{window_height}+{posx}+{posy}")

        # Setting the target
        self.target = StringVar()
        self.target.set(target_list[0])

        # Creating the dropdown
        dropdown = OptionMenu(self.window, self.target, *target_list)
        dropdown.pack(pady=20)

        # Creating the confirm button
        confirm_button = Button(self.window, text="Confirmar", command=self.confirm_selection)
        confirm_button.pack(pady=10)

    # Confirming the selection
    def confirm_selection(self):
        self.window.quit()
        self.window.destroy() # Destroying the window

    # Running the interface
    def run(self):
        self.window.mainloop()
        return self.target.get()