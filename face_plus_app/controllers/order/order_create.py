# -*- coding: utf-8 -*-

from odoo import http
from .. import dictionary
from .. import external_api
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


@http.route('/api/order_create', auth='public', type="json", methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
@external_api.authenticated()
def order_create(self, **kw):
    json_body = kw["json_body"]
    # user = dictionary.get_login_user()

    # user = http.request.env['res.users'].sudo().search([('id', '=', user.get('id'))], limit=1)
    # if user.scan_limit <= 0:
    #     raise UserError("Please upgrade to a higher plan for analysis.")

    image_base64 = json_body.get('image_base64', None)

    order = http.request.env['face.plus.order'].sudo().create({})
    if order:
        http.request.env['ir.attachment'].sudo().create({
            'name': order.name,
            'res_id': order.id,
            'res_model': 'face.plus.order',
            'datas': image_base64,
            'type': 'binary',
            'mimetype': 'application/jpg',
        })
        order.run_face_plus_report()
        order.run_chat_gpt_report()

        
        # user.sudo().update({ 'scan_limit': user.scan_limit - 1})

    orders_dict = self.get_order_to_dict(order)
    return {'results': orders_dict}
