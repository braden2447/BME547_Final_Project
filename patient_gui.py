import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime


def load_and_resize_image(filename, adj_factor):
    pil_image = Image.open(filename)
    original_size = pil_image.size
    new_width = round(original_size[0] * adj_factor)
    new_height = round(original_size[1] * adj_factor)
    resized_image = pil_image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def patient_gui():

    def medical_img_btn_cmd():
        filename = filedialog.askopenfilename(initialdir="BME547_repos")
        if filename == "":
            messagebox.showinfo("Cancel", "You canceled the image load")
            return  # if user cancels picture file selection

        # Open image, resize, return tk image
        tk_image = load_and_resize_image(filename, 0.5)
        med_img_label.configure(image=tk_image)
        med_img_label.image = tk_image  # saving this variable

    def ecg_btn_cmd():
        # Open file
        # Analyze file via old ecg analysis code
        # Return plot as ImageTk and HR number as tk.StringVar
        pass

    def upload_btn_cmd():
        # Send json dict to server to store in database
        pass

    def clear_btn_cmd():
        name_box.delete(0, 100)
        mrn_box.delete(0, 10)
        # Add if statement checking if ECG trace and HR label exist

        # Return med image to transparent image
        tk_image = load_and_resize_image("images/Transparent.png", 0.2)
        med_img_label.configure(image=tk_image)
        med_img_label.image = tk_image

    def exit_btn_cmd():
        root.destroy()

    root = tk.Tk()
    root.title("Patient-Side GUI Client")

    name_label = ttk.Label(root, text="Patient Name")
    name_label.grid(column=0, row=0, pady=(10, 0))

    name_data = tk.StringVar()
    name_box = ttk.Entry(root, width=30, textvariable=name_data)
    name_box.grid(column=0, row=1, padx=(10, 10), pady=(5, 20))

    mrn_label = ttk.Label(root, text="Patient MRN")
    mrn_label.grid(column=2, row=0, padx=(10, 12), pady=(10, 0))

    mrn_data = tk.StringVar()
    mrn_box = ttk.Entry(root, width=10, textvariable=mrn_data)
    mrn_box.grid(column=2, row=1, padx=(10, 10), pady=(5, 20))

    medical_img_label = ttk.Label(root, text="Medical Image")
    medical_img_label.grid(column=0, row=2)

    medical_img_btn = ttk.Button(root, text="Select image file",
                                 command=medical_img_btn_cmd)
    medical_img_btn.grid(column=0, row=3, padx=(10, 10), pady=(5, 20))

    med_img_placeholder = load_and_resize_image("images/Transparent.png", 0.2)
    med_img_label = ttk.Label(root, image=med_img_placeholder)
    med_img_label.grid(column=0, row=4, columnspan=2, rowspan=3, padx=(10, 10))

    ecg_data_label = ttk.Label(root, text="Analyze ECG Data")
    ecg_data_label.grid(column=2, row=2)

    ecg_data_btn = ttk.Button(root, text="Select ECG data file",
                              command=ecg_btn_cmd)
    ecg_data_btn.grid(column=2, row=3, padx=(10, 10), pady=(5, 20))

    # Decided to display HR value as a label after ECG data analysis

    # hr_label = ttk.Label(root, text="HR (bpm):")
    # hr_label.grid(column=2, row=5, padx=(0,20), pady=(50,0))

    # hr_value = tk.StringVar() # Need to integrate with ecg btn command return
    # hr_box = ttk.Entry(root, width=4, textvariable=hr_value)
    # hr_box.state=(["readonly"])
    # hr_box.grid(row=5, column=2, columnspan=2, pady=(50,0))

    upload_btn = ttk.Button(root, text="UPLOAD",
                            command=upload_btn_cmd)
    upload_btn.grid(column=2, row=6)

    clear_btn = ttk.Button(root, text="CLEAR ALL",
                           command=clear_btn_cmd)
    clear_btn.grid(column=3, row=6, padx=(0, 20))

    exit_btn = ttk.Button(root, text="EXIT",
                          command=exit_btn_cmd)
    exit_btn.grid(column=2, row=7, columnspan=2, padx=(15, 0), pady=(0, 20))

    root.mainloop()


if __name__ == "__main__":
    patient_gui()
