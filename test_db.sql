.mode column
.headers on

.print sqlite3 Social.sqlite < test_db.sql

.print user all info

SELECT user.id AS "ID", user.name AS "Name", user.email AS "Email",
       user.username AS "Username",
       user.password AS "Encrypted Password"
FROM user
ORDER BY user.id;


.print user Avi1 info

SELECT * FROM user WHERE user.username = "Avi1";


SELECT chat.name FROM user, chat
WHERE user.id = chat.user_id
AND username = "Avi1"


--SELECT user.id AS "ID", user.name AS "Name", user.email AS "Email",
--       user.username AS "Username",
--       user.password AS "password"
--FROM track, album, artist
--WHERE track.album_id = album.id
--AND   album.artist_id = artist.id
--ORDER BY track.name;