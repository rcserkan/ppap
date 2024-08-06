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

class HelpdeskController(http.Controller):

    @http.route('/helpdesk/solution_question', type='json', auth='public', methods=['GET'], csrf=False)
    def solution_question(self):

        question_ids = request.env['helpdesk.solution.question'].sudo().search([])

        question_dict = [{
            'id': q.id,
            'name': q.name,
            'step': q.step,
            'application_type_ds': [{
                'id': type_id.id,
                'name': type_id.name,
                'request_type_ds': [{
                    'id': request_id.id,
                    'name': request_id.name,
                } for request_id in type_id.request_type_ids], 
            } for type_id in q.type_ids], 
        } for q in question_ids]


        return {'status': 'success', 'data': question_dict}

    @http.route('/helpdesk/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_helpdesk(self, **kwargs):
        image_data = kwargs.get('image')
        video_data = kwargs.get('video')

        helpdesk_id = request.env['helpdesk.ticket'].sudo().create({
            'name': kwargs.get('name'),
            'team_id': request.env['helpdesk.team'].sudo().search([], limit=1).id,
            'user_id': request.env['res.users'].sudo().search([], limit=1).id,
            'application_type_step1_id': kwargs.get('application_type_step1_id'), #1
            'request_type_step1_id': kwargs.get('request_type_step1_id'),#2
            'application_type_step2_id': kwargs.get('application_type_step2_id'),#4
            'request_type_step2_id': kwargs.get('request_type_step2_id'),#12
            'first_name': kwargs.get('first_name'),
            'last_name': kwargs.get('last_name'),
            'tc': kwargs.get('tc'),
            'gender': kwargs.get('gender'),
            'email_cc': kwargs.get('email'),
            'partner_phone': kwargs.get('phone'),
            'description': kwargs.get('description'),
            'address': kwargs.get('address'),
        })

        # Image ekle
        if image_data:
            request.env['ir.attachment'].sudo().create({
                'name': 'Helpdesk Image',
                'type': 'binary',
                'datas': base64.b64encode(image_data.encode()),
                'res_model': 'helpdesk.ticket',
                'res_id': helpdesk_id.id,
                'mimetype': 'image/jpeg'  # uygun mime type kullanın
            })
        
        # Video ekle
        if video_data:
            request.env['ir.attachment'].sudo().create({
                'name': 'Helpdesk Video',
                'type': 'binary',
                'datas': base64.b64encode(video_data.encode()),
                'res_model': 'helpdesk.ticket',
                'res_id': helpdesk_id.id,
                'mimetype': 'video/mp4'  # uygun mime type kullanın
            })


        return {'status': 'success', 'message': 'Helpdesk record successfully created.', 'crm_id': helpdesk_id.id}
