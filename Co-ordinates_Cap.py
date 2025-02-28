#========================================================================================================================================================================
#                      Detecting the face Co-ordinate's and Stored it into Accepted Attendance System Format.. 
#========================================================================================================================================================================
import cv2
import json
import numpy as np
from tkinter import Tk, simpledialog

# Initialize face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Function to save coordinates data to JSON file
def save_coordinates(name, coords):
    # Convert numpy types to native Python types
    coords = [int(coords['x']), int(coords['y']), int(coords['w']), int(coords['h'])]

    # Load existing data
    try:
        with open('coordinates_data.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}


    # Add new coordinates
    if name not in data:
        data[name] = []
    data[name].append(coords)

    # Save data back to file
    with open('coordinates_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Function to get name from the user
def get_name():
    root = Tk()
    root.withdraw()  # Hide the main window
    name = simpledialog.askstring("Input", "Enter name for the detected face:")
    root.destroy()
    return name

def main():
    coordinates_saved = False  # Flag to indicate if coordinates have been saved

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0 and not coordinates_saved:
            # Use the coordinates of the first detected face
            x, y, w, h = faces[0]
            coords = {'x': x, 'y': y, 'w': w, 'h': h}

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"({x}, {y}, {w}, {h})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Save coordinates on pressing 's'
            if cv2.waitKey(1) & 0xFF == ord('s'):
                name = get_name()
                if name:
                    save_coordinates(name, coords)
                    print(f"Coordinates saved for {name}: ({x}, {y}, {w}, {h})")
                    coordinates_saved = True  # Set flag to indicate that coordinates have been saved

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop on pressing 'q' or if coordinates have been saved
        if cv2.waitKey(1) & 0xFF == ord('q') or coordinates_saved:
            break

    # Release the capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
