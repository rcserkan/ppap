# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    face_plus_url = fields.Char(string='Face Plus Url', config_parameter='face_plus_app.face_plus_url')
    face_plus_key = fields.Char(string='Face Plus Key', config_parameter='face_plus_app.face_plus_key')
    face_plus_secret = fields.Char(string='Face Plus Secret', config_parameter='face_plus_app.face_plus_secret')
    openai_key = fields.Char(string='OpenAI Key', config_parameter='face_plus_app.openai_key')
    openai_props = fields.Char(string='OpenAI Prop', config_parameter='face_plus_app.openai_props')
