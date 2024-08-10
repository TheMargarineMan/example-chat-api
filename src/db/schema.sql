/*
Schema Information:
users - Contains users alongside authentication data
inactive_users - Contains users with deactivated accounts
communities - Contains community identification data
comm_users - Contains users that exist within communities
bans - Contains users that are banned from communities
chats - Contains all active chatrooms
chat_users - Contains all users in chatrooms
direct_chats - Contains private chatrooms between two users
messages - Contains all message data
unread_messages - Contains messages yet to be read by users
mentions - Contains users mentioned in a message
*/

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    session_key TEXT,
    name_change TIMESTAMP
);

CREATE TABLE inactive_users(
    user_id SERIAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE communities(
    comm_id SERIAL PRIMARY KEY,
    comm_name TEXT NOT NULL 
);

CREATE TABLE comm_users(
    user_id SERIAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
    comm_id SERIAL,
        FOREIGN KEY (comm_id) REFERENCES communities(comm_id)
);

CREATE TABLE bans(
    user_id SERIAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
    comm_id SERIAL,
        FOREIGN KEY (comm_id) REFERENCES communities(comm_id),
    ban_until TIMESTAMP 
);

CREATE TABLE chats(
    chat_id SERIAL PRIMARY KEY,
    chat_name TEXT NOT NULL,
    comm_id INT,
        FOREIGN KEY (comm_id) REFERENCES communities(comm_id)
);

CREATE TABLE chat_users(
    user_id SERIAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),     
    chat_id SERIAL, 
        FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
);

CREATE TABLE direct_chats(
    user_one SERIAL,
        FOREIGN KEY (user_one) REFERENCES users(user_id),
    user_two SERIAL,
        FOREIGN KEY (user_two) REFERENCES users(user_id),
    chat_id SERIAL,
        FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
);

CREATE TABLE messages( 
    msg_id SERIAL PRIMARY KEY,
    message VARCHAR(500),
    edited BOOLEAN NOT NULL DEFAULT FALSE,
    timestamp TIMESTAMP,
    user_id SERIAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
    chat_id SERIAL,
        FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
);

CREATE TABLE unread_messages( 
    msg_id SERIAL,
        FOREIGN KEY (msg_id) REFERENCES messages(msg_id),
    user_id SERIAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE mentions(
    msg_id SERIAL,
        FOREIGN KEY (msg_id) REFERENCES messages(msg_id),
    user_id SERIAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);