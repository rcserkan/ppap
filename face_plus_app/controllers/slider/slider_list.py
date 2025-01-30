# -*- coding: utf-8 -*-

from odoo import http
from .. import dictionary
from .. import external_api

import logging
_logger = logging.getLogger(__name__)


@http.route('/api/slider_list', auth='public', type="json", methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
@external_api.authenticated()
def slider_list(self, **kw):
    user = dictionary.get_login_user()
    # filters = [('create_uid', '=', user.get('id'))]

    slider_ids = http.request.env['face.plus.slider'].sudo().search([], order='id desc')

    slider_dict = self.get_slider_to_dict(slider_ids)
    return {'results': slider_dict}
