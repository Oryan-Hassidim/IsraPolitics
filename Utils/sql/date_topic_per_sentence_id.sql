SELECT ks.date, t.topic
FROM knesset_speeches ks 
JOIN topics t ON ks.topic_id = t.id
WHERE ks.id = ?;