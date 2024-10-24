# -*- coding: utf-8 -*-
from odoo import http
from .. import auth_engine
from .. import external_api
import logging
_logger = logging.getLogger(__name__)

@http.route('/api/login', auth='public', type='json', methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
def signin(self, json_body):
    username = json_body.get('username', None)
    password = json_body.get('password', None)
    user = auth_engine.auth(username, password)

    token = auth_engine.get_token(user.get_token_data())
    user_dict = self.get_user_to_dict(user)
    return {"token": token, 'user_token': token, 'user_info': user_dict}
