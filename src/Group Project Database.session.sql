DROP TABLE IF EXISTS artist_song;
DROP TABLE IF EXISTS artist_album;
DROP TABLE IF EXISTS playlist_song;
DROP TABLE IF EXISTS following;
DROP TABLE IF EXISTS playlist;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS song;
DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS artist;

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    ID INT AUTO_INCREMENT,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    account_type VARCHAR(255) NOT NULL CHECK (account_type = "free" OR account_type = "premium" OR account_type = "artist"),
    PRIMARY KEY(ID)
);

DROP TABLE IF EXISTS artist;
CREATE TABLE artist (
    ID INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    description VARCHAR(255),
    debut_date DATE DEFAULT (CURRENT_DATE),
    PRIMARY KEY(ID)
);

DROP TABLE IF EXISTS album;
CREATE TABLE album (
    ID INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    record_label VARCHAR(255) NOT NULL,
    genre VARCHAR(255),
    release_date date DEFAULT (CURRENT_DATE),
    classification VARCHAR(255) NOT NULL CHECK (classification = "album" OR classification = "single" OR classification = "EP" OR classification = "Compilation"),
    duration TIME NOT NULL,
    artist_ID INT NOT NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(artist_ID)
        REFERENCES artist (ID)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS song;
CREATE TABLE song (
    ID INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    tempo INT CHECK (tempo >= 20 AND tempo <= 200),
    song_key VARCHAR(255) CHECK (song_key = "A" OR song_key = "A#" OR song_key = "Bb" OR song_key = "B" OR song_key = "C" OR song_key = "C#" OR song_key - "Db" OR song_key = "D" OR song_key = "D#" OR song_key = "Eb" OR song_key = "E" OR song_key = "F" OR song_key = "F#" OR song_key = "Gb" OR song_key = "G" OR song_key = "G#" OR song_key = "Ab"),
    plays INT DEFAULT 0 CHECK (plays >= 0),
    duration TIME NOT NULL CHECK (duration > 0.00),
    artist_ID INT NOT NULL,
    album_ID INT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY(artist_ID)
        REFERENCES artist (ID)
        ON DELETE CASCADE,
    FOREIGN KEY(album_ID)
        REFERENCES album (ID)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS playlist;
CREATE TABLE playlist (
    ID INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    duration TIME NOT NULL CHECK (duration > 0.00),
    user_ID INT NOT NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(user_ID)
        REFERENCES user (ID)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS artist_song;
CREATE TABLE artist_song (
    ID INT AUTO_INCREMENT,
    artist_ID INT NOT NULL,
    song_ID INT NOT NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(artist_ID)
        REFERENCES artist (ID)
        ON DELETE CASCADE,
    FOREIGN KEY(song_ID)
        REFERENCES song (ID)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS artist_album;
CREATE TABLE artist_album (
    ID INT AUTO_INCREMENT,
    artist_ID INT NOT NULL,
    album_ID INT NOT NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(artist_ID)
        REFERENCES artist (ID)
        ON DELETE CASCADE,
    FOREIGN KEY(album_ID)
        REFERENCES album (ID)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS playlist_song;
CREATE TABLE playlist_song (
    ID INT AUTO_INCREMENT,
    playlist_ID INT NOT NULL,
    song_ID INT NOT NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(playlist_ID)
        REFERENCES playlist (ID)
        ON DELETE CASCADE,
    FOREIGN KEY(song_ID)
        REFERENCES song (ID)
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS following;
CREATE TABLE following (
    ID INT AUTO_INCREMENT,
    follower_ID INT NOT NULL,
    following_ID INT NOT NULL,
    PRIMARY KEY(ID),
    FOREIGN KEY(follower_ID)
        REFERENCES user (ID)
        ON DELETE CASCADE,
    FOREIGN KEY(following_ID)
        REFERENCES user (ID)
        ON DELETE CASCADE
);