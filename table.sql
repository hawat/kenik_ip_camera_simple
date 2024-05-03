CREATE TABLE images2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    image_data BLOB
);

.schema images

drop table images;

 CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            address TEXT,
            image BLOB
        )