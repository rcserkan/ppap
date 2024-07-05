# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.addons.helpdesk.models.helpdesk_ticket import TICKET_PRIORITY

class HelpdeskRequestType(models.Model):
    _name = "helpdesk.request.type"
    _order = "name"
    _description = "Helpdesk Request Type"

    name = fields.Char(required=True, index=True, translate=True)