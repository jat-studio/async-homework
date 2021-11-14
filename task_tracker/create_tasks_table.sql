CREATE TABLE tasks
(
    "Id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "PublicId" character VARCHAR(128) NOT NULL,
    "Description" character VARCHAR(128) NOT NULL,
    "Status" character VARCHAR(128) NOT NULL,
    "Price" character VARCHAR(128) NOT NULL,
    "AssignToPublicId" character VARCHAR(128)
);
