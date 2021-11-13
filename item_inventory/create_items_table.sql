CREATE TABLE items
(
    "Id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "UserId" integer,
    "PublicId" character VARCHAR(128) NOT NULL,
    "Title" character VARCHAR(128) NOT NULL,
    "Description" character VARCHAR(128) NOT NULL,
    "Status" character VARCHAR(128) NOT NULL
);
