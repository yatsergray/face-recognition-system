import time
import tkinter as tk

import cv2
import numpy as np
import psycopg2

import face_recognition


def show_login_frame():
    window = tk.Tk()
    window.title("Login Frame")

    login_frame = tk.Frame(window)
    login_frame.pack(pady=20)

    username_label = tk.Label(login_frame, text="YOU NEED TO LOGIN")
    username_label.grid(row=0, column=0, padx=10, pady=5)

    window.mainloop()


def show_register_frame():
    window = tk.Tk()
    window.title("Register Frame")

    login_frame = tk.Frame(window)
    login_frame.pack(pady=20)

    username_label = tk.Label(login_frame, text="YOU NEED TO REGISTER")
    username_label.grid(row=0, column=0, padx=10, pady=5)

    window.mainloop()


def get_db_connection_and_cursor():
    configured_db_connection = psycopg2.connect(
        database="face_recognition_db",
        user="postgres",
        password="yatsergray",
        host="localhost",
        port='5432'
    )

    created_db_cursor = configured_db_connection.cursor()

    return configured_db_connection, created_db_cursor


def get_all_people(input_db_cursor):
    input_db_cursor.execute("SELECT id, first_name, last_name, face_image FROM people;")

    found_all_people = input_db_cursor.fetchall()

    return found_all_people


def get_frame_centre(input_frame):
    input_frame_height, input_frame_width, _ = input_frame.shape

    input_frame_height_centre = int(0.5 * input_frame_height)
    input_frame_width_centre = int(0.5 * input_frame_width)

    return input_frame_height_centre, input_frame_width_centre


def get_constraint_frame_borders(input_frame_height_centre, input_frame_width_centre):
    input_frame_height_part = int(0.75 * input_frame_height_centre)
    input_frame_width_part = int(0.4 * input_frame_width_centre)

    input_frame_frame_top = int(input_frame_height_centre + input_frame_height_part)
    input_frame_frame_right = int(input_frame_width_centre + input_frame_width_part)
    input_frame_frame_bottom = int(input_frame_height_centre - input_frame_height_part)
    input_frame_frame_left = int(input_frame_width_centre - input_frame_width_part)

    return input_frame_frame_top, input_frame_frame_right, input_frame_frame_bottom, input_frame_frame_left


def recognize_face(input_frame, input_frame_face_locations, input_known_face_encodings, input_all_people):
    face_encodings = face_recognition.face_encodings(input_frame, input_frame_face_locations)

    face_encoding = face_encodings[0]

    matches = face_recognition.compare_faces(input_known_face_encodings, face_encoding)

    face_distances = face_recognition.face_distance(input_known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)

    person = input_all_people[best_match_index]

    return input_frame_face_locations[0], f"{person[1]} {person[2]}" if matches[best_match_index] else "Unknown"


def handle_frame(is_recognized):
    if is_recognized:
        show_login_frame()
    else:
        show_register_frame()


def run():
    db_connection, db_cursor = get_db_connection_and_cursor()
    all_people = get_all_people(db_cursor)
    known_face_encodings = [person[3] for person in all_people]

    video_capture = cv2.VideoCapture(0)

    start_time = time.time()
    counter = 1
    max_counter_value = 4
    name = "Unknown"

    while True:
        ret, frame = video_capture.read()

        height_centre, width_centre = get_frame_centre(frame)

        frame_top, frame_right, frame_bottom, frame_left = get_constraint_frame_borders(height_centre, width_centre)

        color = (0, 0, 255)
        counter_str = "Place your face in the frame"
        counter_str_x_coordinate = width_centre - 250

        square_frame = frame[frame_bottom:frame_top, frame_left:frame_right]

        face_locations = face_recognition.face_locations(square_frame)

        if len(face_locations) == 1:
            if counter == max_counter_value:
                break

            color = (0, 255, 0)
            counter_str = str(counter)
            counter_str_x_coordinate = width_centre

            if time.time() - start_time >= 1:
                face_location, name = recognize_face(square_frame, face_locations, known_face_encodings, all_people)

                top, right, bottom, left = face_location

                cv2.rectangle(square_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(square_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                cv2.putText(square_frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255),
                            1)

                start_time = time.time()
                counter += 1
        else:
            start_time = time.time()
            counter = 1

        cv2.rectangle(frame, (frame_left, frame_top), (frame_right, frame_bottom), color, 5)

        cv2.putText(frame, counter_str, (counter_str_x_coordinate, frame_top + 35), cv2.FONT_HERSHEY_DUPLEX, 1.0,
                    (255, 255, 255), 1)

        # gif_writer.write(frame)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    db_cursor.close()
    db_connection.close()

    video_capture.release()

    cv2.destroyAllWindows()

    handle_frame(name != "Unknown")


if __name__ == "__main__":
    run()
