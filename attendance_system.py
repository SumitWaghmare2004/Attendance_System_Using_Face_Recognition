#========================================================================================================================================================================
#                                     Completed Attendance App Code Name & Current Time With (Co-ordinate's as a Dataset) 
#========================================================================================================================================================================
import cv2
import numpy as np
import os
import json
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

# Initialize tkinter
root = Tk()
root.title("Attendance System")

# Load the background image
background_image = Image.open("Resources/background.png")
background_image = background_image.resize((1280, 720), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Load the image to display after marking attendance
marked_image_path = "Resources/3.png"
marked_image = Image.open(marked_image_path)

# Create a white background of 640x495 pixels
background = Image.new('RGB', (640, 495), (255, 255, 255))

# Calculate the position to paste the marked image at the center
marked_image_width, marked_image_height = marked_image.size
center_x = (640 - marked_image_width) // 2
center_y = (495 - marked_image_height) // 2

# Paste the marked image onto the background at the center
background.paste(marked_image, (center_x, center_y))

marked_photo = ImageTk.PhotoImage(background)

# Set up the GUI elements
canvas = Canvas(root, width=1280, height=720)
canvas.pack()
canvas.create_image(0, 0, anchor=NW, image=background_photo)

# Adjust positions for the elements
video_label = Label(root)
canvas.create_window(50, 150, anchor=NW, window=video_label)

# Title label
title_label = Label(root, text="Attendance Status", font=("Algerian", 15, "bold"), bg='white', fg='black')
canvas.create_window(1007, 75, anchor="center", window=title_label)

# Info label
info_label = Label(root, text="Information will be displayed here.", font=("Helvetica", 16), bg='white')
canvas.create_window(820, 150, anchor=NW, window=info_label)

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Initialize face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load face coordinates and names from JSON file
def load_face_coordinates():
    try:
        with open('coordinates_data.json', 'r') as file:
            data = json.load(file)
            # Ensure all coordinates are integers
            return {name: [list(map(int, coords)) for coords in coords_list] for name, coords_list in data.items()}
    except FileNotFoundError:
        print("coordinates_data.json not found.")
        return {}

face_coordinates = load_face_coordinates()

# Load additional person info
def load_person_info():
    person_info = {}
    try:
        with open('person_info.txt', 'r') as file:
            for line in file:
                if ':' in line:
                    name, info = line.split(':', 1)
                    person_info[name.strip()] = info.strip()
    except FileNotFoundError:
        print("person_info.txt not found.")
    return person_info

person_info = load_person_info()

unrecognized_shown = False  # Flag to show error message only once
attendance_marked = False  # Flag to track if attendance is already marked

def mark_attendance(name):
    with open("attendance.txt", "a") as f: 
        f.write(f"{name}, {datetime.now()}\n")

def process_frame():
    global unrecognized_shown, attendance_marked, video_capture

    ret, frame = video_capture.read()
    if not ret:
        return

    frame = cv2.resize(frame, (640, 495))

    if attendance_marked:
        # Stop the webcam feed
        video_capture.release()
        cv2.destroyAllWindows()
        
        # Display the marked image
        video_label.imgtk = marked_photo
        video_label.configure(image=marked_photo)
        return  # Skip the face detection part

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    detected_any_face = False
    for (x, y, w, h) in faces:
        detected = False

        # Check if the detected face coordinates match any in the JSON data
        for name, coords_list in face_coordinates.items():
            for coords in coords_list:
                cx, cy, cw, ch = coords
                if (abs(x - cx) < 20 and abs(y - cy) < 20 and
                    abs(w - cw) < 20 and abs(h - ch) < 20):
                    info = person_info.get(name, None)
                    if info:
                        info_label.config(text=f"\n\nName: {name}\n\n\tTime: {datetime.now().strftime('%H:%M:%S')}\n\n{info}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n Have a Nice Day!")
                    else:
                        info_label.config(text=f"\n\nName: {name}\n\nTime: {datetime.now().strftime('%H:%M:%S')}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t Have a Nice Day!")
                    mark_attendance(name)
                    attendance_marked = True
                    unrecognized_shown = False
                    detected = True
                    detected_any_face = True
                    break
            if detected:
                break

        if not detected:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "Unknown", (x + 6, y+h - 6), font, 1.0, (255, 255, 255), 1)

    if not detected_any_face and not unrecognized_shown:
        messagebox.showerror("Error", "Face not recognized!")
        unrecognized_shown = True

    # Display the resulting frame
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    video_label.imgtk = image
    video_label.configure(image=image)

    video_label.after(10, process_frame)

# Start the frame processing
process_frame()

# Start the GUI event loop
root.mainloop()


#========================================================================================================================================================================
#                                        Completed Attendance App Code Name & Current Time With (Image's as a Dataset) 
#========================================================================================================================================================================


# import cv2
# import numpy as np
# import os
# from tkinter import *
# from tkinter import messagebox
# from PIL import Image, ImageTk
# from datetime import datetime

# # Initialize tkinter
# root = Tk()
# root.title("Attendance System")

# # Load the background image
# background_image = Image.open("Resources/background.png")
# background_image = background_image.resize((1280, 720), Image.Resampling.LANCZOS)
# background_photo = ImageTk.PhotoImage(background_image)

# # Load the image to display after marking attendance
# marked_image_path = "Resources/3.png"
# marked_image = Image.open(marked_image_path)

# # Create a white background of 640x495 pixels
# background = Image.new('RGB', (640, 495), (255, 255, 255))

# # Calculate the position to paste the marked image at the center
# marked_image_width, marked_image_height = marked_image.size
# center_x = (640 - marked_image_width) // 2
# center_y = (495 - marked_image_height) // 2

# # Paste the marked image onto the background at the center
# background.paste(marked_image, (center_x, center_y))

# marked_photo = ImageTk.PhotoImage(background)

# # Set up the GUI elements
# canvas = Canvas(root, width=1280, height=720)
# canvas.pack()
# canvas.create_image(0, 0, anchor=NW, image=background_photo)

# # Adjust positions for the elements
# video_label = Label(root)
# canvas.create_window(50, 150, anchor=NW, window=video_label)

# # Title label
# title_label = Label(root, text="WELCOME TO PUG-ARCH TECHNOLOGY", font=("Algerian",15, "bold"), bg='white', fg='black')
# canvas.create_window(1007, 75, anchor="center", window=title_label)

# # Info label
# info_label = Label(root, text="Information will be displayed here.", font=("Helvetica", 16), bg='white')
# canvas.create_window(820, 150, anchor=NW, window=info_label)

# # Initialize webcam
# video_capture = cv2.VideoCapture(0)

# # Load the known faces and train the recognizer
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# def train_recognizer():
#     faces = []
#     labels = []
#     label_map = {}
#     current_label = 0

#     for filename in os.listdir('known_faces'):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             image_path = os.path.join('known_faces', filename)
#             image = cv2.imread(image_path)
#             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#             faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#             for (x, y, w, h) in faces_detected:
#                 face_roi = gray[y:y+h, x:x+w]
#                 faces.append(face_roi)
#                 labels.append(current_label)
#             person_name = os.path.splitext(filename)[0]
#             label_map[current_label] = person_name
#             current_label += 1

#     recognizer.train(faces, np.array(labels))
#     return label_map

# def load_person_info():
#     person_info = {}
#     try:
#         with open('person_info.txt', 'r') as file:
#             for line in file:
#                 if ':' in line:
#                     name, info = line.split(':', 1)
#                     person_info[name.strip()] = info.strip()
#     except FileNotFoundError:
#         print("person_info.txt not found.")
#     return person_info

# label_map = train_recognizer()
# person_info = load_person_info()

# unrecognized_shown = False  # Flag to show error message only once
# attendance_marked = False  # Flag to track if attendance is already marked

# def mark_attendance(name):
#     with open("attendance.txt", "a") as f:
#         f.write(f"{name}, {datetime.now()}\n")

# def process_frame():
#     global unrecognized_shown, attendance_marked, video_capture

#     ret, frame = video_capture.read()
#     if not ret:
#         return

#     frame = cv2.resize(frame, (640, 495))

#     if attendance_marked:
#         # Stop the webcam feed
#         video_capture.release()
#         cv2.destroyAllWindows()
        
#         # Display the marked image
#         video_label.imgtk = marked_photo
#         video_label.configure(image=marked_photo)
#         return  # Skip the face detection part

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#     face_names = []
#     for (x, y, w, h) in faces:
#         face_roi = gray[y:y+h, x:x+w]
#         label, confidence = recognizer.predict(face_roi)
#         name = label_map[label] if confidence < 60 else "Unknown"  # Adjust threshold for better accuracy
#         face_names.append(name)

#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), (0, 255, 0), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (x + 6, y+h - 6), font, 1.0, (255, 255, 255), 1)

#         if name != "Unknown":
#             info = person_info.get(name, None)
#             if info:
#                 info_label.config(text=f"\n\nName: {name}\n\n\tTime: {datetime.now().strftime('%H:%M:%S')}\n\n{info}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nHave a Nice Day!")
#             else:
#                 info_label.config(text=f"\n\nName: {name}\n\nTime: {datetime.now().strftime('%H:%M:%S')}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\tHave a Nice Day!")
#             mark_attendance(name)
#             attendance_marked = True  # Set the flag when a face is recognized
#             unrecognized_shown = False  # Reset the flag when a face is recognized
#         else:
#             if not unrecognized_shown:
#                 messagebox.showerror("Error", "Face not recognized!")
#                 unrecognized_shown = True  # Set the flag to prevent multiple pop-ups

#     # Display the resulting frame
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     image = Image.fromarray(image)
#     image = ImageTk.PhotoImage(image)
#     video_label.imgtk = image
#     video_label.configure(image=image)

#     video_label.after(10, process_frame)

# # Start the frame processing
# process_frame()

# # Start the GUI event loop
# root.mainloop()

