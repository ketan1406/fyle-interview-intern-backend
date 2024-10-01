-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grading_count AS (
    -- Find the count of assignments graded by each teacher
    SELECT 
        teacher_id, 
        COUNT(id) AS total_graded
    FROM 
        assignments
    WHERE 
        grade IS NOT NULL  -- Ensures that only graded assignments are counted
    GROUP BY 
        teacher_id
), max_grading_teacher AS (
    -- Find the teacher who graded the most assignments
    SELECT 
        teacher_id
    FROM 
        teacher_grading_count
    ORDER BY 
        total_graded DESC
    LIMIT 1
)
-- Now count the number of grade 'A' assignments by that teacher
SELECT 
    COUNT(id) AS grade_A_count
FROM 
    assignments
WHERE 
    teacher_id = (SELECT teacher_id FROM max_grading_teacher)
    AND grade = 'A';
