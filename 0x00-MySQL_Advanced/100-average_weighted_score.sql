-- SQL script that creates a stored procedure 
-- to computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    user_id INT
)
BEGIN
    DECLARE whtd_avg FLOAT;
    SET whtd_avg = (SELECT SUM(score * weight) / SUM(weight)
                        FROM users AS Stdt
                        JOIN corrections as Cg ON Stdt.id=Cg.user_id
                        JOIN projects AS Prj ON Cg.project_id=Prj.id
                        WHERE Stdt.id=user_id);
    UPDATE users SET average_score = whtd_avg WHERE id=user_id;
END
//
DELIMITER ;
