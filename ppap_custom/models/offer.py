from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class Offer(models.Model):
    _name = "offer"
    _description = "Offer"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id'

    vendor_id = fields.Many2one('res.partner', string='Vendor', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', track_visibility='onchange')
    sale_line_id = fields.Many2one('sale.order.line', string='Line', track_visibility='onchange')
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    offer_price = fields.Float(string='Offer Price')
    state = fields.Selection(
        [
            ('waiting', 'Waiting'),
            ('rejected', 'Rejected'),
            ('accepted', 'Accepted')
        ], default='waiting'
    )

    @api.onchange('state')
    def onchange_state(self):
        if not self.env.user.has_group('ppap_custom.group_ppap_custom_admin'):
            raise ValidationError("Only those with the authority to create proposals can modify the State field.")
    