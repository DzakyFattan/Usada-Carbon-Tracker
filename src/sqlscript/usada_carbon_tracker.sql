-- import to SQLite by running: sqlite3.exe db.sqlite3 -init sqlite.sql

PRAGMA journal_mode = MEMORY;
PRAGMA synchronous = OFF;
PRAGMA foreign_keys = OFF;
PRAGMA ignore_check_constraints = OFF;
PRAGMA auto_vacuum = NONE;
PRAGMA secure_delete = OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
`username` TEXT NOT NULL,
`email` TEXT DEFAULT NULL,
`password` TEXT NOT NULL,
`credit_card` TEXT DEFAULT NULL,
`no_telp` TEXT DEFAULT NULL,
`membership` tinyINTEGER DEFAULT 0,
PRIMARY KEY (`username`)
);


DROP TABLE IF EXISTS `activity_history`;

CREATE TABLE `activity_history` (
`activityid` mediumINTEGER NOT NULL ,
`username` TEXT NOT NULL,
`nama_aktivitas` TEXT NOT NULL,
`kategori` TEXT  NOT NULL,
`jumlah_bensin` INTEGER DEFAULT NULL,
`total_watt` INTEGER DEFAULT NULL,
`timestamp_key` datetime NOT NULL,
PRIMARY KEY (`activityid`),
FOREIGN KEY (`username`) REFERENCES `account` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS `daftar_berita`;

CREATE TABLE `daftar_berita` (
`beritaid` mediumINTEGER NOT NULL ,
`judul` TEXT NOT NULL,
`subtitle` TEXT NOT NULL,
`konten` TEXT NOT NULL,
`timestamp_key` datetime NOT NULL,
PRIMARY KEY (`beritaid`)
);


DROP TABLE IF EXISTS `logged_user`;

CREATE TABLE `logged_user` (
`username` TEXT NOT NULL,
FOREIGN KEY (`username`) REFERENCES `account` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS `pending_membership`;

CREATE TABLE `pending_membership` (
`requestid` mediumINTEGER NOT NULL ,
`username` TEXT NOT NULL,
`timestamp_key` datetime NOT NULL,
PRIMARY KEY (`requestid`),
FOREIGN KEY (`username`) REFERENCES `account` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS `tips_and_trick`;

CREATE TABLE `tips_and_trick` (
`tntid` mediumINTEGER NOT NULL ,
`judul` TEXT NOT NULL,
`subtitle` TEXT NOT NULL,
`konten` TEXT NOT NULL,
`timestamp_key` datetime NOT NULL,
PRIMARY KEY (`tntid`)
);


CREATE INDEX `activity_history_username` ON `activity_history` (`username`);
CREATE UNIQUE INDEX `logged_user_username` ON `logged_user` (`username`);
CREATE UNIQUE INDEX `pending_membership_username` ON `pending_membership` (`username`);

COMMIT;
PRAGMA ignore_check_constraints = ON;
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
