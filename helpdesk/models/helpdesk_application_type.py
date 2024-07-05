# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.addons.helpdesk.models.helpdesk_ticket import TICKET_PRIORITY

class HelpdeskApplicationType(models.Model):
    _name = "helpdesk.application.type"
    _order = "name"
    _description = "Helpdesk Application Type"

    name = fields.Char(required=True, index=True, translate=True)
    solution_question_id = fields.Many2one(
        'helpdesk.solution.question',
        string='Question',
    )
    request_type_ids = fields.Many2many('helpdesk.request.type', string='Types')