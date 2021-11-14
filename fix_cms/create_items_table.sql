CREATE TABLE items
(
    "Id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "OwnerPublicId" character VARCHAR(128),
    "PublicId" character VARCHAR(128) NOT NULL,
    "Title" character VARCHAR(128) NOT NULL,
    "BreakCount" integer NOT NULL DEFAULT 0,
    "Status" character VARCHAR(128) NOT NULL,
    "Meta" character VARCHAR(128) NOT NULL,
    "CreatedAt" datetime NOT NULL,
    "UpdatedAt" datetime NOT NULL
);
