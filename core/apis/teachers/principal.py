from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.apis.teachers.schema import TeacherSchema

# Define the blueprint for the principal-related APIs for teachers
teacher_principal_resources = Blueprint('teacher_principal_resources', __name__)

@teacher_principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal  # Authenticate principal
def list_teachers(p):
    """
    Lists all teachers for a principal
    """
    # Query the Teachers model to fetch all teachers
    teachers = Teacher.query.all()

    # Use the TeacherSchema to serialize the data
    teachers_dump = TeacherSchema().dump(teachers, many=True)

    # Return the serialized data
    return APIResponse.respond(data=teachers_dump)
