# -*- coding: utf-8 -*-
from odoo import http
from .. import auth_engine
from .. import external_api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

@http.route('/api/user_create', auth='public', type='json', methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
def user_create(self, json_body):

    name = json_body.get('name', None)
    email = json_body.get('email', None)
    phone = json_body.get('phone', None)
    password = json_body.get('password', None)
    
    check_user = http.request.env['res.users'].sudo().search([(('login', '=', email))], limit=1)
    if check_user:
        raise UserError("The user already exists!")
    else:
        user_id = http.request.env['res.users'].sudo().create({
            'name': name,
            'login': email,
            'phone': phone,
            'scan_limit': 1
            # 'password': password,
        })

        user_dict = self.get_user_to_dict(user_id)
        return {'results': user_dict}
