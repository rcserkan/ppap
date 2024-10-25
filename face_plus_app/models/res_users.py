from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta, datetime

class ResUsers(models.Model):
    _inherit = 'res.users'

    phone = fields.Char(string='Phone')
    scan_limit = fields.Integer(string='Scan Limit')

    def get_token_data(self):
            self.ensure_one()
            return {
                'user': self.bm_api_single(id),
                'id': self.id,
                'name': self.name,
                'username': self.email,
                'scan_limit': self.scan_limit,
                'iss': 'face_plus',
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=1),
            }

    def bm_api_single(self, partner_id):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'scan_limit': self.scan_limit,
        } if self else False