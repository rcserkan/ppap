# -*- coding: utf-8 -*-

import functools
import json
import logging
from odoo import http, SUPERUSER_ID
from odoo.exceptions import AccessDenied, AccessError, UserError, MissingError
from odoo.http import Response
from odoo.tools import date_utils
from . import auth_engine
from datetime import datetime
from jwt import ExpiredSignatureError

import logging
_logger = logging.getLogger(__name__)

_exception_http_code_map = {
    UserError: 400,
    AccessDenied: 401,
    ExpiredSignatureError: 401,
    AccessError: 403,
    MissingError: 404,
}

_exception_message_map = {
    # except_orm: lambda ex: ex.name,
    OSError: lambda ex: ex.strerror,
    AccessDenied: lambda ex: ex.args[0],
}


def _get_exception_http_code(ex: Exception) -> int:
    for ex_type, code in _exception_http_code_map.items():
        if isinstance(ex, ex_type):
            return code
    return 500


def _get_exception_message(ex: Exception) -> str:
    for ex_type, func in _exception_message_map.items():
        if isinstance(ex, ex_type):
            return func(ex)
    return str(ex)


def authenticated(func=None, *, roles=None):
    if func:
        raise TypeError('use @face_plus_app.authenticated(), not @face_plus_app.authenticated')

    _logger.info("*******************")
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token_data = auth_engine.validate()
            user_dict = token_data.get('user')
            iat = token_data.get('iat')
            if not isinstance(user_dict, dict):
                raise AccessError('Token is invalid')
            user_id = user_dict.get('id')
            if not isinstance(user_id, int):
                raise AccessError('Token is invalid')

            user = http.request.env['res.users'].sudo().browse(user_id)
            if not user.exists():
                raise AccessError('Token is invalid')

            iat_date = datetime.fromtimestamp(iat)
            http.request.env.context = dict(
                http.request.env.context,
                display_default_code=False,
                rc_user=token_data['user'],
                rc_username=token_data['username'],
                rc_partner_id=user.partner_id.id,
            )

            if user and user.share:
                http.request.env.uid = user.id

            result = func(*args, **kwargs)
            if not isinstance(result, dict):
                raise ValueError('%s.%s must return a dictionary' % (func.__module__, func.__name__))
            result['token'] = auth_engine.get_token(user.get_token_data())
            return result
        return wrapper
    return decorator


class RestJsonResponse(Response):
    def __init__(self, *args, **kwargs):
        response = kwargs.get('response', None)
        if not response:
            raise TypeError('Response body is required')
        headers: list = kwargs.get('headers')
        if not headers:
            headers = []
            kwargs['headers'] = headers
        headers.append(('Content-Type', 'application/json'))
        headers.append(('Content-Length', len(response)))
        super().__init__(*args, **kwargs)

def rest_response(func=None):
    if func:
        raise TypeError('use @face_plus_app.rest_response(), not @face_plus_app.rest_response')

    def decorator(func):
        logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if http.request.dispatcher.routing_type == 'json':
                    kwargs['json_body'] = http.request.dispatcher.jsonrequest
                result = func(*args, **kwargs)
                headers = []
                if 'token' in result:
                    headers.append(('X-Token', result['token']))
                    del result['token']
                body = json.dumps(result, default=date_utils.json_default)
                return RestJsonResponse(headers=headers, response=body, status=200)
            except Exception as ex:
                logger.error('Platform Exception', exc_info=ex)
                http.request.env.cr.rollback()
                status = _get_exception_http_code(ex)
                error = _get_exception_message(ex)
                body = json.dumps({'error': error}, default=date_utils.json_default)
                return RestJsonResponse(response=body, status=status)
        return wrapper
    return decorator