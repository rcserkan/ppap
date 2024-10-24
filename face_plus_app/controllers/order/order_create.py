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

    orders_dict = self.get_order_to_dict(order)
    return {'results': orders_dict}
