from core.models.users import User

def test_get_user_by_id():
    """
    Test that a user can be correctly retrieved by their user_id.
    """
    # Fetch the user with user_id = 5 (the principal in your case)
    user = User.query.filter_by(id=5).first()

    # Ensure that the user is not None and has valid attributes
    assert user is not None
    assert user.id == 5
    assert user.email == 'principal@fylebe.com'
    assert user.username == 'principal'

def test_get_user_by_invalid_id():
    """
    Test that attempting to retrieve a user with a non-existent user_id returns None.
    """
    # Fetch a user with a user_id that doesn't exist (e.g., user_id = 999)
    user = User.query.filter_by(id=999).first()

    # Ensure that no user is returned
    assert user is None


def test_get_user_by_email():
    """
    Test that a user can be correctly retrieved by their email.
    """
    # Fetch the user with email 'principal@fylebe.com'
    user = User.query.filter_by(email='student1@fylebe.com').first()

    # Ensure that the user is not None and has valid attributes
    assert user is not None
    assert user.email == 'student1@fylebe.com'
    assert user.username == 'student1'

def test_get_user_by_invalid_email():
    """
    Test that attempting to retrieve a user with a non-existent email returns None.
    """
    # Fetch a user with an email that doesn't exist
    user = User.query.filter_by(email='nonexistent@fylebe.com').first()

    # Ensure that no user is returned
    assert user is None

def test_get_all_users():
    """
    Test that all users can be retrieved from the database.
    """
    # Fetch all users from the database
    users = User.query.all()

    # Ensure that the list is not empty and contains valid users
    assert len(users) > 0

    # Check that each user has the expected attributes
    for user in users:
        assert user.id is not None
        assert user.username is not None
        assert user.email is not None
