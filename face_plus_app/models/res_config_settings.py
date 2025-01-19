# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    face_plus_url = fields.Char(string='Face Plus Url', config_parameter='face_plus_app.face_plus_url')
    face_plus_key = fields.Char(string='Face Plus Key', config_parameter='face_plus_app.face_plus_key')
    face_plus_secret = fields.Char(string='Face Plus Secret', config_parameter='face_plus_app.face_plus_secret')
    openai_key = fields.Char(string='OpenAI Key', config_parameter='face_plus_app.openai_key')
    openai_props_character = fields.Char(string='OpenAI Karakter Props', config_parameter='face_plus_app.openai_props_character')
    openai_props_skin = fields.Char(string='OpenAI Cilt Props', config_parameter='face_plus_app.openai_props_skin')
    openai_props_mood = fields.Char(string='OpenAI Ruh Hali Props', config_parameter='face_plus_app.openai_props_mood')
    openai_props_dream = fields.Char(string='OpenAI Rüya Props', config_parameter='face_plus_app.openai_props_dream')
    openai_props_style = fields.Char(string='OpenAI Görünüm Props', config_parameter='face_plus_app.openai_props_style')
    openai_props_wish = fields.Char(string='OpenAI Dilek Props', config_parameter='face_plus_app.openai_props_wish')
    openai_props_nutrition = fields.Char(string='OpenAI Beslenme Props', config_parameter='face_plus_app.openai_props_nutrition')
    openai_props_personal = fields.Char(string='OpenAI Kişisel Props', config_parameter='face_plus_app.openai_props_personal')
