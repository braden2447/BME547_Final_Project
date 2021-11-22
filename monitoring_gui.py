import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from patient_gui import load_and_resize_image


def monitoring_gui():

    def save_med_img_cmd():
        pass

    def save_latest_ecg_cmd():
        pass

    def save_hist_ecg_cmd():
        pass

    def clear_btn_cmd():
        mrn_combo_box.set('')
        mrn_box.delete(0, 10)
        name_box.delete(0, 100)
        hr_box.delete(0, 10)
        time_box.delete(0, 25)
        med_img_combo_box.set('')
        hist_ecg_combo_box.set('')
        # if statement to check if ECG traces exist
        
        # Return med img to transparent
        tk_image = load_and_resize_image("images/Transparent.png", 0.2)
        med_img_label.configure(image=tk_image)
        med_img_label.image = tk_image       

    def exit_btn_cmd():
        root.destroy()

    root = tk.Tk()
    root.title("Monitoring Station GUI Client")
    
    patient_select_label = ttk.Label(root, text="Select Patient by MRN:")
    patient_select_label.grid(column=0, row=0, pady=(10, 0))

    mrn_selected = tk.StringVar()
    mrn_combo_box = ttk.Combobox(root, textvariable=mrn_selected)
    mrn_combo_box.state(["readonly"])
    mrn_combo_box.grid(column=0, row=1, padx=(10, 10))
    # mrn_combo_box["values"] = get from API request

    mrn_label = ttk.Label(root, text="Patient MRN")
    mrn_label.grid(column=0, row=2, padx=(10, 12))

    mrn_data = tk.StringVar()
    mrn_box = ttk.Entry(root, width=10, textvariable=mrn_data)
    mrn_box.config(state='readonly')
    mrn_box.grid(column=0, row=3, padx=(10, 10), sticky='n')
    
    name_label = ttk.Label(root, text="Patient Name")
    name_label.grid(column=0, row=4, sticky='n')

    name_data = tk.StringVar()
    name_box = ttk.Entry(root, width=30, textvariable=name_data)
    name_box.config(state='readonly')
    name_box.grid(column=0, row=5, padx=(10, 10), sticky='n')
    
    ecg_label = ttk.Label(root, text="Latest ECG Trace")
    ecg_label.grid(column=0, row=7, pady=(10, 0))
    
    # Retrieve latest ECG image and display
    # ecg_image = load_and_resize_image("images/Transparent.png", 0.2)
    # ecg_label = ttk.Label(root, image=ecg_image)
    # ecg_label.grid(column=0, row=8, padx=(10, 10))
    
    hr_label = ttk.Label(root, text="HR (bpm):")
    hr_label.grid(column=0, row=9, padx = (0, 40), pady=(10, 10))
    
    hr_data = tk.StringVar()  # get from server
    hr_box = ttk.Entry(root, width=8, textvariable=hr_data)
    hr_box.config(state='readonly')
    hr_box.grid(column=0, row=9, columnspan=2, padx=(0, 300))
    
    time_label = ttk.Label(root, text="Time:")
    time_label.grid(column=0, row=10, padx = (0, 80), pady=(10, 10))
    
    time_data = tk.StringVar()  # get from server
    time_box = ttk.Entry(root, width=18, textvariable=time_data)
    time_box.config(state='readonly')
    time_box.grid(column=0, row=10, columnspan=2, padx=(0, 300))
    
    medical_img_label = ttk.Label(root, text="Saved Medical Images:")
    medical_img_label.grid(column=1, row=0, pady=(10, 0))
    
    med_img_selected = tk.StringVar()
    med_img_combo_box = ttk.Combobox(root, textvariable=med_img_selected)
    med_img_combo_box.state(["readonly"])
    med_img_combo_box.grid(column=1, row=1, padx=(10, 10), pady=(5, 100))
    # med_img_combo_box["values"] = get from API request
    
    # Placeholder medical image for now before server comm established
    med_img_placeholder = load_and_resize_image("images/Transparent.png", 0.2)
    med_img_label = ttk.Label(root, image=med_img_placeholder)
    med_img_label.grid(column=1, row=2, rowspan=4)

    historical_ecg_label = ttk.Label(root, text="Historical ECG Images:")
    historical_ecg_label.grid(column=1, row=6, pady=(30,0))
    
    hist_ecg_selected = tk.StringVar()
    hist_ecg_combo_box = ttk.Combobox(root, textvariable=hist_ecg_selected)
    hist_ecg_combo_box.state=(["readonly"])
    med_img_combo_box.grid(column=1, row=7)

    # Retrieve historical ECG selected and display
    # hist_ecg_image = load_and_resize_image("images/Transparent.png", 0.2)
    # hist_ecg_label = ttk.Label(root, image=hist_ecg_image)
    # hist_ecg_label.grid(column=1, row=8, rowspan=2, padx=(10, 10))

    save_med_img_btn = ttk.Button(root, text="SAVE MEDICAL IMAGE",
                                  command=save_med_img_cmd)
    save_med_img_btn.grid(column=2, row=4, padx=(0, 20))
    
    save_latest_ecg_btn = ttk.Button(root, text="SAVE LATEST ECG",
                                     command=save_latest_ecg_cmd)
    save_latest_ecg_btn.grid(column=2, row=8, padx=(0,20))
    
    save_hist_ecg_btn = ttk.Button(root, text="SAVE HISTORICAL ECG",
                                   command=save_hist_ecg_cmd)
    save_hist_ecg_btn.grid(column=2, row=9, padx=(0, 20))

    clear_btn = ttk.Button(root, text="CLEAR ALL",
                           command=clear_btn_cmd)
    clear_btn.grid(column=1, row=11, padx=(0, 20))

    exit_btn = ttk.Button(root, text="EXIT",
                          command=exit_btn_cmd)
    exit_btn.grid(column=2, row=11, padx=(0, 20), pady=(20, 20))

    root.mainloop()

if __name__ == "__main__":
    monitoring_gui()