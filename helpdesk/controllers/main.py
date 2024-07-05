# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import _, http, fields
from odoo.http import request
from odoo.addons.payment import utils as payment_utils
from odoo.addons.account.controllers import portal
from odoo.addons.portal.controllers import portal as PortalP
from odoo.addons.payment.controllers.portal import PaymentPortal

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website_sale.controllers.main import WebsiteSale 
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.addons.portal.controllers.mail import _message_post_helper
import base64
_logger = logging.getLogger(__name__)

class CrmController(http.Controller):

    @http.route('/helpdesk/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_helpdesk(self, **kwargs):
        headers = request.httprequest.headers
        auth_header = headers.get('Authorization')

        if auth_header and auth_header.startswith('Basic '):
            auth_token = auth_header.split(' ')[1]
            decoded_auth = base64.b64decode(auth_token).decode('utf-8')
            username, password = decoded_auth.split(':')

            login_status = request.session.authenticate("ppap", username, password)
            if not login_status:
                return {'status': 'error', 'message': 'Username or password incorrect.'}
            
            helpdesk_id = request.env['crm.lead'].sudo().create({
                'name': kwargs.get('full_name'),
               
            })

            return {'status': 'success', 'message': 'Helpdesk record successfully created.', 'crm_id': helpdesk_id.id}
        else:
            return {'status': 'error', 'message': 'Authorization header is missing.'}
