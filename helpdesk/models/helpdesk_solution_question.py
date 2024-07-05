# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.addons.helpdesk.models.helpdesk_ticket import TICKET_PRIORITY

class HelpdeskSolutionQuestion(models.Model):
    _name = "helpdesk.solution.question"
    _order = "name"
    _description = "Helpdesk Solution Question"

    name = fields.Char(required=True, index=True, translate=True)
    type_ids = fields.One2many('helpdesk.application.type', 'solution_question_id', string='Types')
    step = fields.Selection(
        [
            ('step1', 'Step 1'),
            ('step2', 'Step 2')
        ], required=True
    )