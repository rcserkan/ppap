# -*- coding: utf-8 -*-
from odoo import http
from .. import auth_engine
from .. import external_api
import logging
_logger = logging.getLogger(__name__)

@http.route('/api/user_create', auth='public', type='json', methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
@external_api.authenticated()
def user_create(self, json_body):
    name = json_body.get('name', None)
    email = json_body.get('email', None)
    password = json_body.get('password', None)
    
    user_id = http.request.env['res.users'].create({
        'name': name,
        'login': email,
        # 'password': password,
    })

    user_dict = self.get_user_to_dict(user_id)
    return {'results': user_dict}
