from core.libs.assertions import assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError


def test_assert_auth_pass():
    """
    Test assert_auth when the condition is True (no error should be raised).
    """
    try:
        assert_auth(True)
    except FyleError:
        assert False, "FyleError was raised when it should not have been"


def test_assert_auth_fail():
    """
    Test assert_auth when the condition is False (should raise FyleError with 401).
    """
    try:
        assert_auth(False)
    except FyleError as e:
        assert e.status_code == 401
        assert e.message == 'UNAUTHORIZED'
    else:
        assert False, "FyleError was not raised"


def test_assert_true_pass():
    """
    Test assert_true when the condition is True (no error should be raised).
    """
    try:
        assert_true(True)
    except FyleError:
        assert False, "FyleError was raised when it should not have been"


def test_assert_true_fail():
    """
    Test assert_true when the condition is False (should raise FyleError with 403).
    """
    try:
        assert_true(False)
    except FyleError as e:
        assert e.status_code == 403
        assert e.message == 'FORBIDDEN'
    else:
        assert False, "FyleError was not raised"


def test_assert_valid_pass():
    """
    Test assert_valid when the condition is True (no error should be raised).
    """
    try:
        assert_valid(True)
    except FyleError:
        assert False, "FyleError was raised when it should not have been"


def test_assert_valid_fail():
    """
    Test assert_valid when the condition is False (should raise FyleError with 400).
    """
    try:
        assert_valid(False)
    except FyleError as e:
        assert e.status_code == 400
        assert e.message == 'BAD_REQUEST'
    else:
        assert False, "FyleError was not raised"


def test_assert_found_pass():
    """
    Test assert_found when the object is not None (no error should be raised).
    """
    try:
        assert_found(object())
    except FyleError:
        assert False, "FyleError was raised when it should not have been"


def test_assert_found_fail():
    """
    Test assert_found when the object is None (should raise FyleError with 404).
    """
    try:
        assert_found(None)
    except FyleError as e:
        assert e.status_code == 404
        assert e.message == 'NOT_FOUND'
    else:
        assert False, "FyleError was not raised"

def test_fyle_error_initialization():
    """
    Test that the FyleError is correctly initialized with status code and message.
    """
    error = FyleError(403, 'FORBIDDEN')

    assert error.status_code == 403
    assert error.message == 'FORBIDDEN'


def test_fyle_error_to_dict():
    """
    Test that the FyleError correctly converts to a dictionary with the message.
    """
    error = FyleError(400, 'BAD_REQUEST')

    error_dict = error.to_dict()
    assert error_dict['message'] == 'BAD_REQUEST'