CREATE DATABASE TwitterClone;

USE TwitterClone;

CREATE TABLE users (
    username NVARCHAR(50) PRIMARY KEY
);

CREATE TABLE posts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL,
    content NVARCHAR(MAX) NOT NULL,
    timestamp DATETIME DEFAULT GETDATE(),
    parent_post_id INT NULL,
    media_filename NVARCHAR(255) NULL,
    media_type NVARCHAR(10) NULL,
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (parent_post_id) REFERENCES posts(id)
);


CREATE TABLE likes (
    post_id INT,
    username NVARCHAR(50),
    PRIMARY KEY (post_id, username),
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (username) REFERENCES users(username)
);
