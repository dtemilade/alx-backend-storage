-- SQL script that creates a stored procedure 
-- to computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS Stdt,
        (SELECT Stdt.id, SUM(score * weight) / SUM(weight) AS wht_avg
        FROM users AS Stdt
        JOIN corrections as Cg ON Stdt.id=Cg.user_id
        JOIN projects AS Prj ON Cg.project_id=Prj.id
        GROUP BY Stdt.id)
    AS WA
    SET Stdt.average_score = WA.wht_avg
    WHERE Stdt.id=WA.id;
END
//
DELIMITER ;
