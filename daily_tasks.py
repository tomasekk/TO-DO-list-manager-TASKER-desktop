############################################
# Author: Ondrej Tomasek
# Programmed by: Ondrej Tomasek
# LinkedIn: linkedin.com/in/ondrat
# Date of creation (DD.MM.YYYY): 02.03.2023
############################################
# Please read README.txt before use
############################################

import tkinter as tk
import datetime
from PIL import Image, ImageTk
import readable_format
import object_names

logo_path = "PSD/logo.ico"
history_file_path = "data/history.txt"
current_data_file_path = "data/existing_data.txt"
session_file_path = "data/session_live_data.txt"
time_format_data = "YYYY%YMM%mDD%d/HOUR%HMINUTE%MSECOND%S"

# Reset session file
with open(session_file_path, "w"):
    pass

def update_session(what, edit):
    with open(session_file_path, "a") as session_file:
        now = datetime.datetime.now()
        timestamp = now.strftime(time_format_data)
        session_file.write(f"{timestamp}€$€${what} - **{edit}**\n")

def load_button_graphics():
    global new_size_done, image_add_task, img_load_done
    img_load_done = Image.open("PSD/done_green.png")
    new_size_done = tuple(int(x * 0.015) for x in img_load_done.size)
    img_load_add_task = Image.open("PSD/add_task.png")
    image_add_task = img_load_add_task.resize((int(img_load_add_task.size[0] * 0.06), int(img_load_add_task.size[1] * 0.06)))

class DoneButton:
    def __init__(self, master, text):
        self.master = master
        self.text = text
        self.create_widgets()


    def create_widgets(self):
        self.display_text = tk.Label(self.master, text=self.text, bg="#1a1a1a", fg="white")
        self.display_text.config(highlightbackground="#1a1a1a", highlightcolor="#1a1a1a", highlightthickness=1)
        self.display_text.pack()
        self.done_button = tk.Button(self.master, command=self.remove_text, bg="#1a1a1a", bd=0, highlightthickness=0)
        self.done_button.config(highlightbackground="#1a1a1a", highlightcolor="#1a1a1a", highlightthickness=1)


        img = img_load_done.resize(new_size_done, Image.Resampling.LANCZOS)

        img = ImageTk.PhotoImage(img)
        self.done_button.config(image=img)
        self.done_button.image = img
        self.done_button.pack()

    def remove_text(self):
        text_to_remove = self.text
        update_session("Remove task", text_to_remove)
        self.display_text.destroy()
        self.done_button.destroy()
        with open(current_data_file_path, "r") as f:
            lines = f.readlines()
        with open(current_data_file_path, "w") as f:
            for line in lines:
                if text_to_remove not in line:
                    f.write(line)
        with open(history_file_path, "a") as f:
            now = datetime.datetime.now()
            timestamp = now.strftime(time_format_data)
            f.write(f"{timestamp}€$€${text_to_remove}\n")


class App:
    def __init__(self, master):
        self.master = master
        self.text = tk.StringVar()
        self.done_buttons = []
        self.create_widgets()
        self.master.bind("<Configure>", self.window_resized)

        # center the window on the screen
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_widgets(self):
        bg_color = "#1a1a1a"
        now = datetime.datetime.now()
        day_name = now.strftime("%A")
        date_str = now.strftime("%d.%m. %Y")
        self.master_width = self.master.winfo_screenwidth()
        self.master_height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.master_width // 4.5, self.master_height // 2))
        self.master.title(object_names.nm_main_window)
        self.master.config(bg=bg_color)  # set the background color to black

        # create the menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # create the "menu" button in the menu bar
        menu_button = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu_button)

        # create the "history" button in the menu bar
        history_button = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="History", menu=history_button)

        # create the "Load history" option in the "history" button submenu
        load_history_option = tk.Menu(history_button, tearoff=0)
        history_button.add_cascade(label="Load history", menu=load_history_option)

        # create the "Clear history" option in the "history" button submenu
        clear_history_option = tk.Menu(history_button, tearoff=0)
        clear_history_option.add_command(label="Clear history", command=self.clear_history)
        history_button.add_cascade(label="Clear history", menu=clear_history_option)

        self.hello_label = tk.Label(self.master, text=f"Tasker\n{day_name} - {date_str}", bg=bg_color, fg="white",
                                    font=("TkDefaultFont", 14, "bold"))
        self.hello_label.place(relx=0.5, rely=0.08, anchor="center")

        self.text_entry = tk.Entry(self.master, textvariable=self.text, bg="white")
        self.text_entry.place(relx=0.5, rely=0.15, anchor="center")
        self.text_entry.bind("<Return>", lambda event: self.submit_text())

        # open the image file, resize it by 90%, and convert it to a PhotoImage object

        self.add_task_image = ImageTk.PhotoImage(image_add_task)

        self.submit_button = tk.Button(self.master, image=self.add_task_image, command=self.submit_text, bg="#1a1a1a",
                                       activebackground="#1a1a1a", bd=0)
        self.submit_button.place(relx=0.5, rely=0.2, anchor="n")

        # Create a frame to hold the done buttons
        self.done_frame = tk.Frame(self.master, bg=bg_color)  # set the background color to black
        self.done_frame.place(relx=0.5, rely=0.3, anchor="n")

        try:
            with open(current_data_file_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    text = line.strip()
                    start_index = text.find("€$€$")
                    if start_index != -1:
                        text = text[start_index + len("€$€$"):]
                    text = text.strip()
                    if text:
                        done_button = DoneButton(self.done_frame, text)
                        self.done_buttons.append(done_button)
        except FileNotFoundError:
            pass


    def submit_text(self):
        text = self.text.get()
        if text:
            self.text_entry.delete(0, tk.END)
            if text == "#programmer" or text == "#getProgrammer":
                update_session("Call command", text)
                # Open a new window with a label containing "programmed by ondrat"
                programmer_window = tk.Toplevel(self.master)
                programmer_window.iconbitmap(logo_path)
                programmer_label = tk.Label(programmer_window, text="""###################################
# Author: Ondrej Tomasek
# Programmed by: Ondrej Tomasek
# LinkedIn: linkedin.com/in/ondrat
# Idea: Lukas Laznicka
# Date (DD.MM.YYYY): 02.03.2023
###################################""")
                #programmer_window.geometry(100, 100)
                programmer_window.title(object_names.nm_programmer_info_window)
                programmer_window.config(bg="#4d0000")
                programmer_label.config(bg="#4d0000", fg="white", font=("TkDefaultFont", 12, "bold"))
                programmer_label.pack()
                print("""
                
###################################
# Author: Ondrej Tomasek
# Programmed by: Ondrej Tomasek
# LinkedIn: linkedin.com/in/ondrat
# Idea: Lukas Laznicka
# Date (DD.MM.YYYY): 02.03.2023
###################################

""")


            elif text == "#getHistory":
                update_session("Call command", text)
                # Open a new window with a label containing "readable history data"
                history_data_window = tk.Toplevel(self.master)
                history_data_window.iconbitmap(logo_path)
                history_data_label = tk.Label(history_data_window, text=readable_format.history_data())
                history_data_window.title(object_names.nm_history_data_window)
                history_data_window.config(bg="#4d0000")
                history_data_label.config(bg="#4d0000", fg="white", font=("TkDefaultFont", 12, "bold"))
                history_data_label.pack()
                print(readable_format.history_data())
            elif text == "#getCurrent":
                update_session("Call command", text)
                # Open a new window with a label containing "readable current data"
                current_data_window = tk.Toplevel(self.master)
                current_data_window.iconbitmap(logo_path)
                current_data_label = tk.Label(current_data_window, text=readable_format.history_data())
                current_data_window.title(object_names.nm_current_data_window)
                current_data_window.config(bg="#4d0000")
                current_data_label.config(bg="#4d0000", fg="white", font=("TkDefaultFont", 12, "bold"))
                current_data_label.pack()
                print(readable_format.current_data())
            elif text == "#getSession":
                update_session("Call command", text)
                # Open a new window with a label containing "readable current data"
                getSession_window = tk.Toplevel(self.master)
                getSession_window.iconbitmap(logo_path)
                getSession_label = tk.Label(getSession_window, text=readable_format.session_data())
                getSession_window.title(object_names.nm_session_data_window)
                getSession_window.config(bg="#4d0000")
                getSession_label.config(bg="#4d0000", fg="white", font=("TkDefaultFont", 12, "bold"))
                getSession_label.pack()
                print(readable_format.session_data())
            else:
                update_session("Add task", text)
                done_button = DoneButton(self.done_frame, text)
                self.done_buttons.append(done_button)
                # Append the submitted text to a new line in the existing_data.txt file
                with open(current_data_file_path, "a") as f:
                    now = datetime.datetime.now()
                    timestamp = now.strftime(time_format_data)
                    f.write(f"{timestamp}€$€${text}\n")

    def clear_history(self):
        with open(history_file_path, "w"):
            pass
        update_session("Clear history", "history.txt wiped")
        self.history_window = tk.Toplevel(self.master)
        self.history_window.iconbitmap(logo_path)
        self.history_window.title(object_names.nm_history_window)
        self.history_window.config(bg="#1a1a1a")
        self.history_window.geometry("%dx%d+0+0" % (self.master_width // 2, self.master_height // 2))
        self.history_label = tk.Label(self.history_window, text="History cleared", font=("TkDefaultFont", 12, "bold"),
                                      bg="#1a1a1a", fg="white")
        self.history_label.pack(expand=True)

    def window_resized(self, event):
        # Reset the size and position of the window when it's resized
        self.master_width = self.master.winfo_screenwidth()
        self.master_height = self.master.winfo_screenheight()


load_button_graphics()
root = tk.Tk()
app = App(root)
# Set icon
root.iconbitmap(logo_path)
root.mainloop()
