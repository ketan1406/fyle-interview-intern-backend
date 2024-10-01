from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema

# Define the blueprint for the principal-related APIs
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """
    Returns list of all submitted and graded assignments for the principal.
    """
    # Query all assignments that are in 'SUBMITTED' or 'GRADED' state
    principal_assignments = Assignment.query.filter(
        (Assignment.state == AssignmentStateEnum.SUBMITTED) |
        (Assignment.state == AssignmentStateEnum.GRADED)
    ).all()
    
    # Serialize the assignments using the AssignmentSchema
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    
    # Return the API response with the list of assignments
    return APIResponse.respond(data=principal_assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """
    Grades or re-grades an assignment as a principal.
    """
    # Load the incoming payload using AssignmentGradeSchema
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment by ID
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # Ensure that the assignment is in a valid state to be graded or re-graded
    if assignment.state == AssignmentStateEnum.DRAFT:
        # Directly return a response indicating that a DRAFT assignment cannot be graded
        return APIResponse.respond(data={'error': 'Assignment in DRAFT state cannot be graded.'}, status_code=400)

    # Grade or regrade the assignment
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )


    # Commit the changes to the database
    db.session.commit()

    # Serialize the graded/re-graded assignment
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

    # Return the response with the graded assignment details
    return APIResponse.respond(data=graded_assignment_dump)