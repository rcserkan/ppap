# -*- coding: utf-8 -*-

from odoo import http
from .. import dictionary
from .. import external_api
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


@http.route('/api/pay', auth='public', type="json", methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
@external_api.authenticated()
def pay(self, **kw):
    json_body = kw["json_body"]
    user = dictionary.get_login_user()

    name = json_body.get('name', None)
    number = json_body.get('number', None)
    valid = json_body.get('valid', None)
    cvv = json_body.get('cvv', None)
    
    pay = []

    user = http.request.env['res.users'].sudo().search([('id', '=', user.get('id'))], limit=1)
    if user:
        if number == "1234 5678 9012 3456" and cvv == "123": #Başarılı
            pay.append({
                'id': 1,
                'message': "Başarılı",
                'status': True,
            })
        else:
            pay.append({
                'id': 0,
                'message': "Başarısız",
                'status': False,
            })

    pay_dict = self.get_pay_to_dict(pay)
    return {'results': pay_dict}
