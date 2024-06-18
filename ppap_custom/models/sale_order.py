from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    offer_ids = fields.One2many('offer', 'sale_id', string='Offers')
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')
    is_request_a_quote = fields.Boolean(string='Is Request a Quote', copy=False)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    

    def request_a_quote(self):
        if self.is_request_a_quote:
            raise ValidationError('A proposal has already been requested, you cannot request it again.')
        
        VendorProductModel = self.env['vendor.product']
        OfferModel = self.env['offer']
        for line in self.order_line:
            vendor_product_ids = VendorProductModel.search([('product_id', '=', line.product_id.id)])
            for vendor_p in vendor_product_ids:
                OfferModel.create({
                    'vendor_id': vendor_p.vendor_id.id,
                    'product_id': line.product_id.id,
                    'sale_line_id': line.id,
                    'sale_id': self.id,
                    'offer_price': 0,
                    'state': 'waiting',
                })
        self.update({
            'is_request_a_quote': True,
            'state': 'sent'
        })
        


    def get_offers(self):
        for record in self:
            # ids = record.offer_ids.ids
            # if not self.env.user.has_group('ppap_custom.group_ppap_custom_admin'):
            #     ids = record.offer_ids.filtered(lambda x: x.vendor_id.id == self.env.user.partner_id.id).ids

            return {
                'type': 'ir.actions.act_window',
                'name': 'Offers',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'offer',
                'domain': [('id', 'in', record.offer_ids.ids)],
            }