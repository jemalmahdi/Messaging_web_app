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


SELECT chat.name FROM user, chat
WHERE user.id = chat.user_id
AND username = "AviVajpeyi"


--SELECT user.id AS "ID", user.name AS "Name", user.email AS "Email",
--       user.username AS "Username",
--       user.password AS "password"
--FROM track, album, artist
--WHERE track.album_id = album.id
--AND   album.artist_id = artist.id
--ORDER BY track.name;