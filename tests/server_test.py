def test_server_ready(client):
    """
    Test that the server is ready and returns the correct status.
    """
    response = client.get('/')
    assert response.status_code == 200
    data = response.json
    assert data['status'] == 'ready'
    assert 'time' in data


def test_handle_fyle_error(client):
    """
    Test that a FyleError is handled correctly by the global error handler.
    """
    @client.application.route('/raise-fyle-error')
    def raise_fyle_error():
        from core.libs.exceptions import FyleError
        raise FyleError(400, 'This is a FyleError')

    response = client.get('/raise-fyle-error')
    assert response.status_code == 400
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'This is a FyleError'


def test_handle_validation_error(client):
    """
    Test that a ValidationError is handled correctly by the global error handler.
    """
    @client.application.route('/raise-validation-error')
    def raise_validation_error():
        from marshmallow.exceptions import ValidationError
        raise ValidationError('This is a ValidationError')

    response = client.get('/raise-validation-error')
    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'
    assert response.json['message'] == ['This is a ValidationError']


def test_handle_integrity_error(client):
    """
    Test that an IntegrityError is handled correctly by the global error handler.
    """
    @client.application.route('/raise-integrity-error')
    def raise_integrity_error():
        from sqlalchemy.exc import IntegrityError
        raise IntegrityError('Integrity error', 'params', 'orig')

    response = client.get('/raise-integrity-error')
    assert response.status_code == 400
    assert response.json['error'] == 'IntegrityError'
    assert response.json['message'] == 'orig'


def test_handle_http_exception(client):
    """
    Test that an HTTPException is handled correctly by the global error handler.
    """
    @client.application.route('/raise-http-error')
    def raise_http_exception():
        from werkzeug.exceptions import NotFound
        raise NotFound('This is an HTTPException')

    response = client.get('/raise-http-error')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'
    assert response.json['message'] == '404 Not Found: This is an HTTPException'

