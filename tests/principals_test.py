from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.principals import Principal


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

def test_list_teachers(client, h_principal):
    """
    Test case to check if the principal can list all the teachers.
    """
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    assert isinstance(data, list)  # Ensure the data is a list

    for teacher in data:
        assert 'id' in teacher
        assert 'user_id' in teacher
        assert 'created_at' in teacher
        assert 'updated_at' in teacher

def test_get_principal_by_user_id():
    """
    Test that the principal can be correctly retrieved by their user_id.
    """
    # Fetch the principal with user_id = 5
    principal = Principal.query.filter_by(user_id=5).first()

    # Ensure that the principal is not None and is valid
    assert principal is not None
    assert principal.user_id == 5
    assert principal.id is not None

def test_get_principal_by_invalid_user_id():
    """
    Test that attempting to retrieve a principal with a non-existent user_id returns None.
    """
    # Fetch a principal with a user_id that doesn't exist
    principal = Principal.query.filter_by(user_id=999).first()

    # Ensure that no principal is returned
    assert principal is None

