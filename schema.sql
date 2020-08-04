CREATE TABLE "files" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "filename" TEXT NOT NULL UNIQUE,
    "st_mode" INTEGER,
    "st_uid" INTEGER,
    "st_gid" INTEGER,
    "st_size" INTEGER,
    "st_ctime" INTEGER,
    "st_atime" INTEGER,
    "st_mtime" INTEGER,
    "md5" VARCHAR(64)
)

