def bad_request(message):
    response = {'error': 'Bad request.',
                'message': message}
    status_code = 400
    return response, status_code


def not_found(message):
    response = {'error': 'Not Found', 'message': message}
    status_code = 404
    return response, status_code
