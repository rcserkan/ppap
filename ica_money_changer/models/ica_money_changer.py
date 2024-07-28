from odoo import fields, models


class IcaMoneyChanger(models.Model):
    _name = 'ica.money.changer'
    _description = 'IcaMoneyChanger'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], default='draft')
    date = fields.Date(default=fields.Date.today)
    line_ids = fields.One2many('ica.money.changer.line', 'ica_money_changer_id')

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirmed'

    def action_processing(self):
        self.state = 'processing'
        self.line_ids.convert_currency()

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def _action_open_kiosk_mode(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/ica/ica-money-changer',
        }


class IcaMoneyChangerLine(models.Model):
    _name = 'ica.money.changer.line'
    _description = 'IcaMoneyChanger'

    ica_money_changer_id = fields.Many2one('ica.money.changer')
    from_currency_id = fields.Many2one('res.currency')
    from_amount = fields.Monetary(currency_field='from_currency_id')
    to_currency_id = fields.Many2one('res.currency', related='ica_money_changer_id.currency_id')
    to_amount = fields.Monetary(currency_field='to_currency_id', readonly=True)

    def convert_currency(self):
        for rec in self:
            rec.to_amount = rec.from_currency_id._convert(from_amount=rec.from_amount, to_currency=rec.to_currency_id)
