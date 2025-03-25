DROP TABLE IF EXISTS people CASCADE;

CREATE TABLE people
(
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name  VARCHAR NOT NULL,
    face_image FLOAT[]
);

SELECT *
FROM people;