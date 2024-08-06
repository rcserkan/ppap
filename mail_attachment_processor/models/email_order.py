from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class EmailOrder(models.Model):
    _name = "email.order"
    _description = "Email Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id'

    name = fields.Char(string='Name')
    file_name = fields.Char(string='File Name')
    email = fields.Char(string='Email')
    order_date = fields.Date(string='Date')
    order_json = fields.Html(string="Order JSON")