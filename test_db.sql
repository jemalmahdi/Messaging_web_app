.mode column
.headers on

.print sqlite3 WooMessages.sqlite < test_db.sql

.print user all info

SELECT user.id AS "ID", user.name AS "Name", user.email AS "Email",
       user.username AS "Username",
       user.password AS "Encrypted Password"
FROM user
ORDER BY user.id;



.print user AviVajpeyi info

SELECT * FROM user WHERE user.username = "AviVajpeyi";

.print chat info from different users in different chats ordered by time


.print chat room ordered by time

SELECT user.name AS "Name", chat.title AS "Chat Room",
 message.message AS "Text", message.time AS "Time"
FROM user, chat, chat_rel, message
WHERE chat_rel.user_id = user.id
AND chat_rel.chat_id = chat.id
AND message.user_id = user.id
AND message.chat_id = chat.id
ORDER BY chat.title, message.time;

.print chatrooms
SELECT chat.title AS "Chat room"
FROM chat;