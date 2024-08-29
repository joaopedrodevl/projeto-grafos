from tkinter import *

class Interface:
    def __init__(self, title: str):
        self.data = ([], [], "")
        self.w = Tk()
        self.w.title(title)
        
        # Centering the window
        window_width = 720
        window_height = 300

        # Getting the screen width and height
        screen_width = self.w.winfo_screenwidth()
        screen_height = self.w.winfo_screenheight()

        # Calculating the x and y coordinates of the window
        posx = (screen_width // 2) - (window_width // 2)
        posy = (screen_height // 2) - (window_height // 2)

        # Setting the window's position
        self.w.geometry(f"{window_width}x{window_height}+{posx}+{posy}")
        self.w.resizable(False, False)

        # Configuring grid columns
        self.w.grid_columnconfigure(0, weight=1)
        self.w.grid_columnconfigure(1, weight=0)
        self.w.grid_columnconfigure(2, weight=1)
        
        # Configuring grid rows
        self.w.grid_rowconfigure(0, weight=1)  # Main content row for dropdowns and checkboxes
        self.w.grid_rowconfigure(1, weight=0)  # Text input row
        self.w.grid_rowconfigure(2, weight=0)  # Button row

        # Adding the Confirm button
        self.confirm_button = Button(self.w, text="Confirmar", command=self.confirm_selection)
        self.confirm_button.grid(row=2, column=2, padx=10, pady=10, sticky=SE)

        # Bind the Enter key to the Confirm button
        self.w.bind('<Return>', lambda event: self.confirm_selection())

        # Focus the Confirm button
        self.confirm_button.focus_set()
        
        # Initialize dropdown row counter
        self.dropdown_row = 0

        # Frame to hold dropdowns
        self.dropdown_frame = Frame(self.w)
        self.dropdown_frame.grid(row=0, column=2, padx=10, pady=10, sticky=N+S+E+W)

        # Initialize checkbox row counter
        self.checkbox_row = 0

        # Frame to hold checkboxes
        self.checkbox_frame = Frame(self.w)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)
        
        # Frame to hold text input
        self.text_input_frame = Frame(self.w)
        self.text_input_frame.grid(row=1, column=2, padx=10, pady=(10, 5), sticky=N+S+E+W)

        # Initialize dropdown vars
        self.dropdown_vars = []
        self.text_entry = None

        # Bind the close event
        self.w.protocol("WM_DELETE_WINDOW", self.on_closing)

    def checkbox_options(self, options: list, label_text: str = "Choose"):
        frame = Frame(self.checkbox_frame)
        frame.grid(row=self.checkbox_row, column=0, padx=10, pady=10, sticky=N+S+E+W)
        
        label = Label(frame, text=f"{label_text}: ")
        label.grid(row=0, column=0, columnspan=5, sticky=W)

        all_var = IntVar()
        all_check = Checkbutton(frame, text="Todas", variable=all_var, command=lambda: self.toggle_all(all_var, frame))
        all_check.grid(row=1, column=0, columnspan=5, sticky=W)

        option_vars = []
        for i, option in enumerate(options):
            var = IntVar()
            chk = Checkbutton(frame, text=option, variable=var)
            row = (i // 5) + 2
            column = i % 5
            chk.grid(row=row, column=column, sticky=W)
            option_vars.append((var, option))
        
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=0)
        for i in range(2, (len(options) // 5) + 3):
            frame.grid_rowconfigure(i, weight=1)

        self.checkbox_row += 1
        if not hasattr(self, 'checkbox_frames'):
            self.checkbox_frames = []
        self.checkbox_frames.append((frame, all_var, option_vars))
        
    def toggle_all(self, all_var, frame):
        state = all_var.get()
        for f, all_var_frame, vars_ in self.checkbox_frames:
            if f == frame:
                for var, _ in vars_:
                    var.set(state)
                break
    
    def dropdown_options(self, options: list, label_text: str = "Choose"):
        frame = Frame(self.dropdown_frame)
        frame.grid(row=self.dropdown_row, column=0, padx=5, pady=5, sticky=W)

        label = Label(frame, text=f"{label_text}: ")
        label.grid(row=0, column=0, padx=(0, 5), sticky=W)

        options = ["Nenhuma Seleção"] + options

        dropdown_var = StringVar()
        dropdown_var.set(options[0])

        # Create a frame for the OptionMenu to control its width
        dropdown_frame = Frame(frame)
        dropdown_frame.grid(row=0, column=1, sticky=W)
        
        # Define a fixed width for the OptionMenu
        dropdown = OptionMenu(dropdown_frame, dropdown_var, *options)
        dropdown.config(width=20)  # Adjust the width as needed
        dropdown.pack(side=LEFT)

        self.dropdown_row += 1
        self.dropdown_vars.append(dropdown_var)
        self.dropdown_frame.grid_rowconfigure(self.dropdown_row, weight=0)

    def text_input(self, label_text: str = "Input"):
        # Determine the row index for the text input based on the number of dropdowns
        row_index = 1  # Always place it in the row where the text input should be

        # Frame para entrada de texto, posicionado acima do botão de confirmação
        self.text_input_frame = Frame(self.w)
        self.text_input_frame.grid(row=row_index, column=2, padx=10, pady=(10, 5), sticky=N+S+E+W)

        # Label para entrada de texto
        label = Label(self.text_input_frame, text=f"{label_text}: ")
        label.grid(row=0, column=0, padx=(0, 5), sticky=W)
        
        # Entrada de texto com tamanho reduzido
        self.text_entry = Entry(self.text_input_frame, width=20)  # Ajuste o valor de 'width' conforme necessário
        self.text_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    def get_selections(self):
        selected_options = [text for frame, _, vars_ in self.checkbox_frames for var, text in vars_ if var.get() == 1]
        selected_dropdowns = [var.get() for var in self.dropdown_vars]
        selected_dropdowns = [s for s in selected_dropdowns if s != "Nenhuma Seleção"]
        text_input_value = self.text_entry.get() if self.text_entry and self.text_entry.winfo_ismapped() else ""

        return (selected_options, selected_dropdowns, text_input_value)
    
    def confirm_selection(self):
        self.data = self.get_selections()
        self.on_closing()

    def on_closing(self):
        self.w.quit()
        self.w.destroy()

    def run(self):
        self.w.mainloop()
        return self.data