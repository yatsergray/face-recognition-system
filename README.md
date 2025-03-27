# Face Recognition System

## Overview

This project is a face recognition system that utilizes OpenCV and face\_recognition libraries to detect and recognize faces. It consists of two main components:

1. **face\_preparation.py** – Used to encode and store face data in a PostgreSQL database.
2. **face\_recognition.py** – Captures video from a webcam, detects faces, and attempts to recognize them against stored face data.

## Features

- Face encoding and storage in a PostgreSQL database.
- Real-time face detection and recognition using OpenCV.
- Basic UI for login and registration using Tkinter.

## How It Works

1. `face_preparation.py`:

   - Loads an image and encodes the face into numerical data.
   - Stores the encoded face data in the PostgreSQL database.

2. `face_recognition.py`:

   - Captures video frames from the webcam.
   - Detects faces in the video feed.
   - Compares detected faces with stored encodings.
   - If a match is found, a login frame appears; otherwise, a registration frame appears.