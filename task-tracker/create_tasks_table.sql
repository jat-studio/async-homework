CREATE TABLE users
(
    "Id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "Uuid" character VARCHAR(128) NOT NULL,
    "Title" character VARCHAR(128) NOT NULL,
    "Description" character VARCHAR(128) NOT NULL,
    "Status" character VARCHAR(128) NOT NULL
);
