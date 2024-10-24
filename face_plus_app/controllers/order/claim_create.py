from odoo import http, _
from .. import external_api
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

@http.route('/api/claims', type='json', auth='public', methods=["POST", "OPTIONS"], csrf=False, cors="*")
@external_api.rest_response()
@external_api.authenticated()
def claim_create(self, **kw):
    json_body = kw["json_body"]
    
    items = json_body.get('items', [])
    claim_ids = []
    for item in items:
        sale_line_id = http.request.env['sale.order.line'].search([('id', '=', int(item['order_line']))], limit=1)
        
        check_claim = http.request.env['rc.claim'].search([('order_line', '=', int(item['order_line']))], limit=1)
        if check_claim:
            raise UserError(_('I have an existing Claim for this product (%s)' %(sale_line_id.product_id.default_code)))
        
        claim = http.request.env['rc.claim'].create({
            'sale_id': sale_line_id.order_id.id,
            'order_line': sale_line_id.id,
            'claim_type': int(item['claim_type']),
            'productpart': int(item['productpart']),
            'note': item['note'],
        })
        for f in item['files']:
            
            attachment = http.request.env['ir.attachment'].sudo().create({
                'name': f['name'],
                'datas': f['base64'],
                'res_id': claim.id,
                'res_model': 'rc.claim',
                'mimetype': f['mimetype'],
            })
            
            claim.message_post(body="", attachments=attachment, attachment_ids=[attachment.id])

        claim_ids.append(claim)


    claims_dict = self.get_claim_to_dict(claim_ids)
    return {'results': claims_dict}
