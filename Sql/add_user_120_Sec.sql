# Add a new user to radcheck

SET @random_chars :=
	(SELECT CONCAT(CHAR(FLOOR(65 + RAND()*26)),
	       CHAR(FLOOR(65 + RAND()*26)),
	       CHAR(FLOOR(65 + RAND()*26)),
	       CHAR(FLOOR(65 + RAND()*26)),
	       CHAR(FLOOR(65 + RAND()*26))));

SET @random_pass :=
	(SELECT CONCAT(CHAR(FLOOR(48 + RAND()*10)),
	       CHAR(FLOOR(48 + RAND()*10)),
	       CHAR(FLOOR(48 + RAND()*10)),
	       CHAR(FLOOR(48 + RAND()*10))));

INSERT INTO radcheck
	(
	username
	,attribute
	,op
	,value
	)
VALUES
	(
	@random_chars,
	"Cleartext-Password",
	":=",
	@random_pass 
	),
	(
	@random_chars,
	"Max-All-Session",
	":=",
	"120"
	),
	(
	@random_chars,
	"Simultaneous-Use",
	":=",
	"1"
	);

SELECT 	@random_chars
	,@random_pass;
