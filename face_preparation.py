import psycopg2

import face_recognition


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


def add_person(input_db_connection, input_cursor, input_first_name, input_last_name, input_face_image):
    sql = "INSERT INTO people(first_name, last_name, face_image) VALUES (%s, %s, %s);"
    input_values = (input_first_name, input_last_name, input_face_image)

    input_cursor.execute(sql, input_values)
    input_db_connection.commit()


def encode_image(input_image_path):
    image = face_recognition.load_image_file(input_image_path)
    face_encoding = face_recognition.face_encodings(image)[0].tolist()

    return face_encoding


def run():
    db_connection, db_cursor = get_db_connection_and_cursor()

    # Stub
    first_name = "Serhii"
    last_name = "Yatsuk"
    image_path = "images/yatsuk.jpg"

    known_face_encoding = encode_image(image_path)

    add_person(db_connection, db_cursor, first_name, last_name, known_face_encoding)

    db_cursor.close()
    db_connection.close()


if __name__ == "__main__":
    run()
