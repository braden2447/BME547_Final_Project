import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from ECG_analysis import read_data, manipulate_data, filter_data
from api.shared_methods import str_to_int
import image_toolbox as it
import os

# Server path
path = "http://vcm-23156.vm.duke.edu:5000"

# Declare global variable to hold med img and ecg filenames
global med_img_filename
med_img_filename = None


def adj_factor(original_size):
    """Calculates adjustment factor to resize images to 300x200

    This function uses the input tuple of original image size
    to determine image orientation, calculate an adjustment factor,
    and return a list of new width and height.

    Args:
        original_size (tuple): tuple of integers of orig width, height

    Returns:
        list: list of integers with newly-sized width, height
    """
    # Determine if vertical or horizontal pic, which way to scale
    if original_size[0] > original_size[1]:   # horizontal
        adj_factor = 300/original_size[0]
    else:                                     # vertical or square
        adj_factor = 200/original_size[1]
    new_sizes = []
    new_sizes.append(round(original_size[0] * adj_factor))  # New width
    new_sizes.append(round(original_size[1] * adj_factor))  # New height
    return new_sizes


def load_and_resize_image(filename):
    """Opens image file and resizes based on adj factor

    This function opens a specified file as a PIL image. The
    adj_factor function is used to resize the image, and the
    resulting image is converted to a Tk PhotoImage and returned.

    Args:
        filename (str): string containing filename of image to load

    Returns:
        ImageTk.PhotoImage: resized Tk PhotoImage
    """
    pil_image = Image.open(filename)
    original_size = pil_image.size
    new_sizes = adj_factor(original_size)
    resized_image = pil_image.resize((new_sizes[0], new_sizes[1]))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image


def analyze_ecg(filename):
    """Analyzes ECG data file to save ECG trace and return heart rate

    This function calls the ECG_analysis module to analyze a selected
    ECG data file, plot and save the resulting ECG trace (as filename
    ecg_trace.jpg), and return the analyzed heart rate as an integer.

    Args:
        filename (str): string containing filename of ECG data to analyze

    Returns:
        int: integer containing average heart rate value in bpm
    """
    metrics = []  # initialize metrics list for data storage
    test_data = read_data(filename)  # open file and convert to text format
    time, voltage = manipulate_data(test_data)  # produce time, voltage lists
    metrics_list = filter_data(time, voltage, metrics)
    return metrics_list[1]


def create_pat_dict(mrn, name, hr, ecg, med):
    """Creates patient info dict to post to database

    This function scans the input variables to create a dictionary
    containing only keys that have associated values to be stored
    and posted to the patient database.

    Args:
        mrn (int): integer of patient medical record number
        name (str, None): string containing patient name if present
        hr (int, None): integer containing heart rate value if present
        ecg (list, None): list of b64 image strings if present
        med (list, None): list of b64 med image strings if present

    Returns:
        dict: patient dictionary containing keys of input patient info,
              containing at least an "MRN" key
    """
    pat_dict = {"MRN": mrn}
    if name != "":
        pat_dict["patient_name"] = name
    if ecg is not None:
        pat_dict["ECG_trace"] = ecg
        pat_dict["heart_rate"] = hr
    if med is not None:
        pat_dict["medical_image"] = med
    return pat_dict


def patient_dict_upload(mrn, name, hr, ecg, med):
    """Verifies MRN input and creates POST request of patient info

    This function first verifies that the input MRN was an integer
    then calls the create_pat_dict function to create a patient info
    dictionary to include as the json of the "post_new_patient_info"
    POST request.

    Args:
        mrn (int): integer of patient medical record number
        name (str, None): string containing patient name if present
        hr (int, None): integer containing heart rate value if present
        ecg (list, None): list of b64 image strings if present
        med (list, None): list of b64 med image strings if present

    Returns:
        None
    """
    check = str_to_int(mrn)
    if(not check[1]):
        messagebox.showinfo("Error", "MRN must be an integer value")
        return  # if user tries to input non-integer MRN
    mrn_int = check[0]

    # Create patient dictionary to upload
    pat_dict = create_pat_dict(mrn_int, name, hr, ecg, med)

    # API route
    r = requests.post(path + "/api/post_new_patient_info", json=pat_dict)
    print(r.status_code)
    print(r.text)


def patient_gui():
    """GUI function to create Tk loop for patient-side GUI

    This function contains the widget outline for the patient-side
    GUI as well as embedded functions for all the GUI functionality.
    The user is able to connect to a MongoDB database via a server to
    access, display, and save patient info such as name, MRN,
    ECG traces, and medical images.

    Args:
        None

    Returns:
        None
    """

    def medical_img_btn_cmd():
        """Button command to display selected med image file

        Activated upon "Select medical image" button press, this function
        opens a filedialog box and allows the user to select a local medical
        image file. This image is then loaded, resized, and displayed
        in the GUI.

        Args:
            None

        Returns:
            None
        """
        filename = filedialog.askopenfilename(initialdir="BME547_repos")
        if filename == "":
            messagebox.showinfo("Cancel", "You canceled the image load")
            return  # if user cancels picture file selection

        # Open image, resize, return tk image
        tk_image = load_and_resize_image(filename)
        med_img_label.configure(image=tk_image)
        med_img_label.image = tk_image  # saving this variable

        # Save filename to global variable for img upload
        global med_img_filename
        med_img_filename = filename

    def ecg_btn_cmd():
        """Button command to analyze and display ECG data file

        Activated upon "Select ECG data file" button press, this function
        opens a filedialog box and allows the user to select a local ECG
        data file. This file is then analyzed using the ECG_analysis module
        to display the heart rate and ECG trace.

        Args:
            None

        Returns:
            None
        """
        filename = filedialog.askopenfilename()
        if filename == "":
            messagebox.showinfo("Cancel", "You canceled ECG file selection")
            return  # if user cancels ECG data file selection

        # Analyze file via old ecg analysis code
        hr = analyze_ecg(filename)

        # Return HR value and ECG trace
        hr_value_label.configure(text=hr)
        hr_value_label.text = hr

        ecg_tk_image = load_and_resize_image("ecg_trace.jpg")
        ecg_img_label.configure(image=ecg_tk_image)
        ecg_img_label.image = ecg_tk_image

    def upload_btn_cmd():
        """Button command to upload displayed patient info to database

        Activated upon "UPLOAD" button press, this function interprets the
        current GUI state to produce a dictionary containing keys and values
        to all corresponding text and images displayed. If at least a MRN is
        present, a POST request is made through the patient_dict_upload
        function.

        Args:
            None

        Returns:
            None
        """
        # Send json dict to server to store in database
        name = name_data.get()
        mrn = mrn_data.get()
        if mrn == "":
            messagebox.showinfo("Error",
                                "Must enter MRN to upload patient data")
            return

        # Check if images exist, convert to b64str
        if os.path.exists("ecg_trace.jpg"):  # ECG file exists
            ecg_upload_str = it.file_to_b64("ecg_trace.jpg")
            hr = int(hr_value_label.cget("text"))
        else:
            ecg_upload_str = None
            hr = None

        global med_img_filename
        if med_img_filename is None:         # Blank med img
            med_upload_str = None
        else:
            med_upload_str = it.file_to_b64(med_img_filename)

        # Dict creation and server function call
        patient_dict_upload(mrn, name, hr,
                            ecg_upload_str, med_upload_str)

    def clear_btn_cmd():
        """Button command to clear all fields

        Activated upon "CLEAR ALL" button click, this function
        clears the entire GUI of images and textbox data.

        Args:
            None

        Returns:
            None
        """
        name_box.delete(0, 100)
        mrn_box.delete(0, 10)
        # Add if statement checking if ECG trace and HR label exist

        # Return med image to transparent image
        med_img_label.configure(image=med_img_placeholder)
        med_img_label.image = med_img_placeholder
        global med_img_filename
        med_img_filename = None

        # Clear HR value and ecg image
        blank = ''
        hr_value_label.configure(text=blank)
        hr_value_label.text = blank

        ecg_img_label.configure(image=ecg_img_placeholder)
        ecg_img_label.image = ecg_img_placeholder

        # Delete ECG trace file
        if os.path.exists("ecg_trace.jpg"):
            os.remove("ecg_trace.jpg")

    def exit_btn_cmd():
        """Button command to exit GUI and quit code

        Activated upon "EXIT" button press, this function destroys
        the Tk loop and exits the GUI, quitting the code.

        Args:
            None

        Returns:
            None
        """
        root.destroy()

    root = tk.Tk()
    root.title("Patient-Side GUI Client")

    # Patient name label/box
    name_label = ttk.Label(root, text="Patient Name")
    name_label.grid(column=0, row=0, pady=(10, 0))

    name_data = tk.StringVar()
    name_box = ttk.Entry(root, width=30, textvariable=name_data)
    name_box.grid(column=0, row=1, padx=(10, 10), pady=(5, 20))

    # Patient MRN label/box
    mrn_label = ttk.Label(root, text="Patient MRN")
    mrn_label.grid(column=2, row=0, columnspan=2, padx=(10, 12), pady=(10, 0))

    mrn_data = tk.StringVar()
    mrn_box = ttk.Entry(root, width=10, textvariable=mrn_data)
    mrn_box.grid(column=2, row=1, columnspan=2, padx=(10, 10), pady=(5, 20))

    # Medical image label and blank medical image
    medical_img_label = ttk.Label(root, text="Medical Image")
    medical_img_label.grid(column=0, row=2)

    med_img_placeholder = load_and_resize_image("images/Transparent.png")
    med_img_label = ttk.Label(root, image=med_img_placeholder)
    med_img_label.grid(column=0, row=4, columnspan=2, padx=(10, 10))

    # ECG trace label and blank ECG image
    ecg_data_label = ttk.Label(root, text="Analyze ECG Data")
    ecg_data_label.grid(column=2, row=2, columnspan=2)

    ecg_img_placeholder = load_and_resize_image("images/Transparent.png")
    ecg_img_label = ttk.Label(root, image=ecg_img_placeholder)
    ecg_img_label.grid(column=2, row=4, columnspan=2, padx=(0, 20))

    # HR label and blank value label
    hr_label = ttk.Label(root, text="HR (bpm):")
    hr_label.grid(column=2, row=5, columnspan=2, padx=(0, 25), pady=(20, 20))

    hr_value_label = ttk.Label(root, text='')
    hr_value_label.grid(column=3, row=5, padx=(0, 75), pady=(20, 20))

    # Action buttons
    medical_img_btn = ttk.Button(root, text="Select image file",
                                 command=medical_img_btn_cmd)
    medical_img_btn.grid(column=0, row=3, padx=(10, 10), pady=(5, 20))

    ecg_data_btn = ttk.Button(root, text="Select ECG data file",
                              command=ecg_btn_cmd)
    ecg_data_btn.grid(column=2, row=3, columnspan=2,
                      padx=(10, 10), pady=(5, 20))

    upload_btn = ttk.Button(root, text="UPLOAD",
                            command=upload_btn_cmd)
    upload_btn.grid(column=2, row=6, padx=(27, 0))

    clear_btn = ttk.Button(root, text="CLEAR ALL",
                           command=clear_btn_cmd)
    clear_btn.grid(column=3, row=6, padx=(40, 20))

    exit_btn = ttk.Button(root, text="EXIT",
                          command=exit_btn_cmd)
    exit_btn.grid(column=2, row=7, columnspan=2, padx=(15, 8), pady=(20, 20))

    root.mainloop()


if __name__ == "__main__":
    patient_gui()
