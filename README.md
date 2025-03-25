# Face Recognition System

## Overview

This project is a face recognition system that utilizes OpenCV and face\_recognition libraries to detect and recognize faces. It consists of two main components:

1. **face\_preparation.py** – Used to encode and store face data in a PostgreSQL database.
2. **face\_recognition.py** – Captures video from a webcam, detects faces, and attempts to recognize them against stored face data.

## Features

- Face encoding and storage in a PostgreSQL database.
- Real-time face detection and recognition using OpenCV.
- Basic UI for login and registration using Tkinter.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- PostgreSQL
- Required Python libraries (install via pip):

```sh
pip install opencv-python numpy face-recognition psycopg2 tkinter
```

### Database Setup

1. Create a PostgreSQL database:

```sql
CREATE DATABASE face_recognition_db;
```

2. Create a table for storing face data:

```sql
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    face_image BYTEA
);
```

## Usage

### 1. Adding a New Face

Run the `face_preparation.py` script to encode and store a new person's face:

```sh
python face_preparation.py
```

Modify the script to change the person's name and image file path before running.

### 2. Running Face Recognition

Run the `face_recognition.py` script to start real-time face recognition:

```sh
python face_recognition.py
```

Press `q` to quit the recognition process.

## How It Works

1. `face_preparation.py`:

   - Loads an image and encodes the face into numerical data.
   - Stores the encoded face data in the PostgreSQL database.

2. `face_recognition.py`:

   - Captures video frames from the webcam.
   - Detects faces in the video feed.
   - Compares detected faces with stored encodings.
   - If a match is found, a login frame appears; otherwise, a registration frame appears.
