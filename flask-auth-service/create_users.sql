CREATE TABLE users
(
    "Id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "ClientSecret" VARCHAR(256) NOT NULL,
    "Uuid" character VARCHAR(128) NOT NULL,
    "Email" character VARCHAR(128) NOT NULL,
    "FullName" character VARCHAR(128) NOT NULL,
    "Position" character VARCHAR(128) NOT NULL,
    "IsActive" boolean NOT NULL,
    "Role" character varying(128) NOT NULL
);
