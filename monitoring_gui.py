import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from patient_gui import load_and_resize_image, adj_factor

# Image toolbox imports
import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from skimage.io import imsave
import image_toolbox as it

# Server path
global path
path = "http://127.0.0.1:5000"

# Define global image and mrn variables
global med_img_str
global hist_ecg_img_str
global latest_ecg_img_str
global global_mrn


def enumerate_times(list):
    combo_list = []
    if len(list) != 0:
        for index, value in enumerate(list):
            combo_list.append("#" + str(index+1) + ": " + value)
    return combo_list


def enumerate_med_img(list):
    combo_list = []
    if len(list) != 0:
        for index, value in enumerate(list):
            combo_list.append("Medical Image #" + str(index+1))
    return combo_list


def monitoring_gui():

    def display_ndarray_img(img_ndarray):
        ndarray_img = Image.fromarray(img_ndarray)
        original_size = ndarray_img.size
        new_sizes = adj_factor(original_size)
        resized_img = ndarray_img.resize((new_sizes[0], new_sizes[1]))
        img_to_display = ImageTk.PhotoImage(resized_img)
        return img_to_display

    def display_server_img(b64_string, img_widget):
        # Convert b64 str to ImageTk
        img_ndarray = it.b64_to_ndarray(b64_string)
        img_to_display = display_ndarray_img(img_ndarray)

        # Assign ImageTk var to specified image label
        img_widget.configure(image=img_to_display)
        img_widget.image = img_to_display

    def save_file(b64_string, img_type):
        new_filename = filedialog.asksaveasfilename(defaultextension='.jpg')
        if new_filename is None:
            messagebox.showinfo("Cancel", (img_type + " save "
                                           "has been canceled"))
        it.b64_to_file(b64_string, new_filename)

    def save_med_img_cmd():
        global med_img_str
        save_file(med_img_str, "Medical image")

    def save_latest_ecg_cmd():
        global latest_ecg_img_str
        save_file(latest_ecg_img_str, "Latest ECG image")

    def save_hist_ecg_cmd():
        global hist_ecg_img_str
        save_file(hist_ecg_img_str, "Historical ECG image")

    def clear_btn_cmd():
        # Delete populated entry boxes/labels
        mrn_data.set('')
        name_data.set('')
        hr_data.set('')
        time_data.set('')
        med_img_combo_box.set('')
        med_img_combo_box["values"] = []
        hist_ecg_combo_box.set('')
        hist_ecg_combo_box["values"] = []

        # Return images to transparent
        tk_image = load_and_resize_image("images/Transparent.png")
        med_img_label.configure(image=tk_image)
        med_img_label.image = tk_image
        ecg_img_label.configure(image=tk_image)
        ecg_img_label.image = tk_image
        hist_ecg_label.configure(image=tk_image)
        hist_ecg_label.image = tk_image

    def get_mrn():
        r = requests.get(path + "/api/get_mrn")
        mrn_req_values = r.json()
        mrn_combo_box["values"] = mrn_req_values

    def db_get_req(mrn, info):
        global path
        end_route = ("/api/get_patient_from_database/{}/".
                     format(mrn) + info)
        r = requests.get(path + end_route)
        return r.json()

    def populate_hist_ecg_combo(mrn):
        timestamp_list = db_get_req(mrn, "receipt_timestamps")
        hist_combo_list = enumerate_times(timestamp_list)
        if len(hist_combo_list) != 0:
            hist_ecg_combo_box["values"] = hist_combo_list

    def populate_med_img_combo(mrn):
        med_img_list = db_get_req(mrn, "medical_image")
        med_combo_list = enumerate_med_img(med_img_list)
        if len(med_combo_list) != 0:
            med_img_combo_box["values"] = med_combo_list

    def on_patient_select(event):
        global global_mrn
        global latest_ecg_img_str
        clear_btn_cmd()

        # Display patient name and mrn
        mrn = mrn_selected.get()
        global_mrn = mrn
        mrn_data.set(mrn)
        pat_name = db_get_req(mrn, "patient_name")
        if pat_name is not None:
            name_data.set(pat_name)

        # Get and display latest HR and timestamp
        hr_list = db_get_req(mrn, "heart_rate")
        if len(hr_list) != 0:
            hr_data.set(hr_list[-1])

        time_list = db_get_req(mrn, "receipt_timestamps")
        if len(time_list) != 0:
            time_data.set(time_list[-1])

        # Get and display latest ECG img from server
        ecg_list = db_get_req(mrn, "ECG_trace")
        if len(ecg_list) != 0:
            latest_ecg = ecg_list[-1]
            display_server_img(latest_ecg, ecg_img_label)
            latest_ecg_img_str = latest_ecg

        # Populate image comboboxes
        populate_hist_ecg_combo(mrn)
        populate_med_img_combo(mrn)

    def on_ecg_select(event):
        global global_mrn
        global hist_ecg_img_str

        # Get index of selection and call from server
        index = hist_ecg_combo_box.current()
        ecg_list = db_get_req(global_mrn, "ECG_trace")
        ecg_to_display = ecg_list[index]
        display_server_img(ecg_to_display, hist_ecg_label)

        # Save globally for save button
        hist_ecg_img_str = ecg_to_display

    def on_med_img_select(event):
        global global_mrn
        global med_img_str

        # Get index of selection and call from server
        index = med_img_combo_box.current()
        med_list = db_get_req(global_mrn, "medical_image")
        med_to_display = med_list[index]
        display_server_img(med_to_display, med_img_label)

        # Save globally
        med_img_str = med_to_display

    def exit_btn_cmd():
        root.destroy()

    root = tk.Tk()
    root.title("Monitoring Station GUI Client")

    # Patient select label and patient mrn combobox
    patient_select_label = ttk.Label(root, text="Select Patient by MRN:")
    patient_select_label.grid(column=0, row=0, columnspan=2, pady=(10, 10))

    mrn_selected = tk.StringVar()
    mrn_combo_box = ttk.Combobox(root, textvariable=mrn_selected,
                                 postcommand=get_mrn)
    mrn_combo_box.bind("<<ComboboxSelected>>", on_patient_select)
    mrn_combo_box.state(["readonly"])
    mrn_combo_box.grid(column=0, row=1, columnspan=2,
                       padx=(10, 10), pady=(0, 10))

    # Patient select label and patient mrn combobox
    name_label = ttk.Label(root, text="Patient Name")
    name_label.grid(column=2, row=0, columnspan=2, pady=(10, 10))

    name_data = tk.StringVar()
    name_box = ttk.Entry(root, width=30, textvariable=name_data)
    name_box.config(state='readonly')
    name_box.grid(column=2, row=1, columnspan=2, padx=(10, 10), pady=(0, 10))

    # Patient mrn label and entry box
    mrn_label = ttk.Label(root, text="Patient MRN")
    mrn_label.grid(column=4, row=0, padx=(10, 10))

    mrn_data = tk.StringVar()
    mrn_box = ttk.Entry(root, width=8, textvariable=mrn_data)
    mrn_box.config(state='readonly')
    mrn_box.grid(column=4, row=1, padx=(10, 10), pady=(0, 10))

    # Latest ECG trace label and blank image
    ecg_label = ttk.Label(root, text="Latest ECG Trace")
    ecg_label.grid(column=0, row=2, columnspan=2, pady=(10, 0))

    # Retrieve latest ECG image and display
    ecg_image = load_and_resize_image("images/Transparent.png")
    ecg_img_label = ttk.Label(root, image=ecg_image)
    ecg_img_label.grid(column=0, row=4, columnspan=2, padx=(10, 10))

    # HR label, blank value, timestamp, and blank timestamp value
    hr_label = ttk.Label(root, text="HR (bpm):")
    hr_label.grid(column=0, row=5, padx=(10, 10), pady=(10, 10), sticky='e')

    hr_data = tk.StringVar()  # get from server
    hr_box = ttk.Entry(root, width=8, textvariable=hr_data)
    hr_box.config(state='readonly')
    hr_box.grid(column=1, row=5, padx=(0, 100))

    time_label = ttk.Label(root, text="Time:")
    time_label.grid(column=0, row=6, padx=(0, 20), pady=(10, 10), sticky='e')

    time_data = tk.StringVar()  # get from server
    time_box = ttk.Entry(root, width=18, textvariable=time_data)
    time_box.config(state='readonly')
    time_box.grid(column=1, row=6, padx=(0, 50))

    # Historical ECG label, combobox, and blank image
    historical_ecg_label = ttk.Label(root, text="Historical ECG Images:")
    historical_ecg_label.grid(column=2, row=2, columnspan=2, pady=(10, 10))

    hist_ecg_selected = tk.StringVar()
    hist_ecg_combo_box = ttk.Combobox(root, textvariable=hist_ecg_selected)
    hist_ecg_combo_box.bind("<<ComboboxSelected>>", on_ecg_select)
    hist_ecg_combo_box.state(["readonly"])
    hist_ecg_combo_box.grid(column=2, row=3, columnspan=2, pady=(0, 10))

    hist_ecg_image = load_and_resize_image("images/Transparent.png")
    hist_ecg_label = ttk.Label(root, image=hist_ecg_image)
    hist_ecg_label.grid(column=2, row=4, columnspan=2, padx=(10, 10))

    # Medical image label, combobox, blank image
    medical_img_label = ttk.Label(root, text="Saved Medical Images:")
    medical_img_label.grid(column=4, row=2, pady=(10, 10))

    med_img_selected = tk.StringVar()
    med_img_combo_box = ttk.Combobox(root, textvariable=med_img_selected)
    med_img_combo_box.bind("<<ComboboxSelected>>", on_med_img_select)
    med_img_combo_box.state(["readonly"])
    med_img_combo_box.grid(column=4, row=3, padx=(10, 10), pady=(0, 10))
    med_img_combo_box["values"] = []

    # Placeholder medical image
    med_img_placeholder = load_and_resize_image("images/Transparent.png")
    med_img_label = ttk.Label(root, image=med_img_placeholder)
    med_img_label.grid(column=4, row=4, padx=(10, 10), pady=(0, 10))

    # Action buttons
    save_med_img_btn = ttk.Button(root, text="SAVE MEDICAL IMAGE",
                                  command=save_med_img_cmd)
    save_med_img_btn.grid(column=4, row=8, padx=(0, 20), pady=(20, 0))

    save_latest_ecg_btn = ttk.Button(root, text="SAVE LATEST ECG",
                                     command=save_latest_ecg_cmd)
    save_latest_ecg_btn.grid(column=0, row=8, columnspan=2, padx=(0, 20),
                             pady=(20, 0))

    save_hist_ecg_btn = ttk.Button(root, text="SAVE HISTORICAL ECG",
                                   command=save_hist_ecg_cmd)
    save_hist_ecg_btn.grid(column=2, row=8, columnspan=2, padx=(0, 20),
                           pady=(20, 0))

    clear_btn = ttk.Button(root, text="CLEAR ALL",
                           command=clear_btn_cmd)
    clear_btn.grid(column=2, row=9, padx=(0, 20))

    exit_btn = ttk.Button(root, text="EXIT",
                          command=exit_btn_cmd)
    exit_btn.grid(column=3, row=9, padx=(0, 20), pady=(20, 20))

    root.mainloop()


if __name__ == "__main__":
    monitoring_gui()
