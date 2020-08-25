/***********************************************************
*
* MPD Designer 3.1.4150.32424
*
* Code for PostgreSQL 7.4
* Generated on 03/01/2020 13:31:32
*
* Louis SAUNDERS
* http://louis.saunders.free.fr/
*
************************************************************/
/*
ALTER TABLE days_off
    DROP FOREIGN KEY FK_DAYSOFF_USERS,
    DROP FOREIGN KEY FK_DAYSOFF_ABSENCE;


*/
DROP TABLE IF EXISTS configuration;
DROP TABLE IF EXISTS queues;
DROP TABLE IF EXISTS users;


PRAGMA encoding="UTF-8";


/***********************************************************
* configuration
************************************************************/

CREATE TABLE configuration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value TEXT NOT NULL
);

/***********************************************************
* absence
************************************************************/

CREATE TABLE queues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    UNIQUE (userid, day)
    FOREIGN KEY (userid)
        REFERENCES users (id)
            ON DELETE CASCADE,
);

/***********************************************************
* users
************************************************************/

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NUL NULL UNIQUE,
    firstname TEXT NOT NULL
);

/***********************************************************
* days_off
************************************************************/

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    FOREIGN KEY (userid)
        REFERENCES users (id)
            ON DELETE CASCADE,
    postid INTEGER NOT NULL,
    FOREIGN KEY (postid)
        REFERENCES users (id)
            ON DELETE CASCADE,
    UNIQUE (userid, postid)
);


/***********************************************************
* INDEXED KEYS
************************************************************/


/***********************************************************
* FOREIGN KEYS
************************************************************/

/***********************************************************
* DATA
************************************************************/
INSERT INTO users (id, email, firstname) VALUES (1, 'germain@lefebvre.fr', 'Germain');
INSERT INTO absence_type (id, kind) VALUES (1, 'Absence enfant');
INSERT INTO absence_type (id, kind) VALUES (2, 'Maladie enfant');
INSERT INTO absence_type (id, kind) VALUES (3, 'Congé Nounou');
INSERT INTO absence_type (id, kind) VALUES (4, 'Maladie Nounou');

