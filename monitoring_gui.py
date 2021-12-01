import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from patient_gui import load_and_resize_image

# Image toolbox imports
import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from skimage.io import imsave


def monitoring_gui():

    def display_server_img(b64_string, img_widget):
        '''# Convert b64 str to ndarray
        image_bytes = base64.b64decode(b64_string)
        image_buf = io.BytesIO(image_bytes)
        img_ndarray = mpimg.imread(image_buf, format='JPG')

        # Plot ndarray using matplotlib
        fig = plt.Figure(figsize=(3,2), dpi=100) # set fig to 300x200
        fig.add_subplot(111)
        tk_img = FigureCanvasTkAgg(fig, root)
        img_widget.configure(image=tk_img)
        img_widget.image = tk_img'''
        pass

    def save_med_img_cmd():
        new_filename = filedialog.asksaveasfile(mode='w',
                                                defaultextension='.jpg')
        if new_filename is None:
            messagebox.showinfo("Cancel", ("Medical image save "
                                           "has been canceled"))
        image_bytes = base64.b64decode(b64_string)
        with open(new_filename, "wb") as out_file:
            out_file.write(image_bytes)

    def save_latest_ecg_cmd():
        new_filename = filedialog.asksaveasfile(mode='w',
                                                defaultextension='.jpg')
        if new_filename is None:
            messagebox.showinfo("Cancel", ("ECG image save "
                                           "has been canceled"))
        image_bytes = base64.b64decode(b64_string)
        with open(new_filename, "wb") as out_file:
            out_file.write(image_bytes)

    def save_hist_ecg_cmd():
        new_filename = filedialog.asksaveasfile(mode='w',
                                                defaultextension='.jpg')
        if new_filename is None:
            messagebox.showinfo("Cancel", ("Historical ECG image save "
                                           "has been canceled"))
        image_bytes = base64.b64decode(b64_string)
        with open(new_filename, "wb") as out_file:
            out_file.write(image_bytes)

    def clear_btn_cmd():
        mrn_combo_box.set('')
        mrn_box.delete(0, 10)
        name_box.delete(0, 100)
        hr_box.delete(0, 10)
        time_box.delete(0, 25)
        med_img_combo_box.set('')
        hist_ecg_combo_box.set('')

        # Return images to transparent
        tk_image = load_and_resize_image("images/Transparent.png")
        med_img_label.configure(image=tk_image)
        med_img_label.image = tk_image
        ecg_img_label.configure(image=tk_image)
        ecg_img_label.image = tk_image
        hist_ecg_label.configure(image=tk_image)
        hist_ecg_label.image = tk_image

    def on_patient_select(event):
        clear_btn_cmd()
        # name_data.set(pat_list[0][0])  # Assuming pat name stored first
        # mrn_data.set(pat_list[0][1])   # Assuming pat mrn stored second
        # hr_data.set(pat_list[0][3])
        # time_data.set(pat_list[0][4])

        # Get latest ECG img from server
        # display_server_img(pat_list[0][2], ecg_img_label)
        pass

    def on_ecg_select(event):
        # ecg_str = hist_ecg_combo_box.get()
        # request b64 from server
        # display_server_img
        pass

    def on_med_img_select(event):
        # med_img_str = med_img_combo_box.get()
        # request b64 from server
        # display_server_img
        pass

    def exit_btn_cmd():
        root.destroy()

    root = tk.Tk()
    root.title("Monitoring Station GUI Client")

    patient_select_label = ttk.Label(root, text="Select Patient by MRN:")
    patient_select_label.grid(column=0, row=0, columnspan=2, pady=(10, 10))

    mrn_selected = tk.StringVar()
    mrn_combo_box = ttk.Combobox(root, textvariable=mrn_selected)
    mrn_combo_box.state(["readonly"])
    mrn_combo_box.grid(column=0, row=1, columnspan=2,
                       padx=(10, 10), pady=(0, 10))

    # mrn_combo_box["values"] = get from API request

    name_label = ttk.Label(root, text="Patient Name")
    name_label.grid(column=2, row=0, columnspan=2, pady=(10, 10))

    name_data = tk.StringVar()
    name_box = ttk.Entry(root, width=30, textvariable=name_data)
    name_box.config(state='readonly')
    name_box.grid(column=2, row=1, columnspan=2, padx=(10, 10), pady=(0, 10))

    mrn_label = ttk.Label(root, text="Patient MRN")
    mrn_label.grid(column=4, row=0, padx=(10, 10))

    mrn_data = tk.StringVar()
    mrn_box = ttk.Entry(root, width=8, textvariable=mrn_data)
    mrn_box.config(state='readonly')
    mrn_box.grid(column=4, row=1, padx=(10, 10), pady=(0, 10))

    ecg_label = ttk.Label(root, text="Latest ECG Trace")
    ecg_label.grid(column=0, row=2, columnspan=2, pady=(10, 0))

    # Retrieve latest ECG image and display
    ecg_image = load_and_resize_image("images/Transparent.png")
    ecg_img_label = ttk.Label(root, image=ecg_image)
    ecg_img_label.grid(column=0, row=4, columnspan=2, padx=(10, 10))

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

    medical_img_label = ttk.Label(root, text="Saved Medical Images:")
    medical_img_label.grid(column=4, row=2, pady=(10, 10))

    med_img_selected = tk.StringVar()
    med_img_combo_box = ttk.Combobox(root, textvariable=med_img_selected)
    med_img_combo_box.state(["readonly"])
    med_img_combo_box.grid(column=4, row=3, padx=(10, 10), pady=(0, 10))
    # med_img_combo_box["values"] = get from API request

    # Placeholder medical image for now before server comm established
    med_img_placeholder = load_and_resize_image("images/Transparent.png")
    med_img_label = ttk.Label(root, image=med_img_placeholder)
    med_img_label.grid(column=4, row=4, pady=(0, 10))

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
