CREATE TABLE users
(
    "Id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "PublicId" character VARCHAR(128) NOT NULL,
    "Email" character VARCHAR(128) NOT NULL,
    "FullName" character VARCHAR(128) NOT NULL,
    "Role" character varying(128) NOT NULL
);
