[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/BME547-Fall2021/final-project-anuj-braden/blob/main/LICENSE.txt)
![GitHub Actions Status](https://github.com/BME547-Fall2021/final-project-anuj-braden/actions/workflows/pytest_runner.yml/badge.svg)

# BME 547 Final Project

## Authors: Braden Garrison and Anuj Som

## Due: 12/5/21

## Repository Purpose

This patient monitoring client/server project repository serves as a total Patient Monitoring 
System containing patient-side and monitoring station GUI client interactions through a server-accessed 
MongoDB patient database. From the patient-side GUI, users are able to upload patient names, medical record numbers (MRNs), 
locally-stored medical images, and ECG traces and heart rate data analyzed in real time from locally-stored 
ECG data files. From the monitoring station GUI, users are able to retrieve the uploaded patient data from the 
patient database via server access and save important medical and ECG images.

This server is running on a virtual machine with the following hostname and port:

```Enter vcm address```

If the user decides to run this server locally, first activate the virtual environment containing the packages listed in 
```requirements.txt``` then type the following command into the command line:

```python ecg_server.py```

A video demo of these client programs in action can be found at this Duke Box link [here](https://duke.app.box.com/folder/151464609081).


## GUI Instruction Manual

### Patient-Side GUI

![Patient-Side GUI](https://github.com/braden2447/final-project-anuj-braden/blob/main/images/Patient_side_GUI.png?raw=true)

Upon patient-side GUI deployment, the above image is the starting interface the user will see.
The user has the option to manually enter the patient name and patient MRN.
The ```Select image file``` button can be pressed to select a medical image to display directly beneath the button on the GUI.
The ```Select ECG data file``` button can be pressed to select an Excel file of raw time and voltage ECG values to be analyzed.
Upon analysis, the resultant ECG trace will be displayed below the button, and the analyzed heart rate in beats per minute will 
be displayed next to the ```HR (bpm):``` label. 

To clear all entered/analyzed data from the interface, the user can click the ```CLEAR ALL``` button. This will return the GUI to 
its original state.

To upload all entered/analyzed data to the patient MongoDB database, the user can click the ```UPLOAD``` button.
**NOTE: A proper upload can only be completed if at least a medical record number has been entered.**

To shut down the program and exit the GUI, the user can click the ```EXIT``` button.


### Monitoring Station GUI

![Monitoring Station GUI](https://github.com/braden2447/final-project-anuj-braden/blob/main/images/Monitoring_GUI.png?raw=true)

Upon monitoring station GUI deployment, the above image is the starting interface the user will see.
The user can select patients by their MRN from the patient database using the upper-left dropdown box.
This dropdown box is automatically synced to the database by short, periodic API requests that constantly keep it up to date 
with the latest patient info. 
Upon patient selection, the patient name and MRN will be displayed in their respective entry boxes. The latest ECG trace for that patient, 
along with the analyzed heart rate value and timestamp of that trace, will be displayed on the left-hand side of the interface. 
The user can then select from updated lists of historical ECG images and saved medical images from their respective dropdown boxes.
Upon selection, these images will be displayed on the GUI below their labels.
**NOTE: Upon new patient selection, any displayed historical ECG and medical images will be deleted, and the new patient name, MRN, and latest ECG will be displayed.**

To save any of the displayed images locally, the user can click one of the following buttons: ```SAVE LATEST ECG```, ```SAVE HISTORICAL ECG```, 
or ```SAVE MEDICAL IMAGE```.

To clear all displayed patient info from the interface, the user can click the ```CLEAR ALL``` button.

To shut down the program and exit the GUI, the user can click the ```EXIT``` button.

## Server API Reference Guide


## MongoDB Database Structure
