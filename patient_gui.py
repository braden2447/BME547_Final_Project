import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime

def load_and_resize_image(filename):
    pil_image = Image.open(filename)
    original_size = pil_image.size
    adj_factor = 0.2
    new_width = round(original_size[0] * adj_factor)
    new_height = round(original_size[1] * adj_factor)
    resized_image = pil_image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def patient_gui():
    
    def medical_img_btn_cmd():
        pass
    
    
    def ecg_btn_cmd():
        # Open file
        # Analyze file via old ecg analysis code
        # Return plot as ImageTk and HR number as tk.StringVar
        pass
    
    
    def upload_btn_cmd():
        pass


    def clear_btn_cmd():
        pass

    
    root = tk.Tk()
    root.title("Patient-Side GUI Client")
    
    name_label = ttk.Label(root, text="Patient Name")
    name_label.grid(column=0, row=0)
    
    name_data = tk.StringVar()
    name_box = ttk.Entry(root, width=30, textvariable=name_data)
    name_box.grid(column=0, row=1, padx=(10,10), pady=(5,20))
    
    mrn_label = ttk.Label(root, text="Patient MRN")
    mrn_label.grid(column=2, row=0, padx=(0,12))
    
    mrn_data = tk.StringVar()
    mrn_box = ttk.Entry(root, width=10, textvariable=mrn_data)
    mrn_box.grid(column=2, row=1, padx=(0,10), pady=(5,20))
    
    medical_img_label = ttk.Label(root, text="Medical Image")
    medical_img_label.grid(column=0, row=2)
    
    medical_img_btn = ttk.Button(root, text="Select image file",
                                 command=medical_img_btn_cmd)
    medical_img_btn.grid(column=0, row=3, padx=(10,10), pady=(5,20))
    
    med_img_placeholder = load_and_resize_image("images/Transparent.png")
    image_label = ttk.Label(root, image=med_img_placeholder)
    image_label.grid(column=0, row=4, columnspan=2, rowspan=3)
        
    ecg_data_label = ttk.Label(root, text="Analyze ECG Data")
    ecg_data_label.grid(column=2, row=2)
    
    ecg_data_btn = ttk.Button(root, text="Select ECG data file",
                              command=ecg_btn_cmd)
    ecg_data_btn.grid(column=2, row=3, padx=(10,10), pady=(5,20))
    
    hr_label = ttk.Label(root, text="HR (bpm):")
    hr_label.grid(column=2, row=5)
    
    hr_value = tk.StringVar() # Need to integrate with ecg btn command return
    hr_box = ttk.Entry(root, width=4, textvariable=hr_value)
    hr_box.state=(["readonly"])
    hr_box.grid(row=5, column=2, columnspan=2)
    
    
    upload_btn = ttk.Button(root, text="UPLOAD",
                            command=upload_btn_cmd)
    upload_btn.grid(column=2, row=6)
    
    clear_btn = ttk.Button(root, text="CLEAR ALL",
                           command=clear_btn_cmd)
    clear_btn.grid(column=3, row=6, padx=(10,10))
    
    root.mainloop()


if __name__ == "__main__":
    patient_gui()