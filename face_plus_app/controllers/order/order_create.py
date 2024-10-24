# -*- coding: utf-8 -*-

from odoo import http
from .. import dictionary
from .. import external_api

import logging
_logger = logging.getLogger(__name__)


@http.route('/api/order_create', auth='public', type="json", methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
@external_api.authenticated()
def order_create(self, **kw):
    json_body = kw["json_body"]
    user = dictionary.get_login_user()

    filters = [('create_uid', '=', user.get('id'))]

    order_ids = http.request.env['face.plus.order'].sudo().search(filters, order='id desc')

    order_dict = self.get_order_to_dict(order_ids)
    return {'results': order_dict}
