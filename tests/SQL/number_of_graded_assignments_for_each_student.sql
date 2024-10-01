-- Write query to get number of graded assignments for each student:
SELECT 
    student_id, 
    COUNT(id) AS graded_assignments_count
FROM 
    assignments
WHERE 
    state = 'GRADED'  -- Filter for assignments that are graded
GROUP BY 
    student_id;
