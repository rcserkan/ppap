from odoo import _, api, fields, models, tools

class VendorProduct(models.Model):
    _name = "vendor.product"
    _description = "Vendor Product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'default_code, name, id'

    active = fields.Boolean('Active', default=True, track_visibility='onchange')
    name = fields.Char('Name', track_visibility='onchange')
    default_code = fields.Char('Internal Reference', index=True, track_visibility='onchange')
    barcode = fields.Char('Barcode', copy=False, track_visibility='onchange')
    lst_price = fields.Float('Sales Price', track_visibility='onchange')
    image_1920 = fields.Image("Image", track_visibility='onchange')
    vendor_id = fields.Many2one('res.partner', string='Vendor', track_visibility='onchange')
    product_id = fields.Many2one('product.product', string='Product', track_visibility='onchange')
