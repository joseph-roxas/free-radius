CREATE TEMPORARY TABLE IF NOT EXISTS TABLE1 AS 
(SELECT a.id
	,a.username
	,a.value
	,TIME_TO_SEC(TIMEDIFF(NOW(),b.authdate)) as lapse_seconds
	FROM (SELECT * FROM radcheck
		       WHERE attribute = 'Max-All-Session') as a
	JOIN (SELECT * FROM radpostauth 
		       WHERE reply = 'Access-Accept') as b
	ON a.username = b.username);

CREATE TEMPORARY TABLE IF NOT EXISTS TABLE2 AS 
(SELECT DISTINCT username FROM (SELECT *, 
	CASE
	WHEN lapse_seconds - value > 0 THEN 1 ELSE 0 
	END AS expired FROM TABLE1) as tag_expired
	WHERE expired = 1);

CREATE TEMPORARY TABLE IF NOT EXISTS TABLE3 AS
(SELECT username FROM  radpostauth WHERE username NOT IN (SELECT username FROM radcheck));


DELETE FROM radcheck WHERE username in (SELECT * FROM TABLE2);
DELETE FROM radpostauth WHERE username in (SELECT * FROM TABLE2);
DELETE FROM radpostauth WHERE username in (SELECT * FROM TABLE3);
DELETE FROM radpostauth WHERE reply = 'Access-Reject';
