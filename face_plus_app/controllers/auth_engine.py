# -*- coding: utf-8 -*-

import logging
import jwt
from odoo import http
from odoo.exceptions import UserError, AccessDenied, AccessError
from odoo.http import request

SECRET = "U2KU!qm6<]:HfKD@"

_logger = logging.getLogger(__name__)


def auth(username, password):
    user = request.session.authenticate(request.db, username.lower(), password)
    if not user:
        raise AccessDenied("Invalid email or password.")
    return request.env.user


def get_token(payload):
    db_secret = http.request.env['ir.config_parameter'].sudo().get_param('database.secret', False)
    
    token = jwt.encode(payload, db_secret, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def validate():
    try:
        db_secret = http.request.env['ir.config_parameter'].sudo().get_param('database.secret', False)
        token = request.httprequest.headers["Authorization"].split(" ")[1].strip()
        
        return jwt.decode(token, db_secret, algorithms=['HS256'], options={'require': ['iss', 'iat', 'exp']}, issuer='face_plus')
    except (KeyError, IndexError, jwt.InvalidTokenError) as ex:
        raise AccessDenied('Invalid or Missing Token') from ex
