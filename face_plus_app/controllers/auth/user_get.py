# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import MissingError
from .. import external_api

import logging
_logger = logging.getLogger(__name__)

@http.route('/api/users', auth='public', methods=["GET", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
@external_api.authenticated()
def user_get(self):
    user = self.get_login_user()
    user_id = user.get('id')
    users = http.request.env['res.users'].sudo().search([('id', '=', user_id)], limit=1)

    user_dict = self.get_user_to_dict(users, http.request.env.company)
    return {'results': user_dict}
